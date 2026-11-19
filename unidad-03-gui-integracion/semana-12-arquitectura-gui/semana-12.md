# Semana 12 — Arquitectura de GUI

> Una ventana no es magia: es un objeto que escucha eventos y dibuja lo que el modelo dice.

## Objetivos de aprendizaje

- Explicar qué es una interfaz gráfica y cómo funciona el bucle de eventos.
- Crear una ventana raíz con `tk.Tk()` y cerrarla sin dejar procesos vivos.
- Colocar `Label`, `Button`, `Entry` y `Frame` con `pack`, `grid` y `place`.
- Organizar widgets en una jerarquía clara y elegir la geometría adecuada.
- Separar la interfaz de la lógica y aplicar MVC a un videojuego.
- Convertir un wireframe sencillo en código funcional.

## ¿Por qué importa?

Hasta ahora tus programas viven en la terminal: escribes un comando, lees una línea de texto y repites. Funciona, pero obliga al usuario a recordar instrucciones y a imaginar el estado del sistema. Una interfaz gráfica cambia eso: muestra las opciones, reacciona a un clic y confirma cada acción en el mismo lugar donde ocurrió.

Piensa en la ficha de un personaje de RPG: en consola imprimes nombre, clase, nivel y vida; en una GUI cada dato tiene su campo, un botón sube de nivel y la vida se actualiza al instante. El usuario ve el efecto de su acción sin escribir nada.

La GUI también plantea un problema nuevo: si mezclas botones, validaciones y reglas del juego, terminas con una ventana imposible de mantener. Esta semana no se trata de «hacer ventanas», sino de **arquitectura**: qué parte piensa, qué parte dibuja y qué parte conecta ambas.

Tkinter viene incluido en Python: no necesitas instalar nada y es la herramienta del proyecto integrador.

:::info
Una GUI no reemplaza la POO: la pone a prueba. Cada widget es un objeto, cada ventana es un objeto y cada acción del usuario termina invocando un método de algún objeto.
:::

## Concepto central

### Qué es una GUI

Una **interfaz gráfica de usuario** (GUI) es una capa visual compuesta por **widgets**: etiquetas, botones, campos de texto, listas, marcos. Cada widget es un objeto con estado (texto, tamaño, color) y comportamiento (qué pasa cuando lo pulsan).

En Tkinter, la ventana principal es un objeto `tk.Tk`. Los demás widgets se crean indicando su **contenedor padre** como primer argumento:

```python
import tkinter as tk

raiz = tk.Tk()                      # ventana raíz
marco = tk.Frame(raiz)              # hijo de la raíz
titulo = tk.Label(marco, text="Hola")  # hijo del marco
```

Eso forma un árbol: raíz → marcos → widgets. La posición de cada widget depende de su padre, no de la pantalla completa. Cambiar el tamaño de un `Frame` afecta a sus hijos, y destruir un padre destruye su descendencia.

### El bucle de eventos

Una GUI no se ejecuta de arriba abajo y termina. Después de construir la ventana, el programa entra en `mainloop()` y se queda esperando:

```text
sistema operativo          Tkinter                 tu código
   clic / tecla   ─────►   cola de eventos  ─────► callback
                                                    │
   repintar       ◄─────   actualiza widgets ◄──────┘
```

`mainloop()` es un bucle interno que:

1. Espera un evento (clic, tecla, cambio de tamaño, temporizador).
2. Identifica qué widget lo recibió.
3. Ejecuta la función asociada, si existe.
4. Redibuja lo que haya cambiado.
5. Vuelve al paso 1.

No escribas ese bucle con `while`: registra **callbacks** —funciones normales, normalmente métodos— y deja que Tkinter los llame.

```python
def _saludar(self) -> None:
    nombre = self.entrada.get().strip() or "aventurero"
    self.saludo.config(text=f"¡Hola, {nombre}!")
```

`command=self._saludar` entrega la función sin ejecutarla; con paréntesis la ejecutas al construir el botón y el clic no hace nada.

:::warning
`mainloop()` bloquea el hilo principal mientras la ventana está abierta. Cualquier tarea larga dentro de un callback congela la interfaz. Para tareas programadas usa `after(ms, funcion)`, no `time.sleep()`.
:::

### Las tres geometrías

Tkinter trae tres gestores de geometría que responden a la misma pregunta —¿dónde va cada widget?— con estrategias distintas.

**`pack`** coloca widgets en orden, como bloques apilados. Es ideal para barras, encabezados y columnas simples.

```python
tk.Label(raiz, text="Ficha del héroe").pack(pady=10)
tk.Button(raiz, text="Cerrar", command=raiz.destroy).pack(side="bottom", pady=10)
```

**`grid`** coloca widgets en una cuadrícula de filas y columnas. Es la mejor opción para formularios, fichas y paneles con alineación.

```python
tk.Label(raiz, text="Nombre:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
tk.Entry(raiz).grid(row=0, column=1, sticky="ew", padx=8, pady=4)
raiz.columnconfigure(1, weight=1)  # la columna del campo se estira
```

**`place`** usa coordenadas absolutas o relativas. Sirve para superposiciones y diseños muy específicos, pero no se adapta bien al redimensionado.

```python
tk.Label(raiz, text="v1.0").place(relx=1.0, rely=1.0, anchor="se", x=-8, y=-8)
```

| Criterio | `pack` | `grid` | `place` |
|---|---|---|---|
| Modelo mental | bloques en orden | filas y columnas | coordenadas |
| Formularios | regular | excelente | mala idea |
| Redimensionado | bueno con `fill`/`expand` | bueno con `weight` | manual |
| Superposición | no | no | sí |
| Curva de aprendizaje | baja | media | baja, pero frágil |

Dos reglas:

- No mezcles `pack` y `grid` **en el mismo contenedor**. Puedes usar `pack` en la raíz y `grid` dentro de un `Frame` hijo; lo que no puede convivir son ambos gestores administrando hijos del mismo padre.
- Si usas `grid`, configura `weight` para que el contenido se expanda.

### Separar interfaz y lógica

El error más común al empezar es escribir la lógica dentro del callback: subir el nivel, recalcular la vida y actualizar la etiqueta en el mismo método. Eso mezcla tres responsabilidades: regla del juego, estado y dibujo. Si mañana quieres subir de nivel desde la consola o una prueba automática, no puedes.

La alternativa es un **modelo** que no sepa que existe una ventana:

```python
class Personaje:
    def __init__(self, nombre: str, clase: str, nivel: int = 1) -> None:
        self.nombre = nombre
        self.clase = clase
        self.nivel = nivel
        self.vida_maxima = 80 + nivel * 20
        self.vida = self.vida_maxima

    def subir_nivel(self) -> None:
        self.nivel += 1
        self.vida_maxima = 80 + self.nivel * 20
        self.vida = self.vida_maxima
```

Y una **vista** que lee del modelo y pinta:

```python
class VistaFicha(tk.Frame):
    def __init__(self, contenedor: tk.Misc, personaje: Personaje) -> None:
        super().__init__(contenedor)
        self.personaje = personaje
        self.lbl_nivel = tk.Label(self)
        self.lbl_nivel.grid(row=0, column=0)

    def actualizar(self) -> None:
        self.lbl_nivel.config(text=str(self.personaje.nivel))
```

El puente entre ambos es el **controlador**: un método que pide la acción al modelo y refresca la vista.

```python
def _subir_nivel(self) -> None:
    self.personaje.subir_nivel()
    self.actualizar()
```

### MVC aplicado a un videojuego

MVC separa tres papeles:

| Componente | Responsabilidad | En un RPG |
|---|---|---|
| Modelo | Datos y reglas | `Personaje`, `Partida`, `Inventario` |
| Vista | Widgets y presentación | `VistaFicha`, `VistaInventario` |
| Controlador | Recibir eventos y coordinar | métodos `command` de botones |

El flujo de un clic queda así:

```text
clic en «Subir de nivel»
        │
        ▼
controlador: personaje.subir_nivel()
        │
        ▼
modelo actualiza nivel y vida
        │
        ▼
vista.actualizar() lee el modelo y repinta
```

El modelo nunca importa `tkinter`. Esa es la prueba definitiva de que la separación existe. Si puedes ejecutar tus reglas de combate en un script de consola, la arquitectura está bien.

:::success
Regla de oro: si borras todos los widgets, la lógica del juego debe seguir funcionando.
:::

### Del wireframe al código

Antes de escribir `grid(row=3, column=1)` conviene dibujar cajas. Un wireframe de la ficha podría ser:

```text
┌─────────────────────────────┐
│  Lyra                       │  ← nombre (fila 0, dos columnas)
├──────────────┬──────────────┤
│ Clase: Maga  │ Nivel: 3     │
│ Vida: 140    │ Estado: OK   │
├──────────────┴──────────────┤
│      [ Subir de nivel ]     │
└─────────────────────────────┘
```

Cada caja es un widget; cada división, una fila o columna. El wireframe te obliga a decidir la jerarquía antes de pelear con la geometría. Si una zona agrupa varios widgets, probablemente sea un `Frame`.

## Diagrama / modelo

```text
tk.Tk (ventana raíz)
└── VistaFicha (Frame)
    ├── Label  nombre
    ├── Label  «Clase:»     Label  valor
    ├── Label  «Nivel:»     Label  valor
    ├── Label  «Vida:»      Label  valor
    └── Button «Subir de nivel» ──► controlador ──► Personaje
```

## Errores comunes

**Olvidar `mainloop()`.** El script construye la ventana y termina; la ventana aparece y desaparece. `mainloop()` es la última línea de `main()`.

**Crear dos ventanas raíz.** `tk.Tk()` debe existir una sola vez por aplicación. Para ventanas secundarias se usa `tk.Toplevel(raiz)`.

**Mezclar `pack` y `grid` en el mismo padre.** Python lanza `TclError: cannot use geometry manager pack inside ... which already has slaves managed by grid`. Solución: un `Frame` por zona y un solo gestor dentro de cada uno.

**Congelar la interfaz con `time.sleep()`.** El callback duerme también el repintado. Usa `raiz.after(1000, funcion)`.

**Guardar la lógica en la vista.** Si el botón calcula la vida y además la dibuja, no podrás probar la regla sin abrir una ventana. Mueve el cálculo al modelo.

**No validar la entrada.** `int("")` lanza `ValueError`; si no lo capturas, el callback imprime un traceback y la ventana queda muda. Valida y muestra el mensaje en la interfaz.

## Buenas prácticas

- Un solo `tk.Tk()` y una función `main()` que lo construya y arranque.
- Un `Frame` por zona lógica: cabecera, formulario, lista, acciones.
- `grid` para formularios y fichas; `pack` para barras; `place` solo para detalles.
- `sticky="nsew"` y `weight` cuando quieras que algo crezca.
- Padding consistente (8, 12, 16) en lugar de píxeles aleatorios.
- Modelo sin `import tkinter`; vista sin reglas de negocio.
- Callbacks cortos: validan, llaman al modelo y refrescan.
- Cierra con la X, `Alt+F4` o `raiz.destroy()`; no mates el proceso desde la terminal.

:::reto
Dibuja en papel el wireframe de tu proyecto integrador: tres zonas como máximo. Si no cabe en tres, probablemente estás mezclando pantallas.
:::

## Checklist de la semana

- [ ] Explico con mis palabras qué hace `mainloop()`.
- [ ] Creé una ventana con `tk.Tk()` y la cerré correctamente.
- [ ] Usé `Label`, `Button`, `Entry` y `Frame` en una jerarquía clara.
- [ ] Coloqué widgets con `pack`, con `grid` y con `place` al menos una vez.
- [ ] Sé por qué no se mezclan `pack` y `grid` en el mismo contenedor.
- [ ] Separé un modelo (`Personaje`) de su vista.
- [ ] Identifico modelo, vista y controlador en mi ejercicio.
- [ ] Convertí un wireframe en código funcional.

## Resumen

Una GUI es un árbol de widgets sobre una ventana raíz que vive dentro de un bucle de eventos. Tú construyes el árbol, registras callbacks y dejas que Tkinter despache los eventos. `pack`, `grid` y `place` resuelven la colocación con distintas estrategias; `grid` es la más útil para formularios y fichas.

La decisión arquitectónica importante es separar: el modelo contiene datos y reglas, la vista dibuja y el controlador conecta eventos con acciones. `Personaje` no sabe que existe una ventana; `VistaFicha` solo lee y muestra. Esa separación te permitirá crecer sin reescribir todo.

## Siguiente paso

La próxima semana cambiamos los widgets clásicos por `ttk`: formularios con `Combobox`, listas con `Treeview`, estilos propios y validación visual. El objetivo es que la ficha se convierta en un creador de personajes completo.
