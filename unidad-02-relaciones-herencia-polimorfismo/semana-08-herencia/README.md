# Semana 08 — Herencia

Unidad 2 · Semana 08

## Qué vas a aprender

- Modelar relaciones **es-un** con una clase base y varias subclases.
- Inicializar la base con `super().__init__()` y sobrescribir métodos.
- Tratar objetos de distinto tipo a través de una lista común.
- Consultar jerarquías con `isinstance()`, `issubclass()` y `__mro__`.
- Entender la herencia múltiple, el diamante y cuándo preferir composición.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-08.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 jerarquia.py
```

## Entregable de la semana

Un archivo `jerarquia.py` con una clase base y al menos tres subclases que:

- usen `super().__init__()` en su constructor;
- sobrescriban un método con una regla distinta por subclase;
- se recorran desde una lista de la clase base sin preguntar por el tipo;
- incluyan una demostración de `isinstance()` y del MRO.

Entrega también una breve nota (5–8 líneas) explicando una decisión de diseño: qué dejaste en la base, qué pusiste en cada hija y por qué.

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
