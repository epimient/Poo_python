"""Semana 04 — Combate básico con métodos y validaciones.

Demo ejecutable: dos personajes pelean por turnos, se cura uno de ellos
y se muestran los errores que produce intentar romper las reglas.
"""

from __future__ import annotations


class Personaje:
    """Personaje con vida validada entre 0 y hp_max."""

    MAX_HP: int = 100

    def __init__(
        self,
        nombre: str,
        hp_max: int = MAX_HP,
        ataque: int = 10,
        defensa: int = 2,
    ) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if hp_max <= 0:
            raise ValueError("hp_max debe ser mayor que cero.")
        if ataque <= 0:
            raise ValueError("El ataque debe ser mayor que cero.")
        if defensa < 0:
            raise ValueError("La defensa no puede ser negativa.")

        self.nombre = nombre.strip()
        self.hp_max = hp_max
        self.ataque = ataque
        self.defensa = defensa
        self._hp = hp_max  # el estado real vive aquí

    @property
    def hp(self) -> int:
        """Vida actual. Solo se modifica a través del setter validado."""
        return self._hp

    @hp.setter
    def hp(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("El hp debe ser un número entero.")
        if not 0 <= valor <= self.hp_max:
            raise ValueError(f"El hp debe estar entre 0 y {self.hp_max}.")
        self._hp = valor

    @property
    def vivo(self) -> bool:
        """Propiedad derivada: no se guarda, se calcula."""
        return self._hp > 0

    def atacar(self, objetivo: "Personaje") -> int:
        """Ataca a otro personaje y devuelve el daño aplicado."""
        if not self.vivo:
            raise ValueError(f"{self.nombre} está derrotado y no puede atacar.")
        if not objetivo.vivo:
            raise ValueError(f"{objetivo.nombre} ya está derrotado.")

        danio = self.calcular_danio(self.ataque, objetivo.defensa)
        return objetivo.recibir_danio(danio)

    def recibir_danio(self, cantidad: int) -> int:
        """Resta vida sin bajar de cero. Devuelve el daño real recibido."""
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")
        antes = self._hp
        self.hp = max(0, self._hp - cantidad)
        return antes - self._hp

    def curar(self, cantidad: int) -> int:
        """Recupera vida sin superar hp_max. Devuelve la curación real."""
        if cantidad <= 0:
            raise ValueError("La curación debe ser mayor que cero.")
        antes = self._hp
        self.hp = min(self.hp_max, self._hp + cantidad)
        return self._hp - antes

    @classmethod
    def desde_ficha(cls, ficha: str) -> "Personaje":
        """Fábrica: crea un personaje desde 'Nombre,hp_max,ataque,defensa'."""
        partes = [parte.strip() for parte in ficha.split(",")]
        if len(partes) != 4:
            raise ValueError("La ficha debe tener 4 campos: nombre,hp_max,ataque,defensa.")
        try:
            hp_max, ataque, defensa = (int(valor) for valor in partes[1:])
        except ValueError:
            raise ValueError("Los campos numéricos de la ficha deben ser enteros.") from None
        return cls(partes[0], hp_max, ataque, defensa)

    @staticmethod
    def calcular_danio(ataque: int, defensa: int) -> int:
        """Fórmula compartida: al menos 1 de daño."""
        return max(1, ataque - defensa)

    def __str__(self) -> str:
        estado = "en pie" if self.vivo else "derrotado"
        return f"{self.nombre} ({self._hp}/{self.hp_max} hp, {estado})"

    def __repr__(self) -> str:
        return (
            f"Personaje(nombre={self.nombre!r}, hp={self._hp}, "
            f"hp_max={self.hp_max}, ataque={self.ataque}, defensa={self.defensa})"
        )


def main() -> None:
    print("=== Combate básico (Semana 04) ===")

    aria = Personaje("Aria", hp_max=90, ataque=18, defensa=4)
    brom = Personaje.desde_ficha("Brom, 120, 15, 6")
    print(f"Combatientes: {aria} vs. {brom}")

    ronda = 1
    while aria.vivo and brom.vivo and ronda <= 12:
        print(f"\n-- Ronda {ronda} --")

        danio = aria.atacar(brom)
        print(f"Aria golpea a Brom: -{danio} hp -> {brom}")
        if not brom.vivo:
            break

        danio = brom.atacar(aria)
        print(f"Brom golpea a Aria: -{danio} hp -> {aria}")

        if ronda == 3 and aria.vivo:
            curado = aria.curar(15)
            print(f"Aria usa una poción: +{curado} hp -> {aria}")

        ronda += 1

    print("\n-- Resultado --")
    print(f"Ganador: {'Aria' if aria.vivo else 'Brom'}")

    print("\n-- Validaciones --")
    for valor in (-5, 999):
        try:
            aria.hp = valor
        except ValueError as error:
            print(f"hp = {valor}: {error}")

    try:
        aria.hp = "mucho"  # type: ignore[assignment]
    except TypeError as error:
        print(f"hp = 'mucho': {error}")

    for cantidad in (0, -3):
        try:
            aria.curar(cantidad)
        except ValueError as error:
            print(f"curar({cantidad}): {error}")

    try:
        Personaje.desde_ficha("Solo, 100")
    except ValueError as error:
        print(f"ficha inválida: {error}")

    print("\n-- Representaciones --")
    print(f"str(aria): {str(aria)}")
    print(f"repr(aria): {repr(aria)}")


if __name__ == "__main__":
    main()
