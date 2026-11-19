# Ejercicios formativos — Unidad 3

Quince ejercicios cortos para reforzar Tkinter, layouts, widgets, eventos, validación y separación de capas. No necesitan solución: se resuelven en clase o como práctica autónoma. Todos usan solo la biblioteca estándar.

## Fundamentos de Tkinter

### 1. Ventana con vida

Crea una ventana de 480 × 320 con el título «Mi primer juego». Dentro, un `Label` con el texto «Listo para jugar» y un botón **Comenzar** que cambie la etiqueta a «Partida iniciada». Al cerrar la ventana, el proceso debe terminar sin errores. Usa `tk.Tk`, `pack` y `command`.

### 2. Contador de pociones

Muestra un contador de pociones que empiece en 3. Cada clic en **Usar poción** resta una y actualiza la etiqueta; al llegar a cero, el botón se deshabilita y aparece «Sin pociones». Añade un botón **Reiniciar** que vuelva a 3 y reactive el botón. Comprueba que el contador no baja de cero.

## Layouts

### 3. Teclado numérico

Construye una cuadrícula de 3 × 3 con los números 1 al 9 y un botón 0 debajo. Usa `grid`, `sticky="nsew"` y `columnconfigure`/`rowconfigure` con `weight` para que los botones crezcan al redimensionar. Cada botón debe escribir su número en una etiqueta superior.

### 4. Ficha de personaje

Diseña un formulario con `pack`: nombre, clase (un `Combobox`), nivel y una etiqueta de resumen. Agrupa los campos en un `LabelFrame` y deja el botón **Guardar** al final, separado con `pady`. Al redimensionar la ventana, los campos deben mantener un ancho legible y el botón no debe quedar pegado al borde.

### 5. Panel lateral redimensionable

Divide la ventana en una barra lateral de 200 px con botones de navegación y un área central con un texto descriptivo. Usa `grid` con pesos para que el área central absorba el espacio extra. Añade un `PanedWindow` o un `Separator` para practicar otra forma de organizar la interfaz.

## Widgets

### 6. Inventario con Treeview

Crea un `ttk.Treeview` con las columnas nombre, tipo y cantidad. Agrega tres objetos de ejemplo. Con un `Entry`, un `Combobox` y un botón **Añadir**, incorpora filas nuevas. Con **Eliminar seleccionado**, borra la fila activa y muestra un aviso si no hay selección. Ordena la tabla por nombre al pulsar el encabezado.

### 7. Barra de energía

Coloca un `Scale` de 0 a 100 y un `ttk.Progressbar`. Al mover el control, la barra debe reflejar el valor y una etiqueta debe mostrar «Energía: N %». Si el valor baja de 20, cambia el texto a «Energía crítica» y deshabilita un botón **Correr**.

### 8. Menú y opciones

Añade un `Menu` con **Archivo → Salir** y **Ayuda → Acerca de** (un `messagebox`). Incluye un `Checkbutton` «Modo difícil» que escriba su estado en una etiqueta y un grupo de `Radiobutton` para elegir dificultad fácil, normal o difícil. Evita que el texto del menú y los radiobuttons se contradigan.

## Eventos

### 9. Enter para añadir, Escape para limpiar

En un formulario con un `Entry` y un botón **Añadir**, haz que `Return` agregue el texto a una lista y `Escape` limpie el campo. Usa `bind` y el objeto evento. Si el campo está vacío, no agregues nada y muestra un mensaje en una etiqueta de estado. El botón y la tecla Enter deben llamar al mismo método.

### 10. Dibujar en el canvas

Crea un `Canvas` blanco de 400 × 300. Al hacer clic con el botón izquierdo, dibuja un óvalo en la posición del cursor y muestra las coordenadas en una etiqueta. Al hacer clic con el botón derecho, borra el último óvalo. Usa `bind("<Button-1>")` y `bind("<Button-3>")`.

### 11. Mover un personaje con flechas

Dibuja un rectángulo en un `Canvas` y muévelo 10 px con las flechas del teclado. La ventana debe capturar el foco al iniciar. Si un `Entry` tiene el foco, las flechas no deben mover el personaje. Muestra la posición actual en una etiqueta y evita que el rectángulo salga del canvas.

## Validación

### 12. Alta de personaje validada

Formulario con nombre, HP máximo y ataque. Valida al pulsar **Crear**: nombre no vacío, HP entre 1 y 999, ataque entre 1 y 99. Los errores deben aparecer junto al campo correspondiente, no en la terminal. Si todo es correcto, crea un objeto `Personaje` y muestra su resumen en un `LabelFrame`. El botón **Crear** debe deshabilitarse mientras haya errores.

### 13. Cargar sin romper la aplicación

Guarda un personaje en `personaje.json` y crea un botón **Cargar**. Si el archivo no existe, muestra un aviso; si el JSON está dañado o le falta una clave, muestra el error en una etiqueta y mantén la ventana abierta. Valida que el HP esté entre 0 y el máximo antes de aceptar los datos.

## MVC e integración

### 14. Tienda separada de la vista

Modela una tienda con stock, precio y un método `comprar(cantidad)` que valide fondos y existencias. La clase `Tienda` no debe importar `tkinter`. Crea una ventana con una tabla de productos, un campo de cantidad y un botón **Comprar** que llame al dominio y refresque la tabla. Muestra los errores de negocio en una etiqueta de estado.

### 15. Arena mínima integrada

Integra `Personaje`, un botón **Atacar**, una barra de HP, un registro con `bind` para la tecla A y guardado en JSON. Separa el código en tres partes: dominio, persistencia y vista. Al terminar, comprueba que puedes probar el combate desde el intérprete sin abrir la ventana y que un archivo JSON inválido no cierra la aplicación.
