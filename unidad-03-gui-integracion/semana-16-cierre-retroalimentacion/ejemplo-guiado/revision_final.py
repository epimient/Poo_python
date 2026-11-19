"""revision_final.py — Revisor de código orientado a objetos.

Analiza un fragmento de Python y reporta señales básicas de calidad:
docstrings, encapsulamiento, tamaño de los métodos, `print` dentro de la
lógica y type hints. Usa `ast` de la biblioteca estándar de forma sencilla:
recorre el árbol, cuenta líneas y busca llamadas, sin análisis profundo.

Ejecuta:
    python3 revision_final.py
"""

from __future__ import annotations

import ast
from typing import Iterable

SEVERIDADES = ("alta", "media", "baja")
PRIORIDAD = {severidad: indice for indice, severidad in enumerate(SEVERIDADES)}


class Hallazgo:
    """Un problema concreto detectado en una línea del código."""

    __slots__ = ("regla", "linea", "detalle", "severidad")

    def __init__(
        self,
        regla: str,
        linea: int,
        detalle: str,
        severidad: str = "media",
    ) -> None:
        if severidad not in SEVERIDADES:
            raise ValueError(f"Severidad no válida: {severidad}")
        self.regla = regla
        self.linea = linea
        self.detalle = detalle
        self.severidad = severidad

    def __str__(self) -> str:
        return f"L{self.linea:>3}  [{self.severidad.upper():<6}] {self.regla}: {self.detalle}"


class Regla:
    """Contrato que cumple toda regla de revisión."""

    nombre = "Regla genérica"
    severidad = "media"

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        """Devuelve los hallazgos encontrados en el árbol sintáctico."""
        raise NotImplementedError("Cada regla debe implementar revisar()")

    def _crear(self, nodo: ast.AST, detalle: str) -> Hallazgo:
        """Construye un hallazgo con los datos de la regla actual."""
        linea = getattr(nodo, "lineno", 0)
        return Hallazgo(self.nombre, linea, detalle, self.severidad)


class DocstringDeClase(Regla):
    """Toda clase debe explicar para qué existe."""

    nombre = "Docstring de clase"
    severidad = "media"

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        hallazgos: list[Hallazgo] = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ClassDef) and not ast.get_docstring(nodo):
                hallazgos.append(
                    self._crear(nodo, f"la clase '{nodo.name}' no tiene docstring")
                )
        return hallazgos


class AtributosPublicos(Regla):
    """Los datos internos se guardan como atributos protegidos."""

    nombre = "Encapsulamiento"
    severidad = "alta"

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        hallazgos: list[Hallazgo] = []
        for clase in ast.walk(arbol):
            if not isinstance(clase, ast.ClassDef):
                continue
            vistos: set[str] = set()
            for metodo in clase.body:
                if not isinstance(metodo, ast.FunctionDef):
                    continue
                if metodo.name != "__init__":
                    continue
                for nodo in ast.walk(metodo):
                    if not isinstance(nodo, ast.Attribute):
                        continue
                    if not isinstance(nodo.ctx, ast.Store):
                        continue
                    if not isinstance(nodo.value, ast.Name) or nodo.value.id != "self":
                        continue
                    if nodo.attr.startswith("_") or nodo.attr in vistos:
                        continue
                    vistos.add(nodo.attr)
                    hallazgos.append(
                        self._crear(
                            nodo,
                            f"atributo público 'self.{nodo.attr}' en '{clase.name}'",
                        )
                    )
        return hallazgos


class MetodoLargo(Regla):
    """Un método que no cabe en una pantalla es difícil de revisar."""

    nombre = "Método largo"
    severidad = "media"
    LIMITE = 12

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        hallazgos: list[Hallazgo] = []
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            fin = getattr(nodo, "end_lineno", nodo.lineno)
            lineas = fin - nodo.lineno + 1
            if lineas > self.LIMITE:
                hallazgos.append(
                    self._crear(
                        nodo,
                        f"'{nodo.name}' ocupa {lineas} líneas (límite {self.LIMITE})",
                    )
                )
        return hallazgos


class PrintEnLogica(Regla):
    """La lógica no debería escribir en la consola."""

    nombre = "print en lógica"
    severidad = "alta"
    EXENTOS = {"__str__", "mostrar", "imprimir", "main"}

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        hallazgos: list[Hallazgo] = []
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, ast.FunctionDef):
                continue
            if nodo.name in self.EXENTOS:
                continue
            for interno in ast.walk(nodo):
                if not isinstance(interno, ast.Call):
                    continue
                if not isinstance(interno.func, ast.Name):
                    continue
                if interno.func.id == "print":
                    hallazgos.append(
                        self._crear(interno, f"'print' dentro de '{nodo.name}'")
                    )
        return hallazgos


class FaltaTypeHints(Regla):
    """Las firmas deben decir qué entra y qué sale."""

    nombre = "Type hints"
    severidad = "baja"

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        hallazgos: list[Hallazgo] = []
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, ast.FunctionDef):
                continue
            sin_anotacion = [
                argumento.arg
                for argumento in nodo.args.args
                if argumento.arg not in {"self", "cls"}
                and argumento.annotation is None
            ]
            if sin_anotacion:
                hallazgos.append(
                    self._crear(
                        nodo,
                        f"'{nodo.name}' sin anotación en: {', '.join(sin_anotacion)}",
                    )
                )
            if nodo.returns is None:
                hallazgos.append(
                    self._crear(nodo, f"'{nodo.name}' sin tipo de retorno")
                )
        return hallazgos


class Informe:
    """Resultado ordenado de una revisión, con veredicto legible."""

    def __init__(self, hallazgos: list[Hallazgo], reglas_aplicadas: int) -> None:
        self._hallazgos = self._limpiar_y_ordenar(hallazgos)
        self._reglas_aplicadas = reglas_aplicadas

    @property
    def total(self) -> int:
        return len(self._hallazgos)

    @property
    def por_severidad(self) -> dict[str, int]:
        conteo = {severidad: 0 for severidad in SEVERIDADES}
        for hallazgo in self._hallazgos:
            conteo[hallazgo.severidad] += 1
        return conteo

    @property
    def veredicto(self) -> str:
        if self.por_severidad["alta"] > 0:
            return "Requiere ajustes antes de entregar"
        if self.total > 0:
            return "Aprobado con observaciones menores"
        return "Sin hallazgos: listo para revisión de pares"

    @staticmethod
    def _limpiar_y_ordenar(hallazgos: list[Hallazgo]) -> list[Hallazgo]:
        vistos: set[tuple[int, str, str]] = set()
        limpios: list[Hallazgo] = []
        for hallazgo in hallazgos:
            clave = (hallazgo.linea, hallazgo.regla, hallazgo.detalle)
            if clave in vistos:
                continue
            vistos.add(clave)
            limpios.append(hallazgo)
        return sorted(
            limpios,
            key=lambda hallazgo: (hallazgo.linea, PRIORIDAD[hallazgo.severidad]),
        )

    def mostrar(self, titulo: str) -> None:
        """Imprime el informe completo en la consola."""
        ancho = 64
        print("=" * ancho)
        print("INFORME DE REVISIÓN DE CÓDIGO".center(ancho).rstrip())
        print("=" * ancho)
        print(f" Fuente          : {titulo}")
        print(f" Reglas aplicadas: {self._reglas_aplicadas}")
        print(f" Hallazgos       : {self.total}")
        print("-" * ancho)
        if not self._hallazgos:
            print(" Sin observaciones: el código cumple las reglas activas.")
        else:
            for hallazgo in self._hallazgos:
                print(f" {hallazgo}")
        print("-" * ancho)
        conteo = self.por_severidad
        print(
            f" Alta: {conteo['alta']}   "
            f"Media: {conteo['media']}   "
            f"Baja: {conteo['baja']}"
        )
        print(f" Veredicto: {self.veredicto}")
        print("=" * ancho)


class Revisor:
    """Ejecuta una lista de reglas sobre un fragmento de código."""

    def __init__(self, reglas: Iterable[Regla] | None = None) -> None:
        self._reglas: list[Regla] = list(reglas) if reglas is not None else []

    @property
    def reglas(self) -> tuple[Regla, ...]:
        """Copia de solo lectura de las reglas registradas."""
        return tuple(self._reglas)

    def agregar(self, regla: Regla) -> None:
        """Registra una regla nueva."""
        if not isinstance(regla, Regla):
            raise TypeError("Solo se pueden registrar instancias de Regla")
        self._reglas.append(regla)

    def analizar(self, codigo: str) -> Informe:
        """Convierte el texto en AST y aplica todas las reglas."""
        if not codigo.strip():
            raise ValueError("No hay código que revisar")
        try:
            arbol = ast.parse(codigo)
        except SyntaxError as error:
            raise ValueError(
                f"Código inválido en la línea {error.lineno}: {error.msg}"
            ) from error

        hallazgos: list[Hallazgo] = []
        for regla in self._reglas:
            hallazgos.extend(regla.revisar(arbol))
        return Informe(hallazgos, len(self._reglas))


# Fragmento con problemas deliberados: sirve como caso de estudio.
CODIGO_EJEMPLO = '''\
class Inventario:
    def __init__(self, duenio):
        self.duenio = duenio
        self.objetos = []

    def agregar(self, objeto):
        print("Agregando:", objeto)
        self.objetos.append(objeto)

    def procesar_todo(self):
        total = 0
        armas = 0
        for objeto in self.objetos:
            if objeto["tipo"] == "arma":
                total += objeto["precio"]
                armas += 1
            elif objeto["tipo"] == "pocion":
                total += objeto["precio"] // 2
            else:
                total += objeto["precio"]
        promedio = total / len(self.objetos) if self.objetos else 0
        resumen = {"total": total, "armas": armas, "promedio": promedio}
        if promedio > 100:
            resumen["alerta"] = True
        else:
            resumen["alerta"] = False
        return resumen
'''

# Misma idea, ahora con docstring, atributos protegidos y type hints.
CODIGO_CORREGIDO = '''\
class Inventario:
    """Guarda los objetos que lleva un personaje."""

    def __init__(self, duenio: str) -> None:
        self._duenio = duenio
        self._objetos: list[str] = []

    def agregar(self, objeto: str) -> None:
        """Añade un objeto al inventario."""
        self._objetos.append(objeto)

    def total(self) -> int:
        """Devuelve cuántos objetos hay."""
        return len(self._objetos)
'''


def main() -> None:
    """Ejecuta el revisor sobre los dos fragmentos de ejemplo."""
    revisor = Revisor()
    revisor.agregar(DocstringDeClase())
    revisor.agregar(AtributosPublicos())
    revisor.agregar(MetodoLargo())
    revisor.agregar(PrintEnLogica())
    revisor.agregar(FaltaTypeHints())

    print()
    revisor.analizar(CODIGO_EJEMPLO).mostrar("fragmento con problemas · inventario.py")
    print()
    revisor.analizar(CODIGO_CORREGIDO).mostrar("fragmento corregido · inventario.py")


if __name__ == "__main__":
    main()
