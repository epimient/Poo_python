# Ejemplo guiado — Arena de Combate

Una aplicación Tkinter completa que enfrenta a tu personaje contra un enemigo automático. El objetivo no es el juego, sino la integración: widgets que llaman a clases de dominio, eventos de teclado y ratón, una vista que se refresca sola y una partida que sobrevive al cierre en JSON.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 arena_tkinter.py
```

Con una semilla fija, para que el enemigo y los daños sean reproducibles:

```bash
python3 arena_tkinter.py --semilla 7
```

Requiere Python 3.12 y Tkinter (incluido en la instalación estándar). No usa dependencias externas. Si estás en Linux sin entorno gráfico, ejecuta `xvfb-run -a python3 arena_tkinter.py` solo para comprobar que abre; para verla necesitas una pantalla real.

## Qué hace

1. Escribes un nombre y eliges **guerrero**, **mago** o **arquero**.
2. Pulsas **Iniciar combate**; aparece un enemigo con estadísticas propias.
3. Pulsas **Atacar** (o la tecla **A**). Tu personaje golpea y, 600 ms después, el enemigo responde solo.
4. La etiqueta y la barra de HP se actualizan, y el registro narra cada turno.
5. Al terminar, puedes **Guardar partida**, **Cargar partida** o **Reiniciar**.
6. Un clic sobre el panel del enemigo muestra su inspección en el registro.

## Salida esperada

Se abre una ventana de 920 × 740 con dos paneles (tu personaje y el enemigo), los controles, el registro de batalla y una línea de estado. El registro empieza así:

```text
Turno 1
Comienza el combate: Aventurero vs Lobo espectral.
Atacas a Lobo espectral y le quitas 12 de HP.
Lobo espectral te golpea y te quita 9 de HP.
Turno 2
```

Al guardar se crea `partida_arena.json` junto al script. Al cargarlo se recuperan turno, vida, ganador y el registro completo.

## Puntos clave del código

1. **Dominio sin Tkinter.** `Personaje` y `Combate` no importan la interfaz. `Combate.turno_jugador()` y `turno_enemigo()` devuelven eventos y actualizan el estado; se pueden probar sin abrir una ventana.
2. **Callbacks delgados.** `_atacar()` comprueba el estado, llama al dominio y pinta. La regla del daño vive en `Personaje.atacar()`.
3. **`command` y `bind` al mismo método.** El botón usa `command=self._atacar`; la ventana usa `bind("<Key>")` y filtra si el foco está en un campo de texto. El clic en el enemigo usa `bind("<Button-1>")`.
4. **Una sola vista.** `_refrescar()` actualiza etiquetas y barras desde el estado. `_escribir()` colorea el registro con etiquetas de `tk.Text`.
5. **Persistencia explícita.** `a_dict()` y `desde_dict()` convierten el combate a JSON y lo validan al volver. El guardado usa un archivo temporal y `replace()` para no dejar una partida a medias.
6. **Turno automático sin bloquear.** `after(600, self._turno_enemigo)` programa la respuesta enemiga; `after_cancel()` la cancela si reinicias o cargas.

## Estructura del archivo

```text
arena_tkinter.py
├── Personaje            dominio + serialización
├── Combate              turnos, ganador, registro
├── crear_personaje()    fábrica de clases jugables
├── crear_enemigo()      IA simple con random.Random
├── guardar_partida()    JSON atómico
├── cargar_partida()     lectura + validación
└── ArenaApp             widgets, eventos y refresco
```

## Pruebas rápidas

```bash
python3 -m py_compile arena_tkinter.py
python3 arena_tkinter.py --semilla 7
```

Con la semilla 7, el mismo par de personajes produce la misma secuencia de daños en cada ejecución. Eso permite comprobar que un cambio no alteró las reglas del combate.

> `partida_arena.json` es un archivo de trabajo: se crea al guardar y no debe formar parte de la entrega ni del repositorio.
