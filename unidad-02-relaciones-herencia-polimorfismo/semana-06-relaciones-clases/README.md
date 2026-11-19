# Semana 06 — Relaciones entre clases

Unidad 2 · Semana 06

## Qué vas a aprender

- Por qué dos clases relacionadas modelan mejor que dos clases aisladas.
- Asociación, dependencia, multiplicidad y navegabilidad.
- Cómo implementar relaciones 1:1, 1:N y N:M con referencias y listas.
- Cómo leer y dibujar un diagrama UML con cardinalidades.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-06.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 equipo.py
```

Modo interactivo opcional:

```bash
python3 equipo.py --interactivo
```

## Entregable de la semana

Un script `relaciones.py` con tres clases relacionadas —por ejemplo `Jugador`, `Personaje` y `Equipo`— que:

1. Use una referencia para la relación 1:1 y una lista privada para la 1:N.
2. Valide duplicados, cupos y pertenencia a un solo equipo.
3. Mantenga coherentes los dos lados de la relación.
4. Imprima una plantilla del equipo y permita retirar integrantes.
5. Incluya un diagrama UML con cardinalidades en un comentario o en el README.

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
