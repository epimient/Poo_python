# Semana 10 — Polimorfismo

Unidad 2 · Semana 10

## Qué vas a aprender

- Qué significa enviar el mismo mensaje y obtener respuestas distintas.
- Cómo construir polimorfismo con herencia, sobrescritura y clases abstractas.
- Cómo usar duck typing y `typing.Protocol` sin herencia.
- Cómo integrar tus clases con `len()`, `for`, `in`, `+` y `str()` mediante dunders.
- Cómo despachar comportamiento por tipo de dato con `functools.singledispatch`.
- Por qué una cadena de `isinstance()` es una señal de mal diseño.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-10.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 combate_turnos.py
python3 dunders_y_despacho.py
```

## Entregable de la semana

Un combate por turnos ejecutable con una clase abstracta `Personaje`, tres especialidades que sobrescriben `atacar()` y un motor `Combate` que recorre una lista sin preguntar tipos. Como cierre obligatorio, entrega el arcade **Duelo por turnos** con menú, validación, registro de turnos y revancha.

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
