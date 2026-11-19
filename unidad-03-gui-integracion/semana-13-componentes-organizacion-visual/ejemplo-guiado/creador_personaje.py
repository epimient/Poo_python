"""Creador de personajes: formulario ttk con validación y vista previa.

El modelo valida sus propios datos y lanza `ValueError`. La interfaz captura
ese error y lo muestra junto al formulario, sin abrir ventanas emergentes.

Ejecuta: python3 creador_personaje.py
"""

import tkinter as tk
from tkinter import ttk

CLASES = ("Guerrero", "Maga", "Arquero", "Pícaro")
COLOR_ERROR = "#b00020"
COLOR_OK = "#1b7f3b"


class Personaje:
    """Modelo de personaje con validación en el constructor."""

    def __init__(self, nombre: str, clase: str, nivel: int) -> None:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        if len(nombre) > 20:
            raise ValueError("El nombre admite como máximo 20 caracteres.")
        if clase not in CLASES:
            raise ValueError("Elige una clase de la lista.")
        if not 1 <= nivel <= 60:
            raise ValueError("El nivel debe estar entre 1 y 60.")

        self.nombre = nombre
        self.clase = clase
        self.nivel = nivel
        self.vida = 80 + nivel * 12

    def fila(self) -> tuple[str, str, str, str]:
        """Devuelve los valores que consume el Treeview."""
        return self.nombre, self.clase, str(self.nivel), str(self.vida)


class AppCreador(tk.Tk):
    """Ventana principal: formulario, vista previa y lista."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Creador de personajes")
        self.geometry("790x640")
        self.minsize(720, 580)

        self.var_nombre = tk.StringVar()
        self.var_clase = tk.StringVar(value=CLASES[0])
        self.var_nivel = tk.StringVar(value="1")
        self.personajes: list[Personaje] = []

        self._configurar_estilos()
        self._crear_widgets()

        # La vista previa se refresca cada vez que cambia una variable.
        for variable in (self.var_nombre, self.var_clase, self.var_nivel):
            variable.trace_add("write", lambda *_: self._actualizar_vista_previa())

        self._actualizar_vista_previa()
        self.entrada_nombre.focus_set()

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Helvetica", 17, "bold"))
        estilo.configure("Subtitulo.TLabel", foreground="#555555")
        estilo.configure("Error.TLabel", foreground=COLOR_ERROR)
        estilo.configure("Ok.TLabel", foreground=COLOR_OK)
        estilo.configure("Dato.TLabel", font=("Helvetica", 11, "bold"))
        estilo.configure("Treeview", rowheight=26)
        estilo.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        estilo.configure("Accion.TButton", font=("Helvetica", 10, "bold"), padding=(10, 6))

    def _crear_widgets(self) -> None:
        self.configure(padx=18, pady=14)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        cabecera = ttk.Frame(self)
        cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(cabecera, text="Creador de personajes", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            cabecera,
            text="Completa el formulario; la vista previa se actualiza mientras escribes.",
            style="Subtitulo.TLabel",
        ).pack(anchor="w")

        cuerpo = ttk.Frame(self)
        cuerpo.grid(row=1, column=0, sticky="ew")
        cuerpo.columnconfigure(0, weight=1, uniform="columna")
        cuerpo.columnconfigure(1, weight=1, uniform="columna")

        self._crear_formulario(cuerpo)
        self._crear_vista_previa(cuerpo)
        self._crear_lista()

        self.mensaje = ttk.Label(self, text="Listo para crear tu primer personaje.")
        self.mensaje.grid(row=3, column=0, sticky="w", pady=(8, 0))

    def _crear_formulario(self, contenedor: ttk.Frame) -> None:
        marco = ttk.LabelFrame(contenedor, text=" Nuevo personaje ", padding=16)
        marco.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        marco.columnconfigure(1, weight=1)

        ttk.Label(marco, text="Nombre").grid(row=0, column=0, sticky="w", pady=6)
        self.entrada_nombre = ttk.Entry(marco, textvariable=self.var_nombre)
        self.entrada_nombre.grid(row=0, column=1, sticky="ew", padx=(12, 0), pady=6)

        ttk.Label(marco, text="Clase").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(
            marco,
            textvariable=self.var_clase,
            values=CLASES,
            state="readonly",
        ).grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=6)

        ttk.Label(marco, text="Nivel").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Spinbox(
            marco,
            from_=1,
            to=60,
            textvariable=self.var_nivel,
            width=6,
        ).grid(row=2, column=1, sticky="w", padx=(12, 0), pady=6)

        ttk.Label(
            marco,
            text="Nombre de 1 a 20 caracteres · nivel de 1 a 60.",
            style="Subtitulo.TLabel",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 12))

        botones = ttk.Frame(marco)
        botones.grid(row=4, column=0, columnspan=2, sticky="ew")
        ttk.Button(
            botones, text="Crear personaje", style="Accion.TButton", command=self._crear_personaje
        ).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self._limpiar_formulario).pack(
            side="left", padx=8
        )

    def _crear_vista_previa(self, contenedor: ttk.Frame) -> None:
        marco = ttk.LabelFrame(contenedor, text=" Vista previa ", padding=16)
        marco.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        marco.columnconfigure(1, weight=1)

        self.pre_nombre = ttk.Label(marco, style="Dato.TLabel")
        self.pre_nombre.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        campos = (
            ("Clase", "pre_clase"),
            ("Nivel", "pre_nivel"),
            ("Vida estimada", "pre_vida"),
        )
        for fila, (titulo, atributo) in enumerate(campos, start=1):
            ttk.Label(marco, text=f"{titulo}:", foreground="#555555").grid(
                row=fila, column=0, sticky="w", pady=4
            )
            etiqueta = ttk.Label(marco, text="—")
            etiqueta.grid(row=fila, column=1, sticky="w", padx=(12, 0), pady=4)
            setattr(self, atributo, etiqueta)

        ttk.Label(
            marco,
            text="La vida se calcula como 80 + nivel × 12.",
            style="Subtitulo.TLabel",
            wraplength=260,
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(14, 0))

    def _crear_lista(self) -> None:
        marco = ttk.LabelFrame(self, text=" Personajes creados ", padding=(12, 10))
        marco.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)

        columnas = ("nombre", "clase", "nivel", "vida")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=6)
        for columna, titulo, ancho, alineacion in (
            ("nombre", "Nombre", 200, "w"),
            ("clase", "Clase", 140, "w"),
            ("nivel", "Nivel", 80, "center"),
            ("vida", "Vida", 90, "center"),
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor=alineacion)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=barra.set)

    def _actualizar_vista_previa(self) -> None:
        nombre = self.var_nombre.get().strip() or "Sin nombre"
        self.pre_nombre.config(text=nombre)
        self.pre_clase.config(text=self.var_clase.get() or "—")

        try:
            nivel = int(self.var_nivel.get())
        except ValueError:
            self.pre_nivel.config(text="—")
            self.pre_vida.config(text="—")
            return

        self.pre_nivel.config(text=str(nivel))
        if 1 <= nivel <= 60:
            self.pre_vida.config(text=str(80 + nivel * 12))
        else:
            self.pre_vida.config(text="—")

    def _crear_personaje(self) -> None:
        try:
            nivel = int(self.var_nivel.get())
        except ValueError:
            self._mostrar_mensaje("El nivel debe ser un número entero.", exito=False)
            return

        try:
            personaje = Personaje(self.var_nombre.get(), self.var_clase.get(), nivel)
        except ValueError as error:
            self._mostrar_mensaje(str(error), exito=False)
            return

        self.personajes.append(personaje)
        self.tabla.insert("", "end", values=personaje.fila())
        self.tabla.yview_moveto(1.0)
        self._mostrar_mensaje(f"Personaje «{personaje.nombre}» creado.", exito=True)
        self._limpiar_formulario(mostrar_aviso=False)

    def _limpiar_formulario(self, mostrar_aviso: bool = True) -> None:
        self.var_nombre.set("")
        self.var_clase.set(CLASES[0])
        self.var_nivel.set("1")
        if mostrar_aviso:
            self._mostrar_mensaje("Formulario limpio.", exito=True)
        self.entrada_nombre.focus_set()

    def _mostrar_mensaje(self, texto: str, exito: bool) -> None:
        self.mensaje.config(text=texto, style="Ok.TLabel" if exito else "Error.TLabel")


def main() -> None:
    app = AppCreador()
    app.mainloop()


if __name__ == "__main__":
    main()
