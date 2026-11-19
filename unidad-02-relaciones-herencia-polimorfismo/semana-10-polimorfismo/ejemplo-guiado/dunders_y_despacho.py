"""Demos complementarias de polimorfismo.

1. Dunders en un inventario (`len`, `for`, `in`, `+`, `str`).
2. Duck typing con un `Protocol`.
3. `singledispatch` para aplicar distintos tipos de daño.

Ejecuta con: python3 dunders_y_despacho.py
"""

from __future__ import annotations

from functools import singledispatch
from typing import Iterator, Protocol


class Item:
    """Objeto simple del inventario."""

    def __init__(self, nombre: str, peso: int) -> None:
        if peso < 0:
            raise ValueError("El peso no puede ser negativo")
        self.nombre = nombre
        self.peso = peso

    def __str__(self) -> str:
        return f"{self.nombre} ({self.peso} kg)"


class Inventario:
    """Colección que se comporta como un contenedor de Python."""

    def __init__(self, items: list[Item] | None = None) -> None:
        self._items = list(items or [])

    def agregar(self, item: Item) -> None:
        self._items.append(item)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Item]:
        return iter(self._items)

    def __contains__(self, nombre: object) -> bool:
        return any(item.nombre == nombre for item in self._items)

    def __add__(self, otro: "Inventario") -> "Inventario":
        if not isinstance(otro, Inventario):
            return NotImplemented
        return Inventario(self._items + otro._items)

    def __str__(self) -> str:
        if not self._items:
            return "Inventario vacío"
        contenido = ", ".join(str(item) for item in self._items)
        return f"Inventario ({len(self)} objetos): {contenido}"


class Volador(Protocol):
    """Contrato estructural: basta con saber volar."""

    def volar(self) -> str:
        ...


class Pajaro:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def volar(self) -> str:
        return f"{self.nombre} bate las alas"


class Avion:
    def __init__(self, modelo: str) -> None:
        self.modelo = modelo

    def volar(self) -> str:
        return f"El avión {self.modelo} enciende los motores"


def despegar(equipo: list[Volador]) -> None:
    """Acepta cualquier objeto que cumpla el protocolo Volador."""
    for volador in equipo:
        print(f"  {volador.volar()}")


class DanoFisico:
    def __init__(self, puntos: int) -> None:
        self.puntos = puntos


class DanoMagico:
    def __init__(self, puntos: int, escuela: str) -> None:
        self.puntos = puntos
        self.escuela = escuela


class DanoVerdadero:
    def __init__(self, puntos: int) -> None:
        self.puntos = puntos


@singledispatch
def aplicar_dano(
    dano: object, armadura: int = 0, resistencia_magica: int = 0
) -> int:
    """Calcula el daño final según el tipo del primer argumento."""
    raise TypeError(f"Tipo de daño no soportado: {type(dano).__name__}")


@aplicar_dano.register
def _(dano: DanoFisico, armadura: int = 0, resistencia_magica: int = 0) -> int:
    return max(1, dano.puntos - armadura)


@aplicar_dano.register
def _(dano: DanoMagico, armadura: int = 0, resistencia_magica: int = 0) -> int:
    return max(1, dano.puntos - resistencia_magica)


@aplicar_dano.register
def _(dano: DanoVerdadero, armadura: int = 0, resistencia_magica: int = 0) -> int:
    return max(1, dano.puntos)


def demo_inventario() -> None:
    print("== Inventario con dunders ==")
    mochila = Inventario([Item("Espada", 3), Item("Poción", 1)])
    cofre = Inventario([Item("Escudo", 4), Item("Poción", 1)])
    total = mochila + cofre  # __add__

    print(total)  # __str__
    print(f"Objetos totales: {len(total)}")  # __len__
    print("Contenido con for:")  # __iter__
    for item in total:
        print(f"  - {item}")

    print(f"¿Hay una poción? {'Poción' in total}")  # __contains__
    print(f"¿Hay un arco? {'Arco' in total}")


def demo_duck_typing() -> None:
    print("\n== Duck typing con Protocol ==")
    despegar([Pajaro("Kiwi"), Avion("Boeing 737")])


def demo_singledispatch() -> None:
    print("\n== singledispatch por tipo de daño ==")
    danos = [
        DanoFisico(18),
        DanoMagico(24, "fuego"),
        DanoVerdadero(15),
    ]
    for dano in danos:
        final = aplicar_dano(dano, armadura=6, resistencia_magica=8)
        print(f"  {type(dano).__name__:<13} -> {final} de daño final")

    try:
        aplicar_dano("fuego")
    except TypeError as error:
        print(f"  Caso no soportado -> {error}")


if __name__ == "__main__":
    demo_inventario()
    demo_duck_typing()
    demo_singledispatch()
