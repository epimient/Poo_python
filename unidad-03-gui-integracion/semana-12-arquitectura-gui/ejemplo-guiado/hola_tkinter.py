"""Ventana mínima de Tkinter: el bucle de eventos en acción.

Ejecuta: python3 hola_tkinter.py
Cierra la ventana con la X de la barra de título o con Alt+F4.
"""

import tkinter as tk


class AppHola(tk.Tk):
    """Ventana raíz con un saludo interactivo."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Hola, Tkinter")
        self.geometry("380x230")
        self.resizable(False, False)

        self._saludos = 0
        self._crear_widgets()

    def _crear_widgets(self) -> None:
        """Construye la jerarquía de widgets dentro de la ventana."""
        self.saludo = tk.Label(
            self,
            text="Escribe tu nombre y pulsa el botón",
            font=("Helvetica", 11),
        )
        self.saludo.pack(pady=(28, 10))

        self.entrada = tk.Entry(self, width=24, justify="center")
        self.entrada.pack(pady=4)
        self.entrada.focus_set()

        # Enter dentro del campo dispara el mismo callback que el botón.
        self.entrada.bind("<Return>", lambda evento: self._saludar())

        tk.Button(
            self,
            text="Saludar",
            width=14,
            command=self._saludar,
        ).pack(pady=12)

        self.contador = tk.Label(self, text="0 saludos", fg="#666666")
        self.contador.pack()

    def _saludar(self) -> None:
        """Callback: lee el campo, actualiza el modelo y refresca la vista."""
        nombre = self.entrada.get().strip() or "aventurero"
        self._saludos += 1
        self.saludo.config(text=f"¡Hola, {nombre}!")
        self.contador.config(text=f"{self._saludos} saludo(s)")


def main() -> None:
    app = AppHola()
    app.mainloop()  # a partir de aquí manda el bucle de eventos


if __name__ == "__main__":
    main()
