"""Semana 06 — Relaciones entre clases.

Modelo del ejemplo:

    Personaje  <-- 1:1 -->  Jugador  <-- 1:N -->  Equipo

- Un jugador tiene un personaje (asociación 1:1, navegable desde el jugador).
- Un equipo tiene varios jugadores (asociación 1:N).
- Cada jugador conoce, como máximo, un equipo (navegabilidad inversa).

Ejecuta la demo con:

    python3 equipo.py

O abre un menú interactivo con:

    python3 equipo.py --interactivo
"""

from __future__ import annotations


class Personaje:
    """Ficha de juego. No sabe nada de jugadores ni de equipos."""

    def __init__(self, nombre: str, clase: str, nivel: int = 1) -> None:
        if not nombre.strip():
            raise ValueError("El personaje necesita un nombre.")
        if nivel < 1:
            raise ValueError("El nivel mínimo es 1.")
        self.nombre = nombre.strip()
        self.clase = clase.strip() or "Aventurero"
        self.nivel = nivel
        self.hp_max = self._calcular_hp()

    def _calcular_hp(self) -> int:
        return 80 + self.nivel * 12

    def subir_nivel(self, cantidad: int = 1) -> None:
        if cantidad < 1:
            raise ValueError("La cantidad de niveles debe ser positiva.")
        self.nivel += cantidad
        self.hp_max = self._calcular_hp()

    def __str__(self) -> str:
        return f"{self.nombre} ({self.clase}, nivel {self.nivel}, {self.hp_max} HP)"


class Jugador:
    """Persona real dentro del juego. Tiene un personaje y, quizá, un equipo."""

    def __init__(self, alias: str, personaje: Personaje) -> None:
        if not alias.strip():
            raise ValueError("El jugador necesita un alias.")
        self.alias = alias.strip()
        self.personaje = personaje       # asociación 1:1
        self.equipo: Equipo | None = None  # navegabilidad inversa (0..1)

    def cambiar_personaje(self, nuevo: Personaje) -> None:
        """La asociación 1:1 es reasignable: el jugador cambia de ficha."""
        self.personaje = nuevo

    def __str__(self) -> str:
        equipo = self.equipo.nombre if self.equipo else "sin equipo"
        return f"{self.alias} [{equipo}] -> {self.personaje.nombre}"


class Equipo:
    """Agrupa jugadores. No crea personajes ni jugadores: solo los referencia."""

    def __init__(self, nombre: str, maximo: int = 3) -> None:
        if maximo < 1:
            raise ValueError("Un equipo necesita al menos un cupo.")
        self.nombre = nombre.strip() or "Sin nombre"
        self.maximo = maximo
        self._jugadores: list[Jugador] = []

    @property
    def jugadores(self) -> tuple[Jugador, ...]:
        """Vista de solo lectura: evita que otros muten la lista interna."""
        return tuple(self._jugadores)

    def agregar(self, jugador: Jugador) -> None:
        if jugador in self._jugadores:
            raise ValueError(f"{jugador.alias} ya está en este equipo.")
        if jugador.equipo is not None:
            raise ValueError(
                f"{jugador.alias} ya juega en {jugador.equipo.nombre}."
            )
        if len(self._jugadores) >= self.maximo:
            raise ValueError(f"{self.nombre} está lleno ({self.maximo} cupos).")

        self._jugadores.append(jugador)
        jugador.equipo = self  # mantener ambos lados de la relación

    def retirar(self, alias: str) -> Jugador:
        for jugador in self._jugadores:
            if jugador.alias.lower() == alias.lower():
                self._jugadores.remove(jugador)
                jugador.equipo = None
                return jugador
        raise ValueError(f"No hay ningún jugador llamado {alias!r}.")

    def promedio_nivel(self) -> float:
        if not self._jugadores:
            return 0.0
        total = sum(jugador.personaje.nivel for jugador in self._jugadores)
        return total / len(self._jugadores)

    def plantilla(self) -> list[str]:
        if not self._jugadores:
            return [f"{self.nombre}: sin integrantes."]
        return [
            f"  {indice}. {jugador.alias:<6} -> {jugador.personaje}"
            for indice, jugador in enumerate(self._jugadores, start=1)
        ]

    def __len__(self) -> int:
        return len(self._jugadores)

    def __str__(self) -> str:
        return f"Equipo {self.nombre} ({len(self)}/{self.maximo})"


def construir_escenario() -> tuple[Equipo, list[Jugador]]:
    """Datos de ejemplo compartidos por la demo y el menú."""
    kael = Personaje("Kael", "Mago", nivel=7)
    runa = Personaje("Runa", "Arquera", nivel=5)
    tork = Personaje("Tork", "Tanque", nivel=9)
    nia = Personaje("Nia", "Sanadora", nivel=4)

    ana = Jugador("Ana", kael)
    beto = Jugador("Beto", runa)
    caro = Jugador("Caro", tork)
    duna = Jugador("Duna", nia)

    equipo = Equipo("Los Cometas", maximo=3)
    return equipo, [ana, beto, caro, duna]


def demo() -> None:
    equipo, (ana, beto, caro, duna) = construir_escenario()

    print("=" * 62)
    print("1) Asociación 1:N — un equipo reúne varios jugadores")
    print("=" * 62)
    equipo.agregar(ana)
    equipo.agregar(beto)
    equipo.agregar(caro)
    print(equipo)
    for linea in equipo.plantilla():
        print(linea)
    print(f"Promedio de nivel: {equipo.promedio_nivel():.1f}")

    print("\n" + "=" * 62)
    print("2) Reglas de la relación — límite de cupos y equipo único")
    print("=" * 62)
    try:
        equipo.agregar(duna)
    except ValueError as error:
        print(f"  ✗ {error}")

    equipo_rival = Equipo("Los Eclipse", maximo=2)
    try:
        equipo_rival.agregar(ana)
    except ValueError as error:
        print(f"  ✗ {error}")

    print("\n" + "=" * 62)
    print("3) Asociación 1:1 — el jugador cambia de personaje")
    print("=" * 62)
    anterior = caro.personaje
    print(f"Antes:  {caro}")
    caro.cambiar_personaje(Personaje("Tork el Viejo", "Paladín", nivel=10))
    print(f"Después: {caro}")
    print(f"El personaje anterior sigue accesible: {anterior}")
    print("Cambiar la referencia no destruye el objeto: solo lo desvincula.")

    print("\n" + "=" * 62)
    print("4) Retirar un jugador libera su cupo y su referencia al equipo")
    print("=" * 62)
    retirado = equipo.retirar("Beto")
    print(f"  Salió: {retirado.alias} (equipo = {retirado.equipo})")
    equipo.agregar(duna)
    print(equipo)
    for linea in equipo.plantilla():
        print(linea)

    print("\n" + "=" * 62)
    print("5) Recorrido en ambos sentidos de la relación")
    print("=" * 62)
    print(f"  {ana.alias} juega en {ana.equipo.nombre} con {ana.personaje.nombre}.")
    print(f"  {equipo.nombre} tiene {len(equipo)} jugadores.")


def menu() -> None:
    """Menú opcional. Solo se ejecuta con --interactivo."""
    equipo, jugadores = construir_escenario()
    equipo.agregar(jugadores[0])
    equipo.agregar(jugadores[1])

    while True:
        print("\n" + "-" * 46)
        print(equipo)
        print("1. Ver plantilla   2. Agregar jugador")
        print("3. Retirar jugador 0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("Fin del menú.")
            return
        if opcion == "1":
            for linea in equipo.plantilla():
                print(linea)
        elif opcion == "2":
            alias = input("Alias a agregar: ").strip()
            candidato = next(
                (j for j in jugadores if j.alias.lower() == alias.lower()), None
            )
            if candidato is None:
                print("✗ Ese alias no existe en el plantel de ejemplo.")
                continue
            try:
                equipo.agregar(candidato)
                print(f"✓ {candidato.alias} fichó por {equipo.nombre}.")
            except ValueError as error:
                print(f"✗ {error}")
        elif opcion == "3":
            alias = input("Alias a retirar: ").strip()
            try:
                equipo.retirar(alias)
                print(f"✓ {alias} salió del equipo.")
            except ValueError as error:
                print(f"✗ {error}")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    import sys

    if "--interactivo" in sys.argv:
        menu()
    else:
        demo()
