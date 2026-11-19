"""Combate por turnos con polimorfismo.

Tres especialidades responden a `atacar()` a su manera. El motor `Combate`
recorre la lista y llama al mismo método sin preguntar de qué clase es cada
personaje.

Ejecuta con: python3 combate_turnos.py
"""

from __future__ import annotations

import random
from abc import ABC, abstractmethod


class Personaje(ABC):
    """Contrato común para todo combatiente."""

    def __init__(self, nombre: str, equipo: str, hp: int) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if hp <= 0:
            raise ValueError("El HP inicial debe ser positivo")
        self.nombre = nombre.strip()
        self.equipo = equipo
        self.hp_maximo = hp
        self._hp = hp

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def vivo(self) -> bool:
        return self._hp > 0

    def recibir_dano(self, cantidad: int) -> int:
        """Aplica daño y devuelve el daño real (sin bajar de cero)."""
        real = min(max(cantidad, 0), self._hp)
        self._hp -= real
        return real

    @abstractmethod
    def atacar(self, objetivo: Personaje) -> str:
        """Aplica daño al objetivo y describe la acción realizada."""

    def __str__(self) -> str:
        clase = self.__class__.__name__
        return f"{self.nombre} [{clase}] ({self.equipo}) {self._hp}/{self.hp_maximo} HP"


class Guerrero(Personaje):
    """Golpe fuerte y probabilidad de un crítico demoledor."""

    def __init__(
        self,
        nombre: str,
        equipo: str,
        hp: int = 150,
        fuerza: int = 18,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(nombre, equipo, hp)
        self.fuerza = fuerza
        self._rng = rng or random.Random()

    def atacar(self, objetivo: Personaje) -> str:
        dano = self.fuerza + self._rng.randint(0, 5)
        if self._rng.random() < 0.2:
            dano += 7
            estilo = "¡Golpe demoledor!"
        else:
            estilo = "golpe de espada"
        real = objetivo.recibir_dano(dano)
        return f"{estilo}: {real} de daño"


class Mago(Personaje):
    """Hechizo potente que consume maná; sin maná, golpea con el bastón."""

    def __init__(
        self,
        nombre: str,
        equipo: str,
        hp: int = 95,
        poder: int = 25,
        mana: int = 60,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(nombre, equipo, hp)
        self.poder = poder
        self.mana_maximo = mana
        self.mana = mana
        self.coste = 15
        self._rng = rng or random.Random()

    def atacar(self, objetivo: Personaje) -> str:
        if self.mana >= self.coste:
            self.mana -= self.coste
            dano = self.poder + self._rng.randint(0, 6)
            real = objetivo.recibir_dano(dano)
            return f"bola de fuego: {real} de daño (maná {self.mana}/{self.mana_maximo})"
        real = objetivo.recibir_dano(6 + self._rng.randint(0, 3))
        return f"golpe de bastón: {real} de daño (sin maná)"


class Arquero(Personaje):
    """Disparo con probabilidad de acierto y de crítico."""

    def __init__(
        self,
        nombre: str,
        equipo: str,
        hp: int = 115,
        destreza: int = 17,
        punteria: float = 0.78,
        critico: float = 0.25,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(nombre, equipo, hp)
        self.destreza = destreza
        self.punteria = punteria
        self.critico = critico
        self._rng = rng or random.Random()

    def atacar(self, objetivo: Personaje) -> str:
        if self._rng.random() > self.punteria:
            return "falla el disparo: 0 de daño"
        dano = self.destreza + self._rng.randint(0, 4)
        if self._rng.random() < self.critico:
            dano *= 2
            estilo = "¡CRÍTICO!"
        else:
            estilo = "flecha certera"
        real = objetivo.recibir_dano(dano)
        return f"{estilo}: {real} de daño"


class Combate:
    """Motor de turnos que solo conoce el contrato `Personaje`."""

    def __init__(self, personajes: list[Personaje], max_turnos: int = 6) -> None:
        equipos = {personaje.equipo for personaje in personajes}
        if len(equipos) < 2:
            raise ValueError("El combate necesita al menos dos equipos")
        self.personajes = personajes
        self.max_turnos = max_turnos

    def _equipos_vivos(self) -> set[str]:
        return {p.equipo for p in self.personajes if p.vivo}

    def _elegir_objetivo(self, atacante: Personaje) -> Personaje | None:
        rivales = [
            p for p in self.personajes if p.vivo and p.equipo != atacante.equipo
        ]
        if not rivales:
            return None
        # Ataca al rival más debilitado; el motor no necesita saber su clase.
        return min(rivales, key=lambda p: p.hp)

    def jugar(self) -> str | None:
        print("=== COMBATE POR TURNOS ===")
        for personaje in self.personajes:
            print(f"  {personaje}")

        for turno in range(1, self.max_turnos + 1):
            print(f"\n--- Turno {turno} ---")
            for personaje in self.personajes:
                if not personaje.vivo or len(self._equipos_vivos()) < 2:
                    continue
                objetivo = self._elegir_objetivo(personaje)
                if objetivo is None:
                    break
                # Aquí está el polimorfismo: misma llamada, respuestas distintas.
                narracion = personaje.atacar(objetivo)
                print(
                    f"{personaje.nombre:<9} -> {objetivo.nombre:<9} "
                    f"{narracion:<46} | {objetivo.nombre}: {objetivo.hp} HP"
                )
                if not objetivo.vivo:
                    print(f"          {objetivo.nombre} ha caído (KO).")

            if len(self._equipos_vivos()) < 2:
                break

        equipos = self._equipos_vivos()
        print("\n=== RESULTADO ===")
        if len(equipos) == 1:
            ganador = equipos.pop()
            print(f"Equipo ganador: {ganador}")
            return ganador

        print("La exhibición termina sin un ganador claro.")
        print("Estado final:")
        for personaje in self.personajes:
            estado = "en pie" if personaje.vivo else "KO"
            print(f"  {personaje.nombre:<9} {personaje.hp:>3} HP  ({estado})")
        return None


def crear_demo() -> list[Personaje]:
    """Datos de ejemplo reproducibles para la demostración."""
    rng = random.Random(2026)
    return [
        Guerrero("Brunilda", "Héroes", fuerza=19, rng=rng),
        Mago("Merlín", "Héroes", poder=26, rng=rng),
        Arquero("Lyra", "Héroes", destreza=18, rng=rng),
        Guerrero("Grom", "Sombras", hp=155, fuerza=18, rng=rng),
        Mago("Morgana", "Sombras", hp=90, poder=24, rng=rng),
        Arquero("Sombra", "Sombras", hp=120, destreza=17, rng=rng),
    ]


if __name__ == "__main__":
    combate = Combate(crear_demo(), max_turnos=6)
    combate.jugar()
