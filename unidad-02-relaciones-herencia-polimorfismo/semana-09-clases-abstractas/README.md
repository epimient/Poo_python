# Semana 09 — Clases abstractas

Unidad 2 · Semana 09

## Qué vas a aprender

- Declarar clases abstractas con `abc.ABC` y `@abstractmethod`.
- Diseñar contratos que las subclases estén obligadas a cumplir.
- Evitar instanciar bases incompletas y entender el `TypeError` de Python.
- Diferenciar clase abstracta, interfaz y `typing.Protocol`.
- Aplicar el patrón método plantilla y duck typing con `Protocol`.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-09.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 personaje_abstracto.py
python3 habilidades.py
```

## Entregable de la semana

Dos scripts:

- `personaje_abstracto.py` con una base `Personaje(ABC)`, el método abstracto `atacar()` y tres subclases que implementen el contrato. La base debe incluir un método plantilla que use `atacar()`.
- `habilidades.py` con un `Protocol` llamado `Curable`, dos clases que lo cumplan sin heredar de él y una función que acepte cualquier objeto curable.

Incluye en cada archivo una prueba que demuestre que la base (o una subclase incompleta) no se puede instanciar, y explica en un comentario breve por qué usaste `ABC` o `Protocol` en cada caso.

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
