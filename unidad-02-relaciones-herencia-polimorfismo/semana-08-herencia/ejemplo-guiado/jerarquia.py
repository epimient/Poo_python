"""Jerarquía de personajes: clase base, subclases, super() y sobrescritura.

Ejecutar con: python3 jerarquia.py
"""

from __future__ import annotations


class Personaje:
    """Base común: todo personaje tiene nombre, vida y un ataque básico."""

    def __init__(self, nombre: str, vida: int, ataque_base: int) -> None:
        self.nombre = nombre
        self.vida = vida
        self.ataque_base = ataque_base

    def atacar(self) -> int:
        """Ataque genérico. Las subclases pueden ampliarlo."""
        return self.ataque_base

    def recibir_dano(self, cantidad: int) -> None:
        self.vida = max(0, self.vida - cantidad)

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def __str__(self) -> str:
        return f"{self.nombre} ({self.vida} PV)"


class Guerrero(Personaje):
    """Cuerpo a cuerpo: suma su fuerza al ataque base."""

    def __init__(
        self,
        nombre: str,
        fuerza: int = 6,
        vida: int = 120,
        ataque_base: int = 10,
    ) -> None:
        super().__init__(nombre, vida, ataque_base)
        self.fuerza = fuerza

    def atacar(self) -> int:
        dano = super().atacar() + self.fuerza
        print(f"  {self.nombre} golpea con la espada: {dano} de daño")
        return dano


class Mago(Personaje):
    """A distancia: gasta maná para lanzar un hechizo."""

    def __init__(
        self,
        nombre: str,
        mana: int = 30,
        vida: int = 80,
        ataque_base: int = 6,
    ) -> None:
        super().__init__(nombre, vida, ataque_base)
        self.mana = mana

    def atacar(self) -> int:
        if self.mana >= 10:
            self.mana -= 10
            dano = super().atacar() + 15
            print(f"  {self.nombre} lanza una bola de fuego: {dano} de daño (maná {self.mana})")
        else:
            # Sin maná el ataque se debilita, pero nunca desaparece.
            dano = super().atacar() // 2
            print(f"  {self.nombre} golpea con el bastón: {dano} de daño (sin maná)")
        return dano


class Arquero(Personaje):
    """A distancia: gasta flechas y hace daño extra mientras tenga."""

    def __init__(
        self,
        nombre: str,
        flechas: int = 5,
        vida: int = 90,
        ataque_base: int = 8,
    ) -> None:
        super().__init__(nombre, vida, ataque_base)
        self.flechas = flechas

    def atacar(self) -> int:
        if self.flechas > 0:
            self.flechas -= 1
            dano = super().atacar() + 4
            print(f"  {self.nombre} dispara una flecha: {dano} de daño (quedan {self.flechas})")
        else:
            dano = super().atacar()
            print(f"  {self.nombre} golpea con el arco: {dano} de daño (sin flechas)")
        return dano


def mostrar_jerarquia() -> None:
    """Muestra el MRO y las consultas de tipo disponibles."""
    print("--- Jerarquía ---")
    for clase in (Guerrero, Mago, Arquero):
        ruta = " -> ".join(c.__name__ for c in clase.__mro__)
        print(f"MRO de {clase.__name__}: {ruta}")

    print(f"issubclass(Guerrero, Personaje) = {issubclass(Guerrero, Personaje)}")


def simular_combate(equipo: list[Personaje]) -> None:
    """Recorre la lista sin preguntar por la clase concreta de cada objeto."""
    enemigo = Personaje("Ogro de práctica", vida=60, ataque_base=0)
    ronda = 1

    while enemigo.esta_vivo() and any(p.esta_vivo() for p in equipo):
        print(f"\nRonda {ronda}")
        for personaje in equipo:
            if personaje.esta_vivo():
                enemigo.recibir_dano(personaje.atacar())

        print(f"  {enemigo} restante")

        if not enemigo.esta_vivo():
            break

        # El enemigo golpea al primer personaje que siga en pie.
        objetivo = next(p for p in equipo if p.esta_vivo())
        objetivo.recibir_dano(7)
        print(f"  El ogro golpea a {objetivo}")
        ronda += 1

    print("\n¡El equipo ganó!" if not enemigo.esta_vivo() else "\nEl equipo fue derrotado.")


def main() -> None:
    equipo: list[Personaje] = [
        Guerrero("Ragnar", fuerza=8),
        Mago("Morgana", mana=20),
        Arquero("Lyra", flechas=2),
    ]

    print("Equipo:")
    for personaje in equipo:
        print(f"  {personaje}")

    simular_combate(equipo)
    mostrar_jerarquia()

    print("\n--- Consultas de tipo ---")
    for personaje in equipo:
        es_guerrero = isinstance(personaje, Guerrero)
        es_personaje = isinstance(personaje, Personaje)
        print(f"{personaje.nombre:8} | Guerrero: {es_guerrero!s:5} | Personaje: {es_personaje}")


if __name__ == "__main__":
    main()
