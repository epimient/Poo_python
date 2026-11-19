"""Semana 07 — Agregación y composición.

Dos formas de decir «todo-parte»:

- Composición (fuerte): ``Inventario`` crea y posee sus ``Item``.
  Si el inventario desaparece, sus ítems también.
- Agregación (débil): ``Equipo`` recibe ``Personaje`` ya creados.
  Si el equipo desaparece, los personajes siguen con vida.

El contador ``vivos`` de cada clase usa ``weakref.finalize`` para mostrar,
en tiempo real, cuándo un objeto deja de existir.

    python3 inventario.py
"""

from __future__ import annotations

import gc
import weakref


class Item:
    """Objeto de inventario. Solo lo crea el inventario que lo posee."""

    vivos = 0

    def __init__(self, nombre: str, tipo: str, valor: int, propietario: str) -> None:
        if not nombre.strip():
            raise ValueError("El ítem necesita un nombre.")
        if valor < 0:
            raise ValueError("El valor no puede ser negativo.")
        self.nombre = nombre.strip()
        self.tipo = tipo.strip() or "misceláneo"
        self.valor = valor
        self.propietario = propietario

        Item.vivos += 1
        self._finalizador = weakref.finalize(self, Item._al_liberar)

    @classmethod
    def _al_liberar(cls) -> None:
        cls.vivos -= 1

    def ficha(self) -> str:
        return f"{self.nombre} [{self.tipo}] · {self.valor} de oro"

    def __str__(self) -> str:
        return self.ficha()


class Inventario:
    """Composición: el contenedor crea, administra y destruye sus ítems."""

    def __init__(self, dueno: str, capacidad: int = 6) -> None:
        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1.")
        self.dueno = dueno.strip() or "Aventurero"
        self.capacidad = capacidad
        self._items: list[Item] = []

    def crear_item(self, nombre: str, tipo: str, valor: int) -> None:
        """El ítem nace dentro del inventario; nadie más lo crea por él."""
        if len(self._items) >= self.capacidad:
            raise ValueError(f"El inventario de {self.dueno} está lleno.")
        if self.obtener(nombre) is not None:
            raise ValueError(f"Ya existe un ítem llamado {nombre!r}.")

        item = Item(nombre, tipo, valor, propietario=self.dueno)
        self._items.append(item)

    def obtener(self, nombre: str) -> Item | None:
        """Referencia de consulta. No la guardes: el dueño es el inventario."""
        for item in self._items:
            if item.nombre.lower() == nombre.lower():
                return item
        return None

    def consumir(self, nombre: str) -> str:
        """Usar un consumible lo saca del inventario y lo deja morir."""
        item = self.obtener(nombre)
        if item is None:
            raise ValueError(f"No hay ningún ítem llamado {nombre!r}.")
        self._items.remove(item)
        return f"Se consumió {item.nombre} (+{item.valor} de efecto)."

    def total_valor(self) -> int:
        return sum(item.valor for item in self._items)

    def fichas(self) -> list[str]:
        """Devuelve texto, no objetos: así no se filtran referencias internas."""
        if not self._items:
            return [f"Inventario de {self.dueno}: vacío."]
        return [f"  - {item.ficha()}" for item in self._items]

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"Inventario de {self.dueno} ({len(self)}/{self.capacidad})"


class Personaje:
    """Entidad independiente. Existe antes y después de cualquier equipo."""

    vivos = 0

    def __init__(self, nombre: str, clase: str, nivel: int = 1) -> None:
        if not nombre.strip():
            raise ValueError("El personaje necesita un nombre.")
        self.nombre = nombre.strip()
        self.clase = clase.strip() or "Aventurero"
        self.nivel = max(1, nivel)

        Personaje.vivos += 1
        self._finalizador = weakref.finalize(self, Personaje._al_liberar)

    @classmethod
    def _al_liberar(cls) -> None:
        cls.vivos -= 1

    def estado(self) -> str:
        return f"{self.nombre} ({self.clase}, nivel {self.nivel}) sigue disponible."


class Equipo:
    """Agregación: referencia personajes existentes y no los destruye."""

    def __init__(self, nombre: str, maximo: int = 3) -> None:
        self.nombre = nombre.strip() or "Sin nombre"
        self.maximo = maximo
        self._integrantes: list[Personaje] = []

    def reclutar(self, personaje: Personaje) -> None:
        if personaje in self._integrantes:
            raise ValueError(f"{personaje.nombre} ya está en {self.nombre}.")
        if len(self._integrantes) >= self.maximo:
            raise ValueError(f"{self.nombre} no tiene cupos libres.")
        self._integrantes.append(personaje)

    def retirar(self, nombre: str) -> Personaje | None:
        for personaje in self._integrantes:
            if personaje.nombre.lower() == nombre.lower():
                self._integrantes.remove(personaje)
                return personaje
        return None

    def poder_total(self) -> int:
        return sum(personaje.nivel * 10 for personaje in self._integrantes)

    def fichas(self) -> list[str]:
        if not self._integrantes:
            return [f"{self.nombre}: sin integrantes."]
        return [
            f"  {indice}. {personaje.estado()}"
            for indice, personaje in enumerate(self._integrantes, start=1)
        ]

    def __len__(self) -> int:
        return len(self._integrantes)

    def __str__(self) -> str:
        return f"Equipo {self.nombre} ({len(self)}/{self.maximo})"


def demo_composicion() -> None:
    print("=" * 64)
    print("COMPOSICIÓN — el inventario es dueño de sus ítems")
    print("=" * 64)
    inventario = Inventario("Kael", capacidad=4)
    inventario.crear_item("Espada corta", "arma", 120)
    inventario.crear_item("Poción de vida", "consumible", 40)
    inventario.crear_item("Amuleto de suerte", "accesorio", 90)

    print(inventario)
    for linea in inventario.fichas():
        print(linea)
    print(f"Valor total: {inventario.total_valor()} de oro")
    print(f"Ítems vivos en memoria: {Item.vivos}")

    print("\nUsar la poción:")
    print(f"  {inventario.consumir('Poción de vida')}")
    gc.collect()
    print(f"  Ítems vivos ahora: {Item.vivos}  (el consumido desapareció)")

    print("\nEliminar el contenedor completo:")
    del inventario
    gc.collect()
    print(f"  Ítems vivos ahora: {Item.vivos}  (murieron con su dueño)")


def demo_fuga() -> None:
    print("\n" + "=" * 64)
    print("ERROR DE OWNERSHIP — guardar una referencia interna")
    print("=" * 64)
    inventario = Inventario("Duna", capacidad=2)
    inventario.crear_item("Mapa antiguo", "objeto de misión", 0)

    mapa = inventario.obtener("Mapa antiguo")  # referencia externa indebida
    del inventario
    gc.collect()
    print(f"Tras borrar el inventario, ítems vivos: {Item.vivos}")
    print("El ítem sigue existiendo porque alguien más lo referencia:")
    print(f"  {mapa}")

    mapa = None  # renunciar a la referencia
    gc.collect()
    print(f"Al soltar la última referencia, ítems vivos: {Item.vivos}")


def demo_agregacion() -> None:
    print("\n" + "=" * 64)
    print("AGREGACIÓN — el equipo usa personajes que ya existían")
    print("=" * 64)
    kael = Personaje("Kael", "Mago", nivel=7)
    runa = Personaje("Runa", "Arquera", nivel=5)
    tork = Personaje("Tork", "Tanque", nivel=9)

    equipo = Equipo("Los Cometas", maximo=2)
    equipo.reclutar(kael)
    equipo.reclutar(runa)
    print(equipo)
    for linea in equipo.fichas():
        print(linea)
    print(f"Poder total: {equipo.poder_total()}")
    print(f"Personajes vivos antes de borrar el equipo: {Personaje.vivos}")

    try:
        equipo.reclutar(tork)
    except ValueError as error:
        print(f"  ✗ {error}")

    del equipo
    gc.collect()
    print(f"\nEquipo eliminado. Personajes vivos: {Personaje.vivos}")
    print("Ninguno murió: el equipo solo los agregaba.")
    print(f"  {kael.estado()}")
    print(f"  {tork.estado()}  (nunca estuvo en el equipo)")


def main() -> None:
    demo_composicion()
    demo_fuga()
    demo_agregacion()
    print("\n" + "=" * 64)
    print("Resumen: composición = dueño único; agregación = préstamo.")
    print("=" * 64)


if __name__ == "__main__":
    main()
