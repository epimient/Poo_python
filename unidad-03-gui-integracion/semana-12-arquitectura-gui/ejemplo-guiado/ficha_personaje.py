"""Ficha de personaje: modelo y vista en clases separadas.

El modelo (`Personaje`) no importa tkinter. La vista (`VistaFicha`) solo
lee del modelo y pinta widgets. Esa separación es la base de MVC.

Ejecuta: python3 ficha_personaje.py
Cierra la ventana con la X de la barra de título o con Alt+F4.
"""

import tkinter as tk


class Personaje:
    """Modelo de dominio: datos y reglas, sin nada de interfaz."""

    def __init__(self, nombre: str, clase: str, nivel: int = 1) -> None:
        self.nombre = nombre
        self.clase = clase
        self.nivel = nivel
        self.vida_maxima = 80 + nivel * 20
        self.vida = self.vida_maxima

    def subir_nivel(self) -> None:
        """Sube un nivel y restaura la vida al máximo."""
        self.nivel += 1
        self.vida_maxima = 80 + self.nivel * 20
        self.vida = self.vida_maxima

    def estado(self) -> str:
        """Devuelve una etiqueta legible según la vida restante."""
        proporcion = self.vida / self.vida_maxima
        if proporcion >= 0.75:
            return "Saludable"
        if proporcion >= 0.35:
            return "Herido"
        return "En peligro"


class VistaFicha(tk.Frame):
    """Vista: conoce al modelo, pero el modelo no la conoce a ella."""

    def __init__(self, contenedor: tk.Misc, personaje: Personaje) -> None:
        super().__init__(contenedor, padx=26, pady=22)
        self.personaje = personaje
        self.grid()
        self._crear_widgets()
        self.actualizar()

    def _crear_widgets(self) -> None:
        self.lbl_nombre = tk.Label(self, font=("Helvetica", 17, "bold"))
        self.lbl_nombre.grid(row=0, column=0, columnspan=2, pady=(0, 14))

        # Cada fila: etiqueta fija a la izquierda, valor dinámico a la derecha.
        tk.Label(self, text="Clase:", anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 18), pady=3
        )
        self.lbl_clase = tk.Label(self, anchor="w")
        self.lbl_clase.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(self, text="Nivel:", anchor="w").grid(
            row=2, column=0, sticky="w", padx=(0, 18), pady=3
        )
        self.lbl_nivel = tk.Label(self, anchor="w")
        self.lbl_nivel.grid(row=2, column=1, sticky="w", pady=3)

        tk.Label(self, text="Vida:", anchor="w").grid(
            row=3, column=0, sticky="w", padx=(0, 18), pady=3
        )
        self.lbl_vida = tk.Label(self, anchor="w")
        self.lbl_vida.grid(row=3, column=1, sticky="w", pady=3)

        tk.Label(self, text="Estado:", anchor="w").grid(
            row=4, column=0, sticky="w", padx=(0, 18), pady=3
        )
        self.lbl_estado = tk.Label(self, anchor="w")
        self.lbl_estado.grid(row=4, column=1, sticky="w", pady=3)

        tk.Button(
            self,
            text="Subir de nivel",
            command=self._subir_nivel,
        ).grid(row=5, column=0, columnspan=2, pady=(18, 0), ipadx=8)

    def actualizar(self) -> None:
        """Copia el estado del modelo a los widgets."""
        p = self.personaje
        self.lbl_nombre.config(text=p.nombre)
        self.lbl_clase.config(text=p.clase)
        self.lbl_nivel.config(text=str(p.nivel))
        self.lbl_vida.config(text=f"{p.vida} / {p.vida_maxima}")
        self.lbl_estado.config(text=p.estado())

    def _subir_nivel(self) -> None:
        """Controlador: pide la acción al modelo y vuelve a pintar."""
        self.personaje.subir_nivel()
        self.actualizar()


def main() -> None:
    raiz = tk.Tk()
    raiz.title("Ficha de personaje")
    raiz.resizable(False, False)

    heroe = Personaje("Lyra", "Maga", nivel=3)
    VistaFicha(raiz, heroe)

    raiz.mainloop()


if __name__ == "__main__":
    main()
