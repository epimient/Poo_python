# Dudas frecuentes — Semana 14

## ¿Por qué `command=self._atacar` funciona y `command=self._atacar()` no?

Porque `command` espera una función, no el resultado de ejecutarla. Sin paréntesis entregas la función para que Tkinter la llame cuando ocurra el clic. Con paréntesis la ejecutas en ese instante, antes de que exista un clic, y Tkinter recibe `None`.

```python
boton = ttk.Button(marco, text="Atacar", command=self._atacar)   # correcto
boton = ttk.Button(marco, text="Atacar", command=self._atacar()) # incorrecto
```

## ¿Cómo paso argumentos a un callback?

Con `lambda` y un argumento con valor por defecto, o con `functools.partial`. El valor por defecto evita el clásico problema de que todos los botones terminen usando el último elemento del bucle.

```python
for nombre in ("guerrero", "mago", "arquero"):
    ttk.Button(marco, text=nombre,
               command=lambda n=nombre: self._elegir(n)).pack()
```

## ¿Cuándo uso `command` y cuándo `bind`?

`command` para la acción principal del widget: pulsar **Atacar**, **Guardar** o **Reiniciar**. `bind` para gestos que no son la acción del widget: una tecla, un clic en un panel, el foco o el cierre de la ventana. Si el botón y la tecla hacen lo mismo, ambos deben llamar al mismo método.

```python
self.btn_atacar = ttk.Button(marco, text="Atacar", command=self._atacar)
self.ventana.bind("<KeyPress-a>", lambda evento: self._atacar())
```

## ¿Qué información trae el objeto evento?

`widget` (quién lo recibió), `x` e `y` (posición del ratón), `keysym` (nombre de la tecla), `char` (carácter) y `num` (botón del ratón). No todos los atributos existen en todos los eventos: comprueba antes de usarlos.

```python
def _al_pulsar(self, evento: tk.Event) -> None:
    if (evento.keysym or "").lower() == "a":
        self._atacar()
```

## ¿Cómo evito que la tecla A active el ataque mientras escribo el nombre?

Revisa qué widget tiene el foco. Si es un `Entry` o un `Combobox`, ignora el atajo.

```python
foco = self.ventana.focus_get()
if isinstance(foco, (tk.Entry, ttk.Entry, ttk.Combobox)):
    return
```

## ¿Por qué la ventana se congela cuando uso `time.sleep()`?

Porque `sleep` detiene el hilo que ejecuta el bucle de eventos: Tkinter no puede repintar ni atender clics. Usa `after` para programar la respuesta enemiga sin bloquear, y `after_cancel` si reinicias o cierras antes de que se ejecute.

```python
self._pendiente = self.ventana.after(600, self._turno_enemigo)

def _reiniciar(self) -> None:
    if self._pendiente is not None:
        self.ventana.after_cancel(self._pendiente)
        self._pendiente = None
```

## ¿Puedo actualizar un `Label` desde la clase `Combate`?

No es recomendable: el dominio quedaría atado a Tkinter y no podrías probarlo sin pantalla. Haz que el dominio cambie su estado y devuelva datos; la vista llama a su propio método de refresco.

```python
# En la vista
eventos = self.combate.turno_jugador()
self._escribir(eventos)
self._refrescar()
```

## ¿Cómo guardo un objeto con `json`?

JSON solo entiende diccionarios, listas, números, cadenas, booleanos y `None`. Convierte el objeto con un método `a_dict()` y reconstruyelo con `desde_dict()`. No uses `pickle` para una entrega: el archivo no es legible y es inseguro al abrir datos ajenos.

```python
def a_dict(self) -> dict[str, object]:
    return {
        "nombre": self.nombre,
        "hp": self.hp,
        "hp_max": self.hp_max,
        "ataque": self.ataque,
        "defensa": self.defensa,
    }

@classmethod
def desde_dict(cls, datos: dict) -> "Personaje":
    personaje = cls(
        nombre=str(datos["nombre"]),
        clase="jugador",
        hp_max=int(datos["hp_max"]),
        ataque=int(datos["ataque"]),
        defensa=int(datos["defensa"]),
    )
    personaje.hp = int(datos["hp"])
    return personaje
```

Al cargar, valida que el HP esté entre 0 y el máximo y que las claves existan; si algo falla, lanza `ValueError` y muéstralo en la interfaz.
