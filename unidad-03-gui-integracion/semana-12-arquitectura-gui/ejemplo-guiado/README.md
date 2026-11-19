# Ejemplo guiado — Semana 12

Dos ventanas para entender la arquitectura antes de llenar la pantalla de widgets.

## Qué construye

| Archivo | Qué muestra |
|---|---|
| `hola_tkinter.py` | Ventana mínima con `Label`, `Entry`, `Button` y un callback que actualiza el saludo. |
| `ficha_personaje.py` | Ficha de un personaje con el modelo `Personaje` separado de la vista `VistaFicha`. |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 hola_tkinter.py
python3 ficha_personaje.py
```

Para cerrar cualquiera de las dos ventanas usa la **X** de la barra de título, **Alt+F4** o **Ctrl+C** en la terminal.

## Salida esperada

**`hola_tkinter.py`** abre una ventana de 380 × 230 con un título, un campo de texto, un botón «Saludar» y un contador. Al escribir un nombre y pulsar el botón —o presionar Enter dentro del campo— el saludo cambia y el contador aumenta.

**`ficha_personaje.py`** abre una ventana con el nombre del personaje, su clase, nivel, vida y estado. El botón «Subir de nivel» incrementa el nivel, recalcula la vida máxima y actualiza todos los valores de la vista.

## Puntos clave

1. **Una sola ventana raíz.** `tk.Tk()` se crea una vez en `main()` y `mainloop()` queda al final. Sin `mainloop()` la ventana aparece y el programa termina.
2. **Jerarquía clara.** En `hola_tkinter.py` los widgets cuelgan de la ventana; en `ficha_personaje.py` la vista es un `Frame` que contiene etiquetas y un botón.
3. **Geometrías distintas.** El saludo usa `pack`; la ficha usa `grid` con `sticky="w"` para alinear etiquetas y valores. Cada contenedor usa un solo gestor.
4. **Modelo sin Tkinter.** `Personaje` no importa `tkinter`: calcula nivel, vida y estado por su cuenta. Esa es la prueba de que la lógica está separada.
5. **Callback en tres pasos.** `_subir_nivel()` llama al modelo, actualiza la vista y no contiene reglas del juego duplicadas.

## Si no hay entorno gráfico

En un servidor sin pantalla, Tkinter lanza `TclError: no display name and no $DISPLAY environment variable`. En ese caso verifica sintaxis e importación:

```bash
python3 -m py_compile hola_tkinter.py ficha_personaje.py
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

La ventana solo puede probarse en una sesión con escritorio (Linux, Windows o macOS).
