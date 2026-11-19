# Ejercicios — Semana 14

Tres niveles para practicar eventos e integración. Puedes partir de la arena de `ejemplo-guiado/` y recortarla, o crear tu propia ventana. Todo debe funcionar con Python 3.12 y Tkinter, sin dependencias externas.

---

## Nivel 1 — Básico: Botón de ataque y registro con `bind`

### 1.1 Un botón que llama a una clase

**Enunciado.** Crea una ventana con un `Personaje` llamado «Héroe» (100 HP, 15 de ataque) y un enemigo «Slime» (60 HP, 4 de defensa). El botón **Atacar** debe llamar a un método del personaje, no restar HP desde el callback. Muestra el HP de ambos con etiquetas y deshabilita el botón cuando el slime llegue a cero.

**Requisitos.**
- La clase `Personaje` no debe importar `tkinter`.
- `Personaje.atacar(objetivo) -> int` devuelve el daño y aplica la resta con un método `recibir_dano()`.
- El callback solo comprueba el estado, llama al dominio y actualiza las etiquetas.
- Al llegar a 0 HP, muestra «Slime derrotado» en una etiqueta de estado y deshabilita **Atacar**.
- No uses `time.sleep()`.

**Entrada esperada.**
- Abrir la ventana y pulsar **Atacar** varias veces.

**Salida esperada.**
- Cada clic reduce el HP del slime y el texto de la etiqueta cambia.
- Cuando el HP llega a 0, el botón queda deshabilitado y aparece el mensaje de victoria.
- La ventana sigue respondiendo en todo momento.

**Criterios de evaluación.**
- [ ] La lógica de daño vive en `Personaje`, no en el callback.
- [ ] El HP nunca baja de cero.
- [ ] El botón se deshabilita al terminar el combate.
- [ ] La ventana se cierra sin errores en la terminal.

---

### 1.2 Registro de batalla con `bind`

**Enunciado.** Añade a la ventana anterior un `tk.Text` de solo lectura que narre la batalla. El botón **Atacar** y la tecla **A** deben ejecutar el mismo método. La tecla **Escape** limpia el registro y reinicia el combate. Un clic sobre la etiqueta del enemigo debe añadir una línea de inspección con sus estadísticas.

**Requisitos.**
- Usa `command` para el botón y `bind("<Key>")` para el teclado; no dupliques la lógica.
- Cada ataque escribe una línea con el turno, el daño y el HP restante.
- Ignora la tecla A cuando el foco esté en un `Entry` o un `Combobox`.
- El registro debe hacer scroll automático a la última línea.
- Etiqueta cada línea con un tag distinto para jugador, enemigo y sistema.

**Entrada esperada.**
- Atacar con el botón, atacar con la tecla A y hacer clic en la etiqueta del enemigo.
- Pulsar Escape para reiniciar.

**Salida esperada.**
- El registro crece con líneas coloreadas y siempre muestra el último turno.
- Escape borra el registro y restaura los HP iniciales.
- El clic en el enemigo agrega una línea de inspección sin alterar los turnos.

**Criterios de evaluación.**
- [ ] Botón y tecla llaman exactamente al mismo método.
- [ ] La tecla A no interfiere mientras se escribe en un campo.
- [ ] El registro es de solo lectura y usa al menos tres tags.
- [ ] Escape reinicia el estado sin dejar turnos pendientes.

---

## Nivel 2 — Intermedio: Guardar y cargar la partida

**Enunciado.** Amplía tu combate con dos botones, **Guardar** y **Cargar**, que persistan la partida en `partida.json`. El archivo debe contener nombre, clase, HP actual, HP máximo, ataque, defensa, turno, si el combate terminó, el ganador y el registro de eventos. Al cargar, la ventana debe reconstruir el estado completo.

**Requisitos.**
- Serializa con `a_dict()` y reconstruye con `desde_dict()`; no uses `pickle`.
- Valida al cargar: claves obligatorias, tipos correctos y `0 <= hp <= hp_max`.
- Si el archivo no existe, muestra un aviso claro sin cerrar la aplicación.
- Si el JSON está dañado, captura la excepción y muestra el error en una etiqueta y en un `messagebox`.
- Guarda primero en un archivo temporal y reemplaza el original al final.
- El botón **Cargar** debe funcionar aunque la ventana se haya abierto sin combate activo.

**Entrada esperada.**
- Iniciar un combate, atacar dos veces, guardar, cerrar la ventana, abrir de nuevo y cargar.
- Editar el archivo a mano para romper el JSON y volver a cargar.

**Salida esperada.**
- Al cargar, aparecen el mismo turno, los mismos HP y el registro previo.
- Con un archivo dañado, la ventana sigue abierta y explica qué falló.
- Sin archivo, se informa que todavía no hay partida guardada.

**Criterios de evaluación.**
- [ ] El JSON es legible y no contiene objetos de Python.
- [ ] Cargar restaura HP, turno, ganador y registro.
- [ ] Un archivo inexistente o inválido no produce un traceback sin control.
- [ ] El guardado no deja un archivo a medias si falla la escritura.
- [ ] La carga está deshabilitada o validada cuando no hay datos coherentes.

---

## Nivel 3 — Reto: Historial de combates con `sqlite3`

**Enunciado.** Implementa un historial persistente de combates usando `sqlite3` de la biblioteca estándar. Cada vez que un combate termine, guarda una fila con fecha, nombre y clase del jugador, enemigo, resultado, turnos y daño total causado. Muestra el historial en un `ttk.Treeview` dentro de una segunda ventana o de una pestaña, con un botón **Actualizar**.

**Requisitos.**
- Crea la tabla si no existe con `CREATE TABLE IF NOT EXISTS`.
- Inserta con parámetros (`?`), nunca concatenando cadenas.
- El historial debe actualizarse al terminar el combate y al pulsar **Actualizar**.
- Si la base de datos falla, muestra el error y permite seguir jugando.
- Agrega un botón **Borrar historial** con confirmación.
- El combate debe seguir funcionando si `sqlite3` no está disponible; el historial es opcional.

**Entrada esperada.**
- Jugar tres combates con resultados distintos y abrir el historial.
- Borrar el historial y confirmar.

**Salida esperada.**
- Una tabla con una fila por combate terminado, ordenada por fecha descendente.
- El borrado pide confirmación y deja la tabla vacía sin cerrar la ventana.
- Un error de base de datos se muestra en la interfaz, no en la terminal.

**Criterios de evaluación.**
- [ ] La tabla se crea sola en la primera ejecución.
- [ ] Las inserciones usan parámetros y no sufren inyección de SQL.
- [ ] El historial muestra fecha, jugador, enemigo, resultado y turnos.
- [ ] Un fallo de base de datos no impide atacar ni guardar la partida JSON.
- [ ] El código separa la consulta a la base de datos de los widgets que la muestran.
