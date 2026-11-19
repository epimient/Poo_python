"""Semana 04 — Cuenta bancaria con encapsulamiento.

Demo ejecutable: abre una cuenta, realiza operaciones válidas, muestra
los errores de las inválidas y lista el historial de movimientos.
"""

from __future__ import annotations

import math


class CuentaBancaria:
    """Cuenta con saldo protegido y validaciones en cada operación."""

    total_cuentas: int = 0

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        if not titular.strip():
            raise ValueError("El titular no puede estar vacío.")
        if not isinstance(saldo_inicial, (int, float)) or isinstance(saldo_inicial, bool):
            raise TypeError("El saldo inicial debe ser un número.")
        if not math.isfinite(saldo_inicial):
            raise ValueError("El saldo inicial debe ser un número finito.")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")

        self.titular = titular.strip()
        self._saldo = round(float(saldo_inicial), 2)
        self._historial: list[str] = []
        if self._saldo > 0:
            self._registrar("Apertura", self._saldo)
        CuentaBancaria.total_cuentas += 1

    @property
    def saldo(self) -> float:
        """Saldo actual: solo lectura desde fuera."""
        return self._saldo

    @property
    def historial(self) -> tuple[str, ...]:
        """Copia inmutable del historial, para que nadie lo modifique."""
        return tuple(self._historial)

    def depositar(self, monto: float) -> float:
        """Suma un monto válido y devuelve lo depositado."""
        monto = self._validar_monto(monto)
        self._saldo = round(self._saldo + monto, 2)
        self._registrar("Depósito", monto)
        return monto

    def retirar(self, monto: float) -> float:
        """Resta un monto válido si hay saldo suficiente."""
        monto = self._validar_monto(monto)
        if monto > self._saldo:
            raise ValueError(
                f"Saldo insuficiente: intentas retirar {self.formatear_monto(monto)} "
                f"y tienes {self.formatear_monto(self._saldo)}."
            )
        self._saldo = round(self._saldo - monto, 2)
        self._registrar("Retiro", -monto)
        return monto

    @classmethod
    def desde_registro(cls, linea: str) -> "CuentaBancaria":
        """Fábrica: crea una cuenta desde 'Titular;saldo'."""
        if ";" not in linea:
            raise ValueError("El registro debe tener el formato 'Titular;saldo'.")
        titular, saldo_texto = [parte.strip() for parte in linea.split(";", maxsplit=1)]
        try:
            saldo = float(saldo_texto)
        except ValueError:
            raise ValueError(f"El saldo '{saldo_texto}' no es un número válido.") from None
        return cls(titular, saldo)

    @staticmethod
    def formatear_monto(monto: float) -> str:
        """Formato de dinero independiente de la configuración regional."""
        return f"${monto:,.2f}"

    @staticmethod
    def _validar_monto(monto: float) -> float:
        if not isinstance(monto, (int, float)) or isinstance(monto, bool):
            raise TypeError("El monto debe ser un número.")
        if not math.isfinite(monto):
            raise ValueError("El monto debe ser un número finito.")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        return round(float(monto), 2)

    def _registrar(self, concepto: str, monto: float) -> None:
        signo = "+" if monto >= 0 else "-"
        self._historial.append(
            f"{concepto}: {signo}{self.formatear_monto(abs(monto))} "
            f"| saldo {self.formatear_monto(self._saldo)}"
        )

    def __str__(self) -> str:
        return f"Cuenta de {self.titular}: {self.formatear_monto(self._saldo)}"

    def __repr__(self) -> str:
        return f"CuentaBancaria(titular={self.titular!r}, saldo={self._saldo:.2f})"


def main() -> None:
    print("=== Cuenta bancaria (Semana 04) ===")

    cuenta = CuentaBancaria("Ada Lovelace", 250.0)
    print(cuenta)

    print("\n-- Operaciones --")
    depositado = cuenta.depositar(120.50)
    print(f"Depósito: +{CuentaBancaria.formatear_monto(depositado)}")
    print(f"Saldo: {CuentaBancaria.formatear_monto(cuenta.saldo)}")

    retirado = cuenta.retirar(80)
    print(f"Retiro: -{CuentaBancaria.formatear_monto(retirado)}")
    print(f"Saldo: {CuentaBancaria.formatear_monto(cuenta.saldo)}")

    print("\n-- Validaciones --")
    try:
        cuenta.retirar(10_000)
    except ValueError as error:
        print(f"retirar(10000): {error}")

    for monto in (0, -20):
        try:
            cuenta.depositar(monto)
        except ValueError as error:
            print(f"depositar({monto}): {error}")

    try:
        cuenta.depositar("50")  # type: ignore[arg-type]
    except TypeError as error:
        print(f"depositar('50'): {error}")

    try:
        CuentaBancaria("", 10)
    except ValueError as error:
        print(f"titular vacío: {error}")

    try:
        CuentaBancaria("Grace", -5)
    except ValueError as error:
        print(f"saldo negativo: {error}")

    print("\n-- Historial --")
    for movimiento in cuenta.historial:
        print(f"  {movimiento}")
    print(f"Movimientos: {len(cuenta.historial)}")

    print("\n-- Fábrica desde registro --")
    otra = CuentaBancaria.desde_registro("Grace Hopper; 900.25")
    print(otra)
    print(f"repr: {otra!r}")
    print(f"Cuentas creadas: {CuentaBancaria.total_cuentas}")
    print("Nota: las construcciones inválidas no incrementan el contador.")


if __name__ == "__main__":
    main()
