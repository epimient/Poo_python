"""Cajero básico: formulario bancario con la lógica en una clase aparte.

`CuentaBancaria` no importa tkinter. La ventana solo traduce clics en
llamadas al modelo y muestra el resultado o el error.

Ejecuta: python3 cajero_basico.py
"""

import tkinter as tk
from tkinter import ttk

COLOR_ERROR = "#b00020"
COLOR_OK = "#1b7f3b"


class CuentaBancaria:
    """Modelo de cuenta: titular, saldo e historial de operaciones."""

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        titular = titular.strip()
        if not titular:
            raise ValueError("El titular es obligatorio.")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")

        self.titular = titular
        self._saldo = saldo_inicial
        self.historial: list[tuple[str, float, float]] = []

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> str:
        """Suma el monto y devuelve el aviso para la interfaz."""
        self._validar_monto(monto)
        self._saldo += monto
        self.historial.append(("Depósito", monto, self._saldo))
        return f"Depósito de ${monto:,.2f} realizado."

    def retirar(self, monto: float) -> str:
        """Resta el monto si hay saldo suficiente."""
        self._validar_monto(monto)
        if monto > self._saldo:
            raise ValueError(f"Saldo insuficiente. Disponible: ${self._saldo:,.2f}.")
        self._saldo -= monto
        self.historial.append(("Retiro", monto, self._saldo))
        return f"Retiro de ${monto:,.2f} realizado."

    @staticmethod
    def _validar_monto(monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")


class AppCajero(tk.Tk):
    """Ventana del cajero: abrir cuenta, operar y ver el historial."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Cajero básico")
        self.geometry("580x640")
        self.minsize(540, 600)

        self.var_titular = tk.StringVar()
        self.var_monto = tk.StringVar()
        self.cuenta: CuentaBancaria | None = None

        self._configurar_estilos()
        self._crear_widgets()

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Helvetica", 17, "bold"))
        estilo.configure("Subtitulo.TLabel", foreground="#555555")
        estilo.configure("Error.TLabel", foreground=COLOR_ERROR)
        estilo.configure("Ok.TLabel", foreground=COLOR_OK)
        estilo.configure("Saldo.TLabel", font=("Helvetica", 20, "bold"), foreground="#1b3a6b")
        estilo.configure("Treeview", rowheight=26)
        estilo.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        estilo.configure("Accion.TButton", font=("Helvetica", 10, "bold"), padding=(10, 6))

    def _crear_widgets(self) -> None:
        self.configure(padx=18, pady=14)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        cabecera = ttk.Frame(self)
        cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(cabecera, text="Cajero básico", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            cabecera,
            text="Abre una cuenta y luego deposita o retira montos.",
            style="Subtitulo.TLabel",
        ).pack(anchor="w")

        self._crear_cuenta()
        self._crear_operaciones()
        self._crear_historial()

        self.mensaje = ttk.Label(self, text="Escribe el titular y abre una cuenta.")
        self.mensaje.grid(row=4, column=0, sticky="w", pady=(8, 0))

    def _crear_cuenta(self) -> None:
        marco = ttk.LabelFrame(self, text=" Cuenta ", padding=(14, 10))
        marco.grid(row=1, column=0, sticky="ew")
        marco.columnconfigure(1, weight=1)

        ttk.Label(marco, text="Titular").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_titular = ttk.Entry(marco, textvariable=self.var_titular)
        self.entrada_titular.grid(row=0, column=1, sticky="ew", padx=(12, 8), pady=5)
        self.entrada_titular.bind("<Return>", lambda evento: self._abrir_cuenta())

        self.btn_abrir = ttk.Button(
            marco, text="Abrir cuenta", style="Accion.TButton", command=self._abrir_cuenta
        )
        self.btn_abrir.grid(row=0, column=2, pady=5)

        ttk.Label(marco, text="Titular actual:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.lbl_titular = ttk.Label(marco, text="—")
        self.lbl_titular.grid(row=1, column=1, columnspan=2, sticky="w", padx=(12, 0), pady=(10, 0))

        ttk.Label(marco, text="Saldo").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.lbl_saldo = ttk.Label(marco, text="$0.00", style="Saldo.TLabel")
        self.lbl_saldo.grid(row=2, column=1, columnspan=2, sticky="w", padx=(12, 0), pady=(2, 0))

        self.entrada_titular.focus_set()

    def _crear_operaciones(self) -> None:
        marco = ttk.LabelFrame(self, text=" Operación ", padding=(14, 10))
        marco.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        marco.columnconfigure(1, weight=1)

        ttk.Label(marco, text="Monto").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_monto = ttk.Entry(marco, textvariable=self.var_monto)
        self.entrada_monto.grid(row=0, column=1, sticky="ew", padx=(12, 8), pady=5)
        self.entrada_monto.bind("<Return>", lambda evento: self._operar(es_deposito=True))

        self.btn_depositar = ttk.Button(
            marco, text="Depositar", style="Accion.TButton", command=lambda: self._operar(True)
        )
        self.btn_depositar.grid(row=0, column=2, padx=(0, 6), pady=5)

        self.btn_retirar = ttk.Button(
            marco, text="Retirar", command=lambda: self._operar(False)
        )
        self.btn_retirar.grid(row=0, column=3, pady=5)

        ttk.Label(
            marco,
            text="Ejemplo de monto: 150.50",
            style="Subtitulo.TLabel",
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # Hasta que no exista una cuenta, las operaciones están bloqueadas.
        self.entrada_monto.config(state="disabled")
        self.btn_depositar.state(["disabled"])
        self.btn_retirar.state(["disabled"])

    def _crear_historial(self) -> None:
        marco = ttk.LabelFrame(self, text=" Historial ", padding=(12, 10))
        marco.grid(row=3, column=0, sticky="nsew", pady=(12, 0))
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)

        columnas = ("operacion", "monto", "saldo")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=7)
        for columna, titulo, ancho, alineacion in (
            ("operacion", "Operación", 140, "w"),
            ("monto", "Monto", 120, "e"),
            ("saldo", "Saldo después", 140, "e"),
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor=alineacion)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=barra.set)

    def _abrir_cuenta(self) -> None:
        try:
            self.cuenta = CuentaBancaria(self.var_titular.get())
        except ValueError as error:
            self._mostrar_mensaje(str(error), exito=False)
            return

        self.var_titular.set(self.cuenta.titular)
        self.entrada_titular.config(state="disabled")
        self.btn_abrir.state(["disabled"])
        self.entrada_monto.config(state="normal")
        self.btn_depositar.state(["!disabled"])
        self.btn_retirar.state(["!disabled"])

        self.lbl_titular.config(text=self.cuenta.titular)
        self._actualizar_saldo()
        self._mostrar_mensaje(f"Cuenta abierta para {self.cuenta.titular}.", exito=True)
        self.entrada_monto.focus_set()

    def _operar(self, es_deposito: bool) -> None:
        if self.cuenta is None:
            self._mostrar_mensaje("Primero abre una cuenta.", exito=False)
            return

        # Acepta coma o punto como separador decimal.
        texto = self.var_monto.get().strip().replace(",", ".")
        try:
            monto = float(texto)
        except ValueError:
            self._mostrar_mensaje("Escribe un monto numérico, por ejemplo 150.50", exito=False)
            return

        try:
            if es_deposito:
                aviso = self.cuenta.depositar(monto)
            else:
                aviso = self.cuenta.retirar(monto)
        except ValueError as error:
            self._mostrar_mensaje(str(error), exito=False)
            return

        self._actualizar_saldo()
        self._registrar_movimiento(es_deposito, monto)
        self.var_monto.set("")
        self._mostrar_mensaje(aviso, exito=True)

    def _actualizar_saldo(self) -> None:
        if self.cuenta is not None:
            self.lbl_saldo.config(text=f"${self.cuenta.saldo:,.2f}")

    def _registrar_movimiento(self, es_deposito: bool, monto: float) -> None:
        valores = (
            "Depósito" if es_deposito else "Retiro",
            f"${monto:,.2f}",
            f"${self.cuenta.saldo:,.2f}" if self.cuenta else "—",
        )
        self.tabla.insert("", 0, values=valores)
        self.tabla.yview_moveto(0)

    def _mostrar_mensaje(self, texto: str, exito: bool) -> None:
        self.mensaje.config(text=texto, style="Ok.TLabel" if exito else "Error.TLabel")


def main() -> None:
    app = AppCajero()
    app.mainloop()


if __name__ == "__main__":
    main()
