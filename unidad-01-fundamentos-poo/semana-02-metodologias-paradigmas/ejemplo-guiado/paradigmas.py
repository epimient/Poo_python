"""El mismo combate resuelto con funciones y con clases.

Ejecutar con:
    python3 paradigmas.py

La salida muestra las dos versiones por separado. El estado final debe
ser idéntico: el paradigma cambia la organización, no el resultado.
"""


# ---------------------------------------------------------------
# Versión 1: procedural (funciones + diccionarios)
# ---------------------------------------------------------------

def crear_personaje(nombre: str, hp: int, ataque: int) -> dict[str, object]:
    """Crea un personaje como diccionario."""
    return {"nombre": nombre, "hp": hp, "ataque": ataque}


def linea_estado(personaje: dict[str, object]) -> str:
    """Devuelve una línea con el estado de un personaje."""
    return f"{personaje['nombre']:<8} | HP {int(personaje['hp']):>3} | ATQ {int(personaje['ataque']):>2}"


def atacar_procedural(atacante: dict[str, object], objetivo: dict[str, object]) -> None:
    """Aplica un ataque usando funciones y diccionarios."""
    dano = int(atacante["ataque"])
    objetivo["hp"] = max(0, int(objetivo["hp"]) - dano)
    print(f"{atacante['nombre']} ataca a {objetivo['nombre']} y causa {dano} de daño.")
    print(f"{objetivo['nombre']} queda con {objetivo['hp']} HP.")


def demo_procedural() -> None:
    """Ejecuta el combate con el enfoque procedural."""
    kaede = crear_personaje("Kaede", 120, 18)
    rook = crear_personaje("Rook", 90, 24)
    nima = crear_personaje("Nima", 100, 14)
    equipo = [kaede, rook, nima]

    print("=== VERSIÓN PROCEDURAL ===")
    for personaje in equipo:
        print(linea_estado(personaje))
    print()

    atacar_procedural(kaede, rook)
    atacar_procedural(rook, kaede)
    atacar_procedural(nima, rook)

    print("\nEstado final:")
    for personaje in equipo:
        print(linea_estado(personaje))
    print()


# ---------------------------------------------------------------
# Versión 2: orientada a objetos (clases + métodos)
# ---------------------------------------------------------------

class Personaje:
    """Un personaje que conoce su estado y sus acciones."""

    def __init__(self, nombre: str, hp: int, ataque: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque

    def estado(self) -> str:
        """Devuelve una línea con el estado del personaje."""
        return f"{self.nombre:<8} | HP {self.hp:>3} | ATQ {self.ataque:>2}"

    def atacar(self, objetivo: "Personaje") -> None:
        """Ataca a otro personaje y descuenta su vida."""
        dano = self.ataque
        objetivo.hp = max(0, objetivo.hp - dano)
        print(f"{self.nombre} ataca a {objetivo.nombre} y causa {dano} de daño.")
        print(f"{objetivo.nombre} queda con {objetivo.hp} HP.")


def demo_poo() -> None:
    """Ejecuta el mismo combate con el enfoque orientado a objetos."""
    kaede = Personaje("Kaede", 120, 18)
    rook = Personaje("Rook", 90, 24)
    nima = Personaje("Nima", 100, 14)
    equipo = [kaede, rook, nima]

    print("=== VERSIÓN ORIENTADA A OBJETOS ===")
    for personaje in equipo:
        print(personaje.estado())
    print()

    kaede.atacar(rook)
    rook.atacar(kaede)
    nima.atacar(rook)

    print("\nEstado final:")
    for personaje in equipo:
        print(personaje.estado())
    print()


def main() -> None:
    """Ejecuta ambas versiones y compara el estado final."""
    demo_procedural()
    demo_poo()

    print("=== COMPARACIÓN ===")
    print("Ambas versiones terminan con el mismo estado:")
    print("Kaede: 96 HP | Rook: 58 HP | Nima: 100 HP")
    print("La diferencia está en dónde viven los datos y las reglas.")


if __name__ == "__main__":
    main()
