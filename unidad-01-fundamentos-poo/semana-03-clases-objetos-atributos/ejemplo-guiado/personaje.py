"""Semana 03 — Clases, objetos y atributos.

Demo ejecutable: crea un equipo de personajes y muestra su estado.
No usa entrada interactiva: todos los datos están en el código.
"""

from __future__ import annotations


class Personaje:
    """Representa a un personaje jugable con estado propio."""

    MAX_HP: int = 100          # atributo de clase: regla compartida
    total_personajes: int = 0  # atributo de clase: contador global

    def __init__(self, nombre: str, hp: int = MAX_HP, nivel: int = 1) -> None:
        # Atributos de instancia: cada personaje tiene los suyos.
        self.nombre = nombre
        self.hp = hp
        self.nivel = nivel
        # El contador vive en la clase, por eso se actualiza con Personaje.
        Personaje.total_personajes += 1


def barra_hp(hp: int, max_hp: int, ancho: int = 10) -> str:
    """Devuelve una barra de vida en texto, por ejemplo [####------] 45/100."""
    proporcion = hp / max_hp if max_hp else 0
    llenos = max(0, min(ancho, round(proporcion * ancho)))
    return f"[{'#' * llenos}{'-' * (ancho - llenos)}] {hp}/{max_hp}"


def mostrar_equipo(titulo: str, equipo: list[Personaje]) -> None:
    """Imprime el estado del equipo y algunos totales."""
    print(f"\n{titulo}")
    print("-" * len(titulo))
    for personaje in equipo:
        linea = barra_hp(personaje.hp, Personaje.MAX_HP)
        print(f"{personaje.nombre:<8} Nv.{personaje.nivel:<2} {linea}")

    nivel_total = sum(personaje.nivel for personaje in equipo)
    hp_total = sum(personaje.hp for personaje in equipo)
    print(f"Nivel combinado: {nivel_total} | hp total: {hp_total}")


def main() -> None:
    print("=== Semana 03: clases, objetos y atributos ===")
    print(f"Personajes creados al inicio: {Personaje.total_personajes}")

    # Tres objetos distintos, creados a partir de la misma clase.
    aria = Personaje("Aria", hp=80, nivel=3)
    brom = Personaje("Brom", nivel=2)  # hp usa el valor por defecto
    cyd = Personaje("Cyd", hp=45, nivel=5)
    equipo = [aria, brom, cyd]

    mostrar_equipo("Equipo Alba", equipo)

    print("\nIdentidad y tipo")
    print(f"id(aria) = {id(aria)}")
    print(f"type(aria) = {type(aria).__name__}")
    print(f"isinstance(aria, Personaje) = {isinstance(aria, Personaje)}")
    print(f"aria is brom -> {aria is brom}")

    print("\nAtributos por objeto (__dict__)")
    for personaje in equipo:
        print(f"{personaje.nombre}: {personaje.__dict__}")

    print("\nAtributos de clase")
    print(f"Personaje.MAX_HP = {Personaje.MAX_HP}")
    print(f"Personaje.total_personajes = {Personaje.total_personajes}")
    print(f"'MAX_HP' en aria.__dict__? {'MAX_HP' in aria.__dict__}")

    print("\nCambiar el hp de un objeto no afecta a los demás")
    brom.hp = 95
    print(f"Brom: {brom.__dict__}")
    print(f"Aria: {aria.__dict__}")

    print("\nCuidado al asignar sobre una instancia")
    cyd.MAX_HP = 120  # crea un atributo de instancia que tapa al de clase
    print(f"cyd.MAX_HP = {cyd.MAX_HP}  -> atributo propio")
    print(f"Personaje.MAX_HP = {Personaje.MAX_HP}  -> intacto")
    print(f"'MAX_HP' en cyd.__dict__? {'MAX_HP' in cyd.__dict__}")

    print(f"\nFin de la demo. Personajes creados: {Personaje.total_personajes}")


if __name__ == "__main__":
    main()
