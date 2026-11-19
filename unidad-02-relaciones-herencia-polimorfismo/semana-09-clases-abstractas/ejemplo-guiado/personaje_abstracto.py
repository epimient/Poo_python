"""Clase abstracta Personaje: contrato obligatorio y método plantilla.

Ejecutar con: python3 personaje_abstracto.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Personaje(ABC):
    """Base abstracta: no se puede instanciar mientras atacar() sea abstracto."""

    def __init__(self, nombre: str, vida: int, ataque_base: int) -> None:
        self.nombre = nombre
        self.vida = vida
        self.ataque_base = ataque_base

    @abstractmethod
    def atacar(self) -> int:
        """Devuelve el daño del ataque. Cada subclase concreta lo implementa."""

    def recibir_dano(self, cantidad: int) -> None:
        self.vida = max(0, self.vida - cantidad)

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def realizar_turno(self, enemigo: Personaje) -> int:
        """Método plantilla: el paso variable es atacar(); el resto es fijo."""
        dano = self.atacar()
        enemigo.recibir_dano(dano)
        return dano

    def __str__(self) -> str:
        return f"{self.nombre} ({self.vida} PV)"


class Guerrero(Personaje):
    """Ataca cuerpo a cuerpo y suma su fuerza al daño base."""

    def __init__(self, nombre: str, fuerza: int = 6, vida: int = 120) -> None:
        super().__init__(nombre, vida, ataque_base=10)
        self.fuerza = fuerza

    def atacar(self) -> int:
        return self.ataque_base + self.fuerza


class Mago(Personaje):
    """Gasta maná para lanzar un hechizo; sin maná, ataca con el bastón."""

    def __init__(self, nombre: str, mana: int = 30, vida: int = 80) -> None:
        super().__init__(nombre, vida, ataque_base=6)
        self.mana = mana

    def atacar(self) -> int:
        if self.mana >= 10:
            self.mana -= 10
            return self.ataque_base + 15
        return self.ataque_base // 2

    def __str__(self) -> str:
        return f"{self.nombre} ({self.vida} PV, maná {self.mana})"


class Arquero(Personaje):
    """Gasta flechas para hacer daño extra; sin flechas, golpea con el arco."""

    def __init__(self, nombre: str, flechas: int = 5, vida: int = 90) -> None:
        super().__init__(nombre, vida, ataque_base=8)
        self.flechas = flechas

    def atacar(self) -> int:
        if self.flechas > 0:
            self.flechas -= 1
            return self.ataque_base + 4
        return self.ataque_base

    def __str__(self) -> str:
        return f"{self.nombre} ({self.vida} PV, flechas {self.flechas})"


class Ogro(Personaje):
    """Enemigo simple: implementa el contrato con el ataque base."""

    def __init__(self, nombre: str = "Ogro", vida: int = 100) -> None:
        super().__init__(nombre, vida, ataque_base=9)

    def atacar(self) -> int:
        return self.ataque_base


def demostrar_contrato() -> None:
    """Muestra que la base y una subclase incompleta no se instancian."""
    print("--- Contrato abstracto ---")
    try:
        Personaje("Genérico", 100, 5)  # type: ignore[abstract]
    except TypeError as error:
        print("Personaje no se puede instanciar:")
        print(f"  {error}")

    class PersonajeIncompleto(Personaje):
        """No implementa atacar(): sigue siendo abstracta."""

    try:
        PersonajeIncompleto("Incompleto", 50, 5)  # type: ignore[abstract]
    except TypeError as error:
        print("\nUna subclase sin atacar() tampoco se instancia:")
        print(f"  {error}")

    print(f"\nMétodos abstractos pendientes: {Personaje.__abstractmethods__}")


def main() -> None:
    demostrar_contrato()

    equipo: list[Personaje] = [
        Guerrero("Ragnar", fuerza=8),
        Mago("Morgana", mana=20),
        Arquero("Lyra", flechas=2),
    ]
    ogro = Ogro("Ogro de práctica", vida=90)

    print("\n--- Combate usando el método plantilla ---")
    for personaje in equipo:
        dano = personaje.realizar_turno(ogro)
        print(f"{personaje.nombre} causa {dano} de daño. {ogro} restante")
        print(f"  Estado: {personaje}")

    if ogro.esta_vivo():
        objetivo = equipo[0]
        dano = ogro.realizar_turno(objetivo)
        print(f"\nEl ogro contraataca a {objetivo.nombre}: {dano} de daño")
        print(f"  Estado: {objetivo}")

    print("\n--- Consultas de tipo ---")
    print(f"isinstance(Ragnar, Personaje): {isinstance(equipo[0], Personaje)}")
    print(f"issubclass(Guerrero, Personaje): {issubclass(Guerrero, Personaje)}")
    print(f"¿Queda algún método abstracto en Guerrero? {Guerrero.__abstractmethods__ or 'ninguno'}")


if __name__ == "__main__":
    main()
