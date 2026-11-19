# Semana 14 — Eventos e integración de una aplicación OO

Unidad 3 · Semana 14

## Qué vas a aprender

- Qué es un callback y por qué `command=self._atacar` no lleva paréntesis.
- Cuándo usar `command` y cuándo usar `bind` para teclado o ratón.
- Cómo leer el objeto evento (`keysym`, `x`, `y`, `widget`).
- A conectar widgets con clases de dominio (`Personaje`, `Combate`) sin mezclar capas.
- A actualizar la interfaz desde una sola función de refresco.
- A guardar y cargar una partida con `json`, con errores visibles.
- A programar el turno enemigo con `after` sin congelar la ventana.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-14.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 arena_tkinter.py
```

Para repetir siempre el mismo combate en las pruebas:

```bash
python3 arena_tkinter.py --semilla 7
```

La partida se guarda en `ejemplo-guiado/partida_arena.json` cuando pulsas **Guardar partida**. Ese archivo se genera en tiempo de ejecución: no lo entregues ni lo subas al repositorio.

## Entregable de la semana

Una arena de combate funcional con Tkinter que:

- permita elegir nombre y clase (guerrero, mago o arquero);
- tenga un botón **Atacar** conectado a la clase `Combate`, no a la lógica escrita en el callback;
- muestre HP con etiqueta y barra, y un registro de turnos;
- responda a la tecla **A** con `bind` y permita inspeccionar al enemigo con un clic;
- guarde y cargue la partida en JSON, mostrando un error visible si el archivo no sirve;
- separe dominio, persistencia y vista en el mismo archivo o en módulos.

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
