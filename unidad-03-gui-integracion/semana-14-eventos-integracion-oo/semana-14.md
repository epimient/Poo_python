# Semana 14 — Eventos e integración de una aplicación OO

> La interfaz no piensa: avisa, muestra y delega. La lógica de tu juego vive en las clases.

## Objetivos de aprendizaje

- Distinguir un callback, el parámetro `command` y el método `bind`.
- Leer el objeto evento y usar teclado y ratón sin duplicar lógica.
- Diseñar el ciclo **evento → lógica → vista** en una aplicación Tkinter.
- Conectar widgets con clases de dominio como `Personaje` y `Combate`.
- Guardar y cargar una partida con `json`, controlando los errores de forma visible.
- Justificar por qué la lógica no debe vivir dentro de los callbacks.

## ¿Por qué importa?

Cuando empiezas con Tkinter, lo natural es escribir la lógica dentro del botón: restar vida, comprobar si el enemigo murió, actualizar tres etiquetas y mostrar un mensaje. Funciona en una demo de veinte líneas. El problema aparece con un segundo botón, una tecla, la barra de vida y el guardado: el mismo bloque se copia en tres callbacks y cada cambio se hace tres veces.

En un proyecto real —y en el P3 de este curso— la ventana es solo una capa. El dominio (`Personaje`, `Combate`, `Partida`) debe poder ejecutarse sin pantalla: en una prueba automática, en consola o desde otro cliente. La interfaz traduce clics y teclas en llamadas a ese dominio, y después vuelve a pintar lo que cambió. Esta semana construyes una arena de combate completa con esa separación. La arena final abre una ventana real y permite elegir clase, atacar, ver el registro, reiniciar y guardar en JSON.

## Concepto central

### El bucle de eventos

Tkinter no ejecuta tu programa de arriba abajo y termina. Al llamar a `mainloop()` entra en un bucle: espera un evento (un clic, una tecla, un temporizador), llama a la función asociada y vuelve a esperar. Tu código no hace `while True`: registra funciones y el bucle las invoca.

### callback, command y bind

Un **callback** es una función que entregas para que otro la llame más tarde. No la ejecutas tú con paréntesis: pasas su nombre. `command=self._atacar` entrega la función; `command=self._atacar()` la ejecuta en ese instante y guarda su resultado, que casi siempre es `None` y no hace nada.

| Aspecto | `command` | `bind` |
|---|---|---|
| Se usa en | Botones, `Checkbutton`, menús | Cualquier widget o la ventana |
| Dispara con | La acción principal del widget | Un evento concreto: tecla, clic, foco |
| Recibe | Nada (por defecto) | Un objeto evento |
| Ideal para | «Atacar», «Guardar», «Reiniciar» | Atajos de teclado, clic en un panel, `<Return>` |
| Varios gestos | No | Sí, puedes enlazar varios eventos al mismo widget |

Usa `command` para la acción evidente del widget y `bind` para gestos adicionales. Si un botón y una tecla hacen lo mismo, ambos llaman al mismo método.

### El objeto evento

Cuando usas `bind`, Tkinter pasa un objeto evento con atributos útiles: `widget` (quién lo recibió), `x` e `y` (posición del ratón), `keysym` (nombre de la tecla, por ejemplo `"a"` o `"Return"`), `char` (carácter escrito) y `num` (botón del ratón). Puedes ignorarlo con `_evento`, pero no lo inventes: sus atributos son los que documenta Tkinter.

:::info
El evento pertenece a la interfaz. No lo guardes como parte del estado del juego ni lo pases al dominio.
:::

### Tres capas, una dirección

- **Dominio:** reglas del juego. `Personaje` calcula daño; `Combate` lleva turnos, vida y ganador. No importa `tkinter`.
- **Persistencia:** convierte el dominio a JSON y lo reconstruye. Tampoco importa `tkinter`.
- **Vista:** `ArenaApp` crea widgets, escucha eventos, llama al dominio y refresca etiquetas, barras y el registro.

:::warning
Si dentro de un callback escribes `enemigo.hp -= 12` y además actualizas la barra, estás mezclando capas. Esa resta pertenece a `Personaje.recibir_dano()`. El callback solo debería decir «ataca» y luego «pinta el resultado».
:::

## Código paso a paso

### Paso 1: dominio sin ventana

```python
class Personaje:
    def __init__(self, nombre: str, clase: str, hp_max: int,
                 ataque: int, defensa: int) -> None:
        if hp_max <= 0 or ataque <= 0 or defensa < 0:
            raise ValueError("Estadísticas inválidas")
        self.nombre = nombre
        self.clase = clase
        self.hp_max = hp_max
        self.hp = hp_max
        self.ataque = ataque
        self.defensa = defensa

    @property
    def esta_vivo(self) -> bool:
        return self.hp > 0

    def recibir_dano(self, cantidad: int) -> int:
        aplicado = min(max(0, cantidad), self.hp)
        self.hp -= aplicado
        return aplicado
```

Nada de Tkinter. Puedes probarla sin abrir una ventana.

### Paso 2: el combate decide, la vista obedece

`Combate` recibe dos personajes y una semilla opcional. Sus métodos devuelven eventos `(tipo, texto)` para que la interfaz sepa qué escribir y de qué color.

```python
def turno_jugador(self) -> list[tuple[str, str]]:
    if self.terminado:
        return [("sistema", "El combate ya terminó.")]
    dano = self.jugador.atacar(self.enemigo, self.rng)
    eventos = [("jugador", f"Atacas y quitas {dano} de HP.")]
    if not self.enemigo.esta_vivo:
        self.terminado = True
        self.ganador = self.jugador.nombre
        eventos.append(("sistema", "¡Victoria!"))
    self.log.extend(eventos)
    return eventos
```

### Paso 3: `command` para el botón

```python
self.btn_atacar = ttk.Button(acciones, text="Atacar (A)", command=self._atacar)
```

```python
def _atacar(self) -> None:
    if self.combate is None or self.combate.terminado:
        return
    eventos = self.combate.turno_jugador()
    self._escribir(eventos)
    self._refrescar()
```

El callback tiene dos responsabilidades y ninguna regla: delegar y pintar.

### Paso 4: `bind` para teclado y ratón

```python
self.ventana.bind("<Key>", self._al_pulsar_tecla)
self.panel_enemigo.bind("<Button-1>", self._inspeccionar_enemigo)

def _al_pulsar_tecla(self, evento: tk.Event) -> None:
    if isinstance(self.ventana.focus_get(), (tk.Entry, ttk.Entry, ttk.Combobox)):
        return  # no atacar mientras se escribe el nombre
    if (evento.keysym or "").lower() == "a":
        self._atacar()
```

La tecla **A** y el botón llaman a `_atacar`; el clic en el enemigo muestra su inspección.

### Paso 5: una sola función de refresco

```python
def _refrescar_panel(self, ui: dict, personaje: Personaje | None) -> None:
    if personaje is None:
        ui["hp_texto"].configure(text="HP — / —")
        ui["barra"].configure(maximum=100, value=0)
        return
    ui["hp_texto"].configure(text=f"HP {personaje.hp} / {personaje.hp_max}")
    ui["barra"].configure(maximum=personaje.hp_max, value=personaje.hp)
```

No actualices etiquetas sueltas en cada callback: concentra el dibujo en `_refrescar()`.

### Paso 6: enemigo automático con `after`

Nunca uses `time.sleep()` dentro de un callback: congela el bucle de eventos y la ventana deja de responder. Para una pausa usa `after`, que programa una función sin bloquear:

```python
self._pendiente = self.ventana.after(600, self._turno_enemigo)
```

El botón se deshabilita mientras el enemigo responde. Si el jugador reinicia o carga antes, cancela el temporizador con `after_cancel`.

### Paso 7: guardar y cargar con JSON

JSON no entiende objetos de Python: convierte cada personaje a un diccionario y reconstruye el combate al leer:

```python
def a_dict(self) -> dict[str, object]:
    return {
        "turno": self.turno,
        "terminado": self.terminado,
        "ganador": self.ganador,
        "jugador": self.jugador.a_dict(),
        "enemigo": self.enemigo.a_dict(),
        "log": [{"tipo": t, "texto": x} for t, x in self.log],
    }
```

Al cargar, valida que el archivo exista, que sea JSON, que tenga las claves y que el HP esté en rango. Un archivo dañado debe mostrar un error visible y no romper la aplicación.

```python
try:
    combate = cargar_partida(self.ruta_partida)
except FileNotFoundError:
    self._avisar("Todavía no hay ninguna partida guardada.", error=True)
except (OSError, ValueError) as exc:
    messagebox.showerror("Partida inválida", str(exc))
```

:::success
Guardar de forma atómica es un detalle profesional: escribe primero en `partida.json.tmp` y luego reemplaza el archivo final. Si el programa se cierra a mitad de la escritura, la partida anterior no se corrompe.
:::

## Diagrama / modelo

```text
   clic / tecla / after
          │
          ▼
   callback de la vista  ──►  método del dominio
   (_atacar, _guardar)         (Combate.turno_jugador)
          │                          │
          │                          ▼
          │                    estado + eventos
          ▼                          │
   _refrescar() / _escribir() ◄──────┘
          │
          ▼
   etiquetas, barra, registro
```

La flecha nunca va del dominio a la vista. `Combate` no sabe que existe un `Label`; devuelve datos y la vista decide cómo mostrarlos.

## Errores comunes

- **`command=self._atacar()`**: ejecuta la función al construir la ventana. Usa `command=self._atacar`.
- **Lógica duplicada en botón y tecla**: dos copias que se desincronizan. Un método, dos disparadores.
- **`time.sleep()` para el turno enemigo**: congela la interfaz. Usa `after`.
- **Guardar el objeto con `json.dumps(personaje)`**: lanza `TypeError`. Serializa con `a_dict()`.
- **Confiar en el archivo del usuario**: un JSON incompleto debe dar un mensaje claro, no un `KeyError` sin contexto.
- **Atacar mientras el enemigo responde**: activa dos veces el botón y adelanta turnos. Deshabilítalo con `state="disabled"` y usa una bandera.
- **Crear widgets desde el dominio**: acopla el juego a Tkinter y no se puede probar sin pantalla.

:::error
Un `except` vacío en un callback oculta el fallo y deja la ventana mintiendo sobre el estado real. Captura solo lo que sabes resolver y muestra el resto.
:::

## Buenas prácticas

- Mantén los callbacks cortos: validar, delegar, refrescar.
- Nombra los métodos por intención (`_iniciar_combate`, `_guardar`), no por widget (`_boton1_click`).
- Centraliza el refresco de la vista en una sola función.
- Inyecta una semilla (`random.Random(semilla)`) para reproducir pruebas.
- Valida en los bordes: entrada del usuario al iniciar y archivo al cargar.
- Muestra los errores en la ventana; usa `messagebox` solo para interrumpir.
- Cancela los `after` pendientes al reiniciar o cerrar.
- Prueba el dominio sin Tkinter y la ventana en una pantalla real.

:::reto
Agrega un botón «Poción» con dos usos por combate. La curación debe ser un método del dominio, el contador debe guardarse en JSON y el botón debe deshabilitarse cuando no queden pociones. Sin lógica dentro del callback.
:::

## Checklist de la semana

- [ ] Explico la diferencia entre `command` y `bind` con un ejemplo propio.
- [ ] Mi callback de ataque no contiene reglas de daño ni de turnos.
- [ ] La ventana responde a un botón y al menos a una tecla con el mismo método.
- [ ] La barra y la etiqueta de HP se actualizan desde una función de refresco.
- [ ] Puedo guardar, cerrar, abrir de nuevo y cargar la partida sin perder el estado.
- [ ] Un JSON dañado muestra un error visible y la aplicación sigue abierta.
- [ ] El combate funciona con `python3 arena_tkinter.py` y con `--semilla` para repetir pruebas.

## Resumen

Los eventos son la entrada de una aplicación de escritorio, no su cerebro. Tkinter te ofrece `command` para la acción principal de un widget y `bind` para gestos adicionales; ambos deben apuntar a métodos delgados. La lógica vive en clases de dominio que pueden probarse sin ventana, la persistencia convierte ese estado a JSON y la vista se limita a leer el estado y pintarlo. Con `after` consigues turnos automáticos sin congelar la interfaz. Esta separación es lo que se evalúa en el P3: si cambias Tkinter por otra biblioteca, `Combate` debería seguir funcionando.

## Siguiente paso

La semana 15 es la evaluación del P3: un arcade con interfaz gráfica, CRUD completo, arquitectura por capas, validaciones, `command` y al menos un `bind`, persistencia JSON tolerante a errores y documentación profesional. Llega con la arena funcionando y reutiliza su estructura: dominio probado, persistencia aislada y una vista que solo conecta widgets. `Personaje` y `Combate` ya te muestran cómo colaboran dos entidades.
