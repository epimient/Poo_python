"""Primer contacto con la POO: un personaje de videojuego.

Ejecutar con:
    python3 personaje.py
"""


class Personaje:
    """Representa a un personaje jugable con nombre, vida y ataque."""

    def __init__(self, nombre: str, hp: int, ataque: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque

    def presentarse(self) -> str:
        """Devuelve una presentación breve del personaje."""
        return f"Soy {self.nombre} y tengo {self.hp} HP."

    def atacar(self, objetivo: "Personaje") -> None:
        """Ataca a otro personaje y descuenta su vida."""
        dano = self.ataque
        objetivo.hp = max(0, objetivo.hp - dano)
        print(f"{self.nombre} ataca a {objetivo.nombre} y causa {dano} de daño.")
        print(f"{objetivo.nombre} queda con {objetivo.hp} HP.")

    def esta_vivo(self) -> bool:
        """Indica si al personaje le queda vida."""
        return self.hp > 0


def mostrar_estado(equipo: list[Personaje]) -> None:
    """Imprime una tabla simple con el estado del equipo."""
    print("\n--- Estado del equipo ---")
    for personaje in equipo:
        estado = "en pie" if personaje.esta_vivo() else "derrotado"
        print(f"{personaje.nombre:<8} | HP {personaje.hp:>3} | ATQ {personaje.ataque:>2} | {estado}")
    print()


def demo() -> None:
    """Crea tres personajes y simula un intercambio de ataques."""
    kaede = Personaje("Kaede", 120, 18)
    rook = Personaje("Rook", 90, 24)
    nima = Personaje("Nima", 100, 14)
    equipo = [kaede, rook, nima]

    print("=== Presentaciones ===")
    for personaje in equipo:
        print(personaje.presentarse())

    mostrar_estado(equipo)

    print("=== Ronda de combate ===")
    kaede.atacar(rook)
    rook.atacar(kaede)
    nima.atacar(rook)

    mostrar_estado(equipo)

    if not rook.esta_vivo():
        print("Rook ha caído. El equipo gana la ronda.")
    else:
        print("La ronda termina y todos siguen en pie.")


if __name__ == "__main__":
    demo()
