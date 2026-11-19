# Semana 04 — Métodos, constructores y encapsulamiento

Unidad 1 · Semana 04

## Qué vas a aprender

A dar comportamiento a tus clases: métodos de instancia, constructores con valores por defecto, fábricas con `@classmethod`, utilidades con `@staticmethod` y protección del estado con atributos `_` y `__`, `@property` y setters que validan. También verás `__str__`, `__repr__` y cuándo lanzar `ValueError`.

## Archivos

| Archivo | Contenido |
|---|---|
| `semana-04.md` | Teoría completa |
| `html/slides.html` | Presentación |
| `ejemplo-guiado/` | Código ejecutable |
| `ejercicios/ejercicios.md` | Básico, intermedio y reto |
| `dudas/dudas.md` | Preguntas frecuentes |

## Cómo ejecutar

```bash
cd ejemplo-guiado
python3 combate_basico.py
python3 cuenta_bancaria.py
```

Ambos scripts usan un modo demo con datos fijos: no piden entrada ni instalan dependencias.

## Entregable de la semana

Dos scripts ejecutables:

1. `combate_basico.py` con una clase `Personaje` cuyo `hp` siempre esté entre `0` y `hp_max`. Debe incluir `atacar`, `recibir_danio`, `curar`, una fábrica `desde_ficha` con `@classmethod`, un cálculo con `@staticmethod` y representaciones `__str__` / `__repr__`.
2. `cuenta_bancaria.py` con una clase `CuentaBancaria` de saldo validado, métodos `depositar` y `retirar` que lancen `ValueError` ante montos inválidos o saldo insuficiente, e historial simple de movimientos.

## Mediación TIC

Python · Visual Studio Code · EVA/LMS · Git · repositorio de código
