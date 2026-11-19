# Semana 13 — Componentes y organización visual

> Una interfaz clara no decora: ordena, guía y dice qué pasó sin que el usuario tenga que adivinar.

## Objetivos de aprendizaje

- Sustituir widgets clásicos de `tk` por widgets temáticos de `ttk`.
- Usar `Label`, `Entry`, `Combobox`, `Treeview`, `Notebook` y `Button` en una misma ventana.
- Agrupar controles con `Frame` y `LabelFrame` según su función.
- Definir estilos coherentes con `ttk.Style`.
- Construir formularios con validación visual y mensajes de error claros.
- Aplicar jerarquía visual, espaciado y alineación.
- Prototipar un creador de personajes completo.

## ¿Por qué importa?

La semana pasada lograste que una ventana funcionara; esta la vuelves usable. Una interfaz que se entiende en tres segundos agrupa lo que va junto, alinea etiquetas, conserva un botón principal y explica los errores donde ocurrieron.

En un creador de personajes, el usuario escribe un nombre, elige una clase y ajusta un nivel. Si el nombre está vacío, debe verlo junto al campo, con el foco puesto ahí; al guardar, la lista confirma que el personaje existe. Ese conjunto de detalles es el **feedback**, tan importante como la lógica.

`ttk` es la capa de widgets temáticos de Tkinter. Usa el aspecto nativo, separa apariencia de configuración y añade componentes que `tk` no trae, como `Combobox`, `Treeview` y `Notebook`. Sigue siendo biblioteca estándar.

:::info
La regla del proyecto integrador es explícita: Tkinter + `ttk`, sin dependencias externas. Lo que aprendas esta semana es exactamente lo que usarás en la entrega.
:::

## Concepto central

### `tk` frente a `ttk`

`tk` ofrece widgets básicos con opciones como `bg`, `fg` y `font` por widget. `ttk` ofrece widgets **temáticos**: su apariencia proviene de un tema y se configura mediante estilos compartidos.

| Necesidad | Widget `tk` | Widget `ttk` |
|---|---|---|
| Texto | `tk.Label` | `ttk.Label` |
| Botón | `tk.Button` | `ttk.Button` |
| Campo de texto | `tk.Entry` | `ttk.Entry` |
| Lista desplegable | — | `ttk.Combobox` |
| Tabla | — | `ttk.Treeview` |
| Pestañas | — | `ttk.Notebook` |
| Contenedor | `tk.Frame` | `ttk.Frame` |
| Contenedor con título | `tk.LabelFrame` | `ttk.LabelFrame` |

No se trata de prohibir `tk`: `Frame`, `Toplevel` y `Canvas` siguen siendo útiles. La convención sana es que **todo control use `ttk`** y que no mezcles estilos en una misma zona.

En `ttk` no cambias el fondo de un botón con `bg`: defines un **estilo** y lo asignas. Así evitas que cada botón invente su color.

### Contenedores que explican la pantalla

Un `Frame` es una caja invisible que agrupa widgets con su propio gestor de geometría. Un `LabelFrame` añade título y borde: perfecto para separar «Nuevo personaje», «Vista previa» y «Personajes creados».

```python
formulario = ttk.LabelFrame(cuerpo, text=" Nuevo personaje ", padding=16)
formulario.grid(row=0, column=0, sticky="nsew")
```

`Notebook` añade pestañas para varias vistas del mismo modelo sin saturar la pantalla:

```python
pestanas = ttk.Notebook(raiz)
pestanas.add(ttk.Frame(pestanas), text="Personajes")
pestanas.add(ttk.Frame(pestanas), text="Inventario")
pestanas.pack(fill="both", expand=True)
```

La jerarquía define qué se mueve junto y qué gestor manda en cada zona. Un buen diseño tiene tres o cuatro contenedores grandes, no treinta widgets sueltos.

### Estilos con `ttk.Style`

Un estilo se define una vez y se reutiliza:

```python
estilo = ttk.Style(self)
if "clam" in estilo.theme_names():
    estilo.theme_use("clam")

estilo.configure("Titulo.TLabel", font=("Helvetica", 17, "bold"))
estilo.configure("Subtitulo.TLabel", foreground="#555555")
estilo.configure("Error.TLabel", foreground="#b00020")
estilo.configure("Accion.TButton", font=("Helvetica", 10, "bold"), padding=(10, 6))
```

La convención `Nombre.TWidget` hereda de `TWidget` y solo cambia lo declarado. Así un error usa `style="Error.TLabel"` sin repetir el color.

Para estados se usa `style.map`:

```python
estilo.map(
    "Accion.TButton",
    background=[("active", "#2f5fa8"), ("disabled", "#9aa5b1")],
)
```

:::warning
Algunos temas ignoran ciertas opciones de color. Si un `background` no aparece, prueba con `clam`, que respeta más configuraciones. No es un error de tu código: es una limitación del tema.
:::

### Formularios: variables y estado

Un formulario conecta campos con variables de Tkinter. `StringVar` guarda el texto y permite leerlo o escribirlo sin tocar el widget:

```python
self.var_nombre = tk.StringVar()
self.var_clase = tk.StringVar(value=CLASES[0])
self.var_nivel = tk.StringVar(value="1")

ttk.Entry(marco, textvariable=self.var_nombre).grid(row=0, column=1, sticky="ew")
ttk.Combobox(
    marco, textvariable=self.var_clase, values=CLASES, state="readonly"
).grid(row=1, column=1, sticky="ew")
ttk.Spinbox(marco, from_=1, to=60, textvariable=self.var_nivel).grid(row=2, column=1)
```

`state="readonly"` impide escribir valores inventados: solo se elige de la lista. En un `Entry`, `state="disabled"` bloquea el campo; `state="normal"` lo habilita.

Las variables permiten una vista previa en vivo: `trace_add("write", ...)` ejecuta una función cuando el valor cambia:

```python
self.var_nombre.trace_add("write", lambda *_: self._actualizar_vista_previa())
```

El panel derecho se actualiza mientras se escribe, sin botón «actualizar».

### Validación visual

La validación vive en dos capas. El modelo no sabe de colores:

```python
class Personaje:
    def __init__(self, nombre: str, clase: str, nivel: int) -> None:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        if len(nombre) > 20:
            raise ValueError("El nombre admite como máximo 20 caracteres.")
        if clase not in CLASES:
            raise ValueError("Elige una clase de la lista.")
        if not 1 <= nivel <= 60:
            raise ValueError("El nivel debe estar entre 1 y 60.")
        self.nombre = nombre
        self.clase = clase
        self.nivel = nivel
```

La vista traduce el error a un mensaje visible:

```python
def _crear_personaje(self) -> None:
    try:
        nivel = int(self.var_nivel.get())
        personaje = Personaje(self.var_nombre.get(), self.var_clase.get(), nivel)
    except ValueError as error:
        self._mostrar_mensaje(str(error), exito=False)
        self.entrada_nombre.focus_set()
        return

    self.personajes.append(personaje)
    self.tabla.insert("", "end", values=personaje.fila())
    self._mostrar_mensaje(f"Personaje «{personaje.nombre}» creado.", exito=True)
```

Una validación correcta cumple cinco condiciones:

1. **Especifica el problema**: «El nivel debe estar entre 1 y 60», no «datos inválidos».
2. **Aparece cerca de la acción**: bajo el formulario o junto al campo.
3. **Usa color y texto**: el rojo solo no es accesible para personas con daltonismo.
4. **No mueve el diseño**: reserva una fila fija para el mensaje o usa `wraplength`.
5. **Devuelve el foco** al campo que hay que corregir.

:::success
El mensaje de error es parte de la interfaz. Un buen error dice qué pasó, dónde y cómo corregirlo.
:::

### Feedback y jerarquía visual

El feedback no es solo para errores: tras crear un personaje, un mensaje en verde, la fila nueva en la lista y el formulario limpio confirman la acción.

La jerarquía visual usa pocos recursos:

- **Tamaño**: título grande, datos medianos, ayuda pequeña y gris.
- **Contraste**: un solo botón principal por zona.
- **Espaciado**: escala fija de 8, 16 y 24 píxeles; el espacio separa grupos.
- **Alineación**: etiquetas a la izquierda, campos en la misma columna, números a la derecha.
- **Agrupación**: cada `LabelFrame` responde a una pregunta distinta.

Aplica estas cinco reglas y el resto es contenido.

### Listas con `Treeview`

`Treeview` muestra filas y columnas. No es una tabla de base de datos: es un widget de presentación que recibe valores.

```python
columnas = ("nombre", "clase", "nivel", "vida")
tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=6)
for columna, titulo, ancho in (
    ("nombre", "Nombre", 200),
    ("clase", "Clase", 140),
    ("nivel", "Nivel", 80),
    ("vida", "Vida", 90),
):
    tabla.heading(columna, text=titulo)
    tabla.column(columna, width=ancho)

tabla.insert("", "end", values=("Lyra", "Maga", "3", "140"))
```

`show="headings"` oculta la columna de árbol. Para que la lista crezca, su contenedor necesita `rowconfigure` y `columnconfigure` con `weight=1`; sin eso queda en su tamaño mínimo.

### Prototipo del creador

```text
┌───────────────────────────────────────────────────────────┐
│ Creador de personajes                                     │
│ Completa el formulario y revisa la vista previa.          │
├─────────────────────────────┬─────────────────────────────┤
│ Nuevo personaje             │ Vista previa                │
│ Nombre  [__________]        │  Lyra                       │
│ Clase   [Maga      ▼]       │  Clase: Maga                │
│ Nivel   [ 3 ]               │  Nivel: 3                   │
│ [Crear personaje] [Limpiar] │  Vida estimada: 116         │
├─────────────────────────────┴─────────────────────────────┤
│ Personajes creados                                        │
│ Nombre │ Clase │ Nivel │ Vida                            │
│ Lyra   │ Maga  │ 3     │ 116                             │
├───────────────────────────────────────────────────────────┤
│ ✓ Personaje «Lyra» creado.                                │
└───────────────────────────────────────────────────────────┘
```

Tres zonas, un botón principal, una lista y una franja de mensajes. Ese wireframe se traduce directo a `grid`.

## Diagrama / modelo

```text
AppCreador (tk.Tk)
├── cabecera (Frame)
├── cuerpo (Frame, 2 columnas)
│   ├── LabelFrame «Nuevo personaje»
│   │   ├── Entry nombre        ─┐
│   │   ├── Combobox clase       ├─► variables StringVar ─► vista previa
│   │   ├── Spinbox nivel       ─┘
│   │   └── Button crear / limpiar
│   └── LabelFrame «Vista previa»
├── LabelFrame «Personajes creados» ─► Treeview
└── Label mensaje (error / éxito)
```

## Errores comunes

**Mezclar `tk.Label` y `ttk.Label` en la misma zona.** Fuentes y bordes delatan la mezcla. Usa `ttk` para controles.

**Olvidar `state="readonly"` en el `Combobox`.** El usuario puede escribir una clase inexistente y la validación falla sin explicación visible. Si la lista es cerrada, bloquea la escritura.

**No reservar espacio para el mensaje.** El error aparece, empuja el diseño y todo salta. Deja una fila fija o fija `wraplength`.

**Validar dos veces con reglas distintas.** La vista comprueba una cosa y el modelo otra. Centraliza las reglas en el modelo y limita la vista a mostrar el `ValueError`.

**Usar un `messagebox` para cada error.** Los diálogos interrumpen y exigen un clic extra. Resérvalos para confirmaciones destructivas; los errores de formulario van en línea.

**No configurar `weight` en la cuadrícula.** La tabla y la vista previa quedan pequeñas aunque la ventana sea grande. `rowconfigure` y `columnconfigure` son parte del diseño.

## Buenas prácticas

- Un `LabelFrame` por grupo funcional; como máximo tres o cuatro zonas.
- Estilos con nombres semánticos: `Titulo.TLabel`, `Error.TLabel`, `Accion.TButton`.
- Una escala de espaciado fija (8/16/24) en lugar de valores improvisados.
- Etiquetas a la izquierda, campos alineados; números a la derecha.
- Mensajes de éxito y error en la misma franja, con color y texto.
- `trace_add` para vistas previas; `command` para acciones explícitas.
- `Treeview` dentro de un contenedor con `weight` y `Scrollbar` cuando haya muchas filas.
- Prueba con textos largos, listas vacías y ventanas pequeñas antes de entregar.

:::reto
Añade una pestaña «Inventario» con un `Notebook` que muestre una lista de objetos del personaje seleccionado. Si no hay selección, muestra un estado vacío claro en lugar de una tabla vacía sin explicación.
:::

## Checklist de la semana

- [ ] Usé `ttk.Label`, `ttk.Entry`, `ttk.Button` y `ttk.Combobox`.
- [ ] Creé una lista con `ttk.Treeview` y encabezados.
- [ ] Agrupé controles con `Frame` y `LabelFrame`.
- [ ] Definí al menos dos estilos propios con `ttk.Style`.
- [ ] Mi formulario valida y muestra el error junto a la acción.
- [ ] El mensaje de error no descoloca el diseño.
- [ ] Hay feedback de éxito después de crear o guardar.
- [ ] La ventana sigue viéndose bien al redimensionarla.

## Resumen

`ttk` aporta controles temáticos y consistentes: `Entry`, `Combobox`, `Spinbox`, `Treeview`, `Notebook`. Los estilos con `ttk.Style` evitan repetir colores y fuentes; los contenedores con título crean zonas comprensibles.

Un formulario profesional alinea etiquetas, valida en el modelo, muestra mensajes claros y confirma cada acción. La jerarquía visual no decora: decide si la ventana se explora o se abandona.

## Siguiente paso

La próxima semana conectamos todo con eventos: `command`, `bind`, teclado, doble clic, selección en tablas y persistencia en JSON. Con eso podrás construir la arena de combate del proyecto integrador.
