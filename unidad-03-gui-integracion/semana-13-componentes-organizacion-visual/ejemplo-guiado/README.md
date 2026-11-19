# Ejemplo guiado — Semana 13

Dos aplicaciones con widgets `ttk`, estilos, formularios y validación visual.

## Qué construye

| Archivo | Qué muestra |
|---|---|
| `creador_personaje.py` | Formulario con nombre, clase y nivel; validación, vista previa en vivo y lista con `Treeview`. |
| `cajero_basico.py` | Formulario bancario con titular, apertura de cuenta, depósitos, retiros e historial. |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 creador_personaje.py
python3 cajero_basico.py
```

## Salida esperada

**`creador_personaje.py`** abre una ventana con dos columnas: a la izquierda el formulario, a la derecha la vista previa. Mientras escribes, la vista previa cambia. Al pulsar «Crear personaje»:

- Si el nombre está vacío, el nivel no es numérico o está fuera de 1–60, aparece un mensaje rojo y no se agrega nada.
- Si todo es válido, el personaje aparece en la tabla, el mensaje se vuelve verde y el formulario se limpia.

**`cajero_basico.py`** comienza con las operaciones bloqueadas. Escribe un titular y pulsa «Abrir cuenta»: el saldo se activa y los botones se habilitan. Deposita `150.50`, retira `50` y observa el saldo y el historial. Prueba un retiro mayor al saldo o un monto vacío para ver la validación.

## Puntos clave

1. **Widgets temáticos.** Los controles son `ttk`; los estilos se definen una vez con `ttk.Style` (`Titulo.TLabel`, `Error.TLabel`, `Accion.TButton`) y se reutilizan.
2. **Variables de Tkinter.** `StringVar` conecta el formulario con el código. `trace_add("write", ...)` refresca la vista previa sin botón adicional.
3. **Validación en el modelo.** `Personaje` y `CuentaBancaria` lanzan `ValueError`; la vista captura el error y lo muestra en una franja fija. Las reglas no están duplicadas en los botones.
4. **Feedback inmediato.** Cada acción produce un mensaje con color y texto; el éxito también limpia el formulario o actualiza el saldo.
5. **Listas y estados.** `Treeview` muestra los registros y las operaciones; `state="disabled"` bloquea el formulario bancario hasta que exista una cuenta.

## Si no hay entorno gráfico

En un servidor sin pantalla, Tkinter lanza `TclError: no display name and no $DISPLAY environment variable`. Verifica sintaxis e importación:

```bash
python3 -m py_compile creador_personaje.py cajero_basico.py
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

La interfaz debe probarse en una sesión con escritorio (Linux, Windows o macOS).
