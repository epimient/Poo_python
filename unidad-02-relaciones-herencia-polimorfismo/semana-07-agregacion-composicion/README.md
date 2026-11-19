# Semana 07 — Agregación y composición

Unidad 2 · Semana 07

## Qué vas a aprender

- Qué es una relación todo-parte y por qué no toda asociación lo es.
- La diferencia entre agregación (débil) y composición (fuerte).
- Cómo el ciclo de vida de las partes depende —o no— del contenedor.
- Cómo implementar ambas relaciones en Python sin frameworks.
- Qué errores de ownership aparecen al compartir o filtrar referencias.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-07.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 inventario.py
```

## Entregable de la semana

Un script `todo_parte.py` con dos contenedores:

1. Uno por **composición**: crea y posee sus partes (por ejemplo `Mochila` e `Item`).
2. Uno por **agregación**: recibe partes ya creadas y no las destruye (por ejemplo `Equipo` y `Personaje`).
3. Una demo que elimine ambos contenedores y muestre qué objetos sobreviven.
4. Validaciones de capacidad, duplicados y pertenencia.
5. Comentarios o README con el diagrama UML (rombos hueco y relleno).

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
