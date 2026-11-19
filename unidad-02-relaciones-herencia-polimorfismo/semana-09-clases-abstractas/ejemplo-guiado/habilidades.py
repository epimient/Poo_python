"""Protocol Curable: contrato por forma, sin herencia obligatoria.

Ejecutar con: python3 habilidades.py
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Curable(Protocol):
    """Cualquier objeto con estos miembros puede recibir curación."""

    nombre: str
    vida: int
    vida_maxima: int

    def curar(self, cantidad: int) -> int:
        """Recupera hasta `cantidad` PV y devuelve lo curado realmente."""
        ...


class Aldeano:
    """Implementa el contrato sin heredar de Curable."""

    def __init__(self, nombre: str, vida: int, vida_maxima: int) -> None:
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida_maxima

    def curar(self, cantidad: int) -> int:
        if cantidad <= 0:
            return 0
        curado = min(cantidad, self.vida_maxima - self.vida)
        self.vida += curado
        return curado

    def __str__(self) -> str:
        return f"{self.nombre} ({self.vida}/{self.vida_maxima} PV)"


class Mascota:
    """Otra clase independiente que también cumple la forma del protocolo."""

    def __init__(self, nombre: str, vida: int, vida_maxima: int) -> None:
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida_maxima

    def curar(self, cantidad: int) -> int:
        if cantidad <= 0:
            return 0
        curado = min(cantidad, self.vida_maxima - self.vida)
        self.vida += curado
        return curado

    def __str__(self) -> str:
        return f"{self.nombre} ({self.vida}/{self.vida_maxima} PV)"


class Piedra:
    """No tiene curar(): no cumple el contrato."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.dureza = 100


def curar_aliado(objetivo: Curable, cantidad: int) -> int:
    """Cura a cualquier objeto que cumpla Curable; devuelve lo curado."""
    if not isinstance(objetivo, Curable):
        print(f"{objetivo.nombre} no se puede curar: no cumple el contrato")
        return 0

    curado = objetivo.curar(cantidad)
    print(f"{objetivo.nombre} recupera {curado} PV ({objetivo.vida}/{objetivo.vida_maxima})")
    return curado


def curar_equipo(objetivos: list[Curable], cantidad: int) -> int:
    """Acepta objetos de clases distintas; solo importa que sean curables."""
    total = 0
    for objetivo in objetivos:
        total += curar_aliado(objetivo, cantidad)
    return total


def main() -> None:
    print("--- Protocolo Curable ---")
    aliados: list[Curable] = [
        Aldeano("Ragnar", vida=40, vida_maxima=120),
        Mascota("Fénix", vida=10, vida_maxima=30),
    ]

    total = curar_equipo(aliados, cantidad=25)
    print(f"Total curado en el primer turno: {total} PV")

    print("\n--- Segunda curación ---")
    curar_equipo(aliados, cantidad=25)

    print("\n--- Un objeto que no cumple el contrato ---")
    piedra = Piedra("Roca")
    print(f"¿Roca es Curable? {isinstance(piedra, Curable)}")
    curar_aliado(piedra, cantidad=10)  # type: ignore[arg-type]

    print("\n--- Sin herencia de por medio ---")
    print(f"¿Aldeano hereda de Curable? {Curable in Aldeano.__mro__}")
    print(f"¿Mascota hereda de Curable? {Curable in Mascota.__mro__}")
    print("Ambas cumplen el contrato por su forma, no por su árbol genealógico.")


if __name__ == "__main__":
    main()
