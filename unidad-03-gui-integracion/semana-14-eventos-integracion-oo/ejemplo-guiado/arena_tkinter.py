"""Arena de combate por turnos con Tkinter.

Tres capas bien separadas:
- Dominio: Personaje y Combate (no importan Tkinter).
- Persistencia: guardar_partida / cargar_partida en JSON.
- Interfaz: ArenaApp, que traduce eventos de la ventana en llamadas al dominio.

Ejecuta: python3 arena_tkinter.py
Semilla fija para pruebas: python3 arena_tkinter.py --semilla 7
"""

from __future__ import annotations

import argparse
import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

RUTA_PARTIDA = Path(__file__).with_name("partida_arena.json")

CLASES: dict[str, dict[str, int]] = {
    "guerrero": {"hp_max": 120, "ataque": 14, "defensa": 8},
    "mago": {"hp_max": 85, "ataque": 20, "defensa": 3},
    "arquero": {"hp_max": 100, "ataque": 16, "defensa": 5},
}

ENEMIGOS: tuple[dict[str, int | str], ...] = (
    {"nombre": "Lobo espectral", "hp_max": 90, "ataque": 13, "defensa": 4},
    {"nombre": "Gólem de ceniza", "hp_max": 120, "ataque": 11, "defensa": 9},
    {"nombre": "Bandido curtido", "hp_max": 100, "ataque": 15, "defensa": 6},
    {"nombre": "Araña gigante", "hp_max": 80, "ataque": 17, "defensa": 3},
)

# Cada evento del registro es (tipo, texto). El tipo solo decide el color.
Evento = tuple[str, str]


# ---------------------------------------------------------------------------
# Dominio: nothing here knows that a window exists.
# ---------------------------------------------------------------------------


class Personaje:
    """Personaje con estadísticas, vida y serialización a diccionario."""

    def __init__(
        self,
        nombre: str,
        clase: str,
        hp_max: int,
        ataque: int,
        defensa: int,
    ) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if hp_max <= 0 or ataque <= 0 or defensa < 0:
            raise ValueError("hp_max y ataque deben ser positivos; defensa no puede ser negativa.")

        self.nombre = nombre.strip()
        self.clase = clase
        self.hp_max = hp_max
        self.hp = hp_max
        self.ataque = ataque
        self.defensa = defensa

    @property
    def esta_vivo(self) -> bool:
        return self.hp > 0

    def recibir_dano(self, cantidad: int) -> int:
        """Aplica el daño sin bajar de cero y devuelve el daño real."""
        aplicado = min(max(0, cantidad), self.hp)
        self.hp -= aplicado
        return aplicado

    def atacar(self, objetivo: "Personaje", rng: random.Random) -> int:
        """Ataca a otro personaje y devuelve el daño causado."""
        base = self.ataque + rng.randint(-2, 3)
        dano = max(1, base - objetivo.defensa // 2)
        return objetivo.recibir_dano(dano)

    def a_dict(self) -> dict[str, object]:
        return {
            "nombre": self.nombre,
            "clase": self.clase,
            "hp": self.hp,
            "hp_max": self.hp_max,
            "ataque": self.ataque,
            "defensa": self.defensa,
        }

    @classmethod
    def desde_dict(cls, datos: dict[str, object]) -> "Personaje":
        try:
            personaje = cls(
                nombre=str(datos["nombre"]),
                clase=str(datos["clase"]),
                hp_max=int(datos["hp_max"]),  # type: ignore[arg-type]
                ataque=int(datos["ataque"]),  # type: ignore[arg-type]
                defensa=int(datos["defensa"]),  # type: ignore[arg-type]
            )
            personaje.hp = int(datos["hp"])  # type: ignore[arg-type]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"personaje inválido: {exc}") from exc

        if not 0 <= personaje.hp <= personaje.hp_max:
            raise ValueError(f"HP fuera de rango para {personaje.nombre}.")
        return personaje


class Combate:
    """Turnos entre dos personajes. No hay widgets ni mensajes de Tkinter."""

    def __init__(
        self,
        jugador: Personaje,
        enemigo: Personaje,
        semilla: int | None = None,
    ) -> None:
        self.jugador = jugador
        self.enemigo = enemigo
        self.semilla = semilla
        self.rng = random.Random(semilla)
        self.turno = 1
        self.terminado = False
        self.ganador: str | None = None
        self.log: list[Evento] = [
            ("turno", "Turno 1"),
            ("sistema", f"Comienza el combate: {jugador.nombre} vs {enemigo.nombre}."),
        ]

    def turno_jugador(self) -> list[Evento]:
        if self.terminado:
            return [("sistema", "El combate ya terminó.")]

        dano = self.jugador.atacar(self.enemigo, self.rng)
        eventos: list[Evento] = [
            ("jugador", f"Atacas a {self.enemigo.nombre} y le quitas {dano} de HP."),
        ]
        if not self.enemigo.esta_vivo:
            self.terminado = True
            self.ganador = self.jugador.nombre
            eventos.append(("sistema", f"¡{self.enemigo.nombre} ha caído! Victoria."))
        self.log.extend(eventos)
        return eventos

    def turno_enemigo(self) -> list[Evento]:
        if self.terminado:
            return [("sistema", "El combate ya terminó.")]

        dano = self.enemigo.atacar(self.jugador, self.rng)
        eventos: list[Evento] = [
            ("enemigo", f"{self.enemigo.nombre} te golpea y te quita {dano} de HP."),
        ]
        if not self.jugador.esta_vivo:
            self.terminado = True
            self.ganador = self.enemigo.nombre
            eventos.append(("sistema", "Has caído. Pulsa Reiniciar para intentarlo otra vez."))
        else:
            self.turno += 1
            eventos.append(("turno", f"Turno {self.turno}"))
        self.log.extend(eventos)
        return eventos

    def a_dict(self) -> dict[str, object]:
        return {
            "version": 1,
            "semilla": self.semilla,
            "turno": self.turno,
            "terminado": self.terminado,
            "ganador": self.ganador,
            "jugador": self.jugador.a_dict(),
            "enemigo": self.enemigo.a_dict(),
            "log": [{"tipo": tipo, "texto": texto} for tipo, texto in self.log],
        }

    @classmethod
    def desde_dict(cls, datos: dict[str, object]) -> "Combate":
        try:
            jugador = Personaje.desde_dict(datos["jugador"])  # type: ignore[arg-type]
            enemigo = Personaje.desde_dict(datos["enemigo"])  # type: ignore[arg-type]
            semilla_cruda = datos.get("semilla")
            semilla = None if semilla_cruda is None else int(semilla_cruda)  # type: ignore[arg-type]

            combate = cls(jugador, enemigo, semilla=semilla)
            combate.turno = int(datos["turno"])  # type: ignore[arg-type]
            combate.terminado = bool(datos["terminado"])
            ganador = datos.get("ganador")
            combate.ganador = None if ganador is None else str(ganador)

            log_crudo = datos["log"]
            if not isinstance(log_crudo, list):
                raise ValueError("el registro no es una lista")
            combate.log = [
                (str(item["tipo"]), str(item["texto"]))  # type: ignore[index]
                for item in log_crudo
            ]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"partida dañada o incompleta: {exc}") from exc

        if combate.turno < 1:
            raise ValueError("el número de turno no puede ser menor que 1")
        return combate


def crear_personaje(nombre: str, clase: str) -> Personaje:
    """Crea un personaje jugable a partir de la clase elegida."""
    clave = clase.strip().lower()
    if clave not in CLASES:
        raise ValueError(f"clase desconocida: {clase!r}")
    datos = CLASES[clave]
    return Personaje(nombre, clave, datos["hp_max"], datos["ataque"], datos["defensa"])


def crear_enemigo(rng: random.Random) -> Personaje:
    """Elige un enemigo al azar y varía un poco sus estadísticas."""
    plantilla = rng.choice(ENEMIGOS)
    ajuste = rng.randint(-5, 5)
    return Personaje(
        nombre=str(plantilla["nombre"]),
        clase="enemigo",
        hp_max=max(40, int(plantilla["hp_max"]) + ajuste),
        ataque=max(5, int(plantilla["ataque"]) + ajuste // 2),
        defensa=max(0, int(plantilla["defensa"])),
    )


# ---------------------------------------------------------------------------
# Persistencia: JSON plano, sin guardar objetos de Python.
# ---------------------------------------------------------------------------


def guardar_partida(combate: Combate, ruta: Path = RUTA_PARTIDA) -> Path:
    """Escribe la partida de forma atómica para no dejar archivos a medias."""
    texto = json.dumps(combate.a_dict(), ensure_ascii=False, indent=2)
    temporal = ruta.with_name(ruta.name + ".tmp")
    temporal.write_text(texto + "\n", encoding="utf-8")
    temporal.replace(ruta)
    return ruta


def cargar_partida(ruta: Path = RUTA_PARTIDA) -> Combate:
    """Lee y valida una partida. Lanza ValueError si el contenido no sirve."""
    texto = ruta.read_text(encoding="utf-8")
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ValueError(f"el archivo no contiene JSON válido: {exc.msg}") from exc
    if not isinstance(datos, dict):
        raise ValueError("el archivo debe contener un objeto JSON")
    return Combate.desde_dict(datos)


# ---------------------------------------------------------------------------
# Interfaz: callbacks delgados que llaman al dominio y refrescan la vista.
# ---------------------------------------------------------------------------


class ArenaApp:
    """Ventana principal de la arena."""

    def __init__(self, ventana: tk.Tk, semilla: int | None = None) -> None:
        self.ventana = ventana
        self.semilla = semilla
        self.combate: Combate | None = None
        self.ruta_partida = RUTA_PARTIDA
        self._rng_ui = random.Random(semilla)
        self._esperando_enemigo = False
        self._pendiente: str | None = None

        self.ventana.title("Arena de Combate · POO con Python")
        self.ventana.geometry("920x740")
        self.ventana.minsize(820, 680)
        self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar)

        self._construir_interfaz()
        self._reiniciar()

        # bind global: la ventana escucha las teclas.
        self.ventana.bind("<Key>", self._al_pulsar_tecla)

    # -- construcción -------------------------------------------------------

    def _construir_interfaz(self) -> None:
        raiz = ttk.Frame(self.ventana, padding=16)
        raiz.pack(fill="both", expand=True)
        raiz.columnconfigure(0, weight=1)
        raiz.rowconfigure(4, weight=1)

        cabecera = ttk.Frame(raiz)
        cabecera.grid(row=0, column=0, sticky="ew")
        ttk.Label(
            cabecera,
            text="Arena de Combate",
            font=("Helvetica", 22, "bold"),
        ).pack(side="left")
        semilla_texto = "Semilla: aleatoria" if self.semilla is None else f"Semilla: {self.semilla}"
        ttk.Label(cabecera, text=semilla_texto, foreground="#555555").pack(side="right")

        paneles = ttk.Frame(raiz)
        paneles.grid(row=1, column=0, sticky="ew", pady=(14, 10))
        paneles.columnconfigure(0, weight=1)
        paneles.columnconfigure(2, weight=1)

        self.panel_jugador, self.ui_jugador = self._crear_panel(paneles, "Tu personaje", 0)
        ttk.Label(paneles, text="VS", font=("Helvetica", 16, "bold")).grid(
            row=0, column=1, padx=16
        )
        self.panel_enemigo, self.ui_enemigo = self._crear_panel(paneles, "Enemigo", 2)

        seleccion = ttk.Frame(raiz)
        seleccion.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(seleccion, text="Nombre:").pack(side="left")
        self.var_nombre = tk.StringVar(value="Aventurero")
        self.entrada_nombre = ttk.Entry(seleccion, textvariable=self.var_nombre, width=16)
        self.entrada_nombre.pack(side="left", padx=(6, 16))

        ttk.Label(seleccion, text="Clase:").pack(side="left")
        self.var_clase = tk.StringVar(value="guerrero")
        self.combo_clase = ttk.Combobox(
            seleccion,
            textvariable=self.var_clase,
            values=tuple(CLASES),
            state="readonly",
            width=12,
        )
        self.combo_clase.pack(side="left", padx=(6, 16))

        self.btn_iniciar = ttk.Button(
            seleccion, text="Iniciar combate", command=self._iniciar_combate
        )
        self.btn_iniciar.pack(side="left")

        acciones = ttk.Frame(raiz)
        acciones.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.btn_atacar = ttk.Button(acciones, text="Atacar (A)", command=self._atacar)
        self.btn_atacar.pack(side="left", padx=(0, 8))
        self.btn_guardar = ttk.Button(acciones, text="Guardar partida", command=self._guardar)
        self.btn_guardar.pack(side="left", padx=(0, 8))
        self.btn_cargar = ttk.Button(acciones, text="Cargar partida", command=self._cargar)
        self.btn_cargar.pack(side="left", padx=(0, 8))
        self.btn_reiniciar = ttk.Button(acciones, text="Reiniciar", command=self._reiniciar)
        self.btn_reiniciar.pack(side="left")

        marco_log = ttk.LabelFrame(raiz, text="Registro de la batalla", padding=8)
        marco_log.grid(row=4, column=0, sticky="nsew")
        marco_log.columnconfigure(0, weight=1)
        marco_log.rowconfigure(0, weight=1)

        self.texto_log = tk.Text(
            marco_log,
            height=10,
            wrap="word",
            state="disabled",
            font="TkFixedFont",
            background="#1f2335",
            foreground="#c0caf5",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.texto_log.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(marco_log, orient="vertical", command=self.texto_log.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.texto_log.configure(yscrollcommand=scroll.set)

        self.texto_log.tag_configure("sistema", foreground="#9aa5ce")
        self.texto_log.tag_configure("jugador", foreground="#9ece6a")
        self.texto_log.tag_configure("enemigo", foreground="#f7768e")
        self.texto_log.tag_configure("turno", foreground="#7dcfff")

        self.lbl_estado = ttk.Label(raiz, text="", anchor="w")
        self.lbl_estado.grid(row=5, column=0, sticky="ew", pady=(8, 0))
        ttk.Label(
            raiz,
            text="Tecla A: atacar · Tecla R: reiniciar · Clic en el enemigo: inspeccionar",
            foreground="#666666",
        ).grid(row=6, column=0, sticky="w", pady=(4, 0))

        # bind sobre un widget concreto: inspeccionar al hacer clic.
        self.panel_enemigo.bind("<Button-1>", self._inspeccionar_enemigo)
        self.ui_enemigo["nombre"].bind("<Button-1>", self._inspeccionar_enemigo)

    def _crear_panel(
        self,
        padre: ttk.Frame,
        titulo: str,
        columna: int,
    ) -> tuple[ttk.LabelFrame, dict[str, tk.Widget]]:
        panel = ttk.LabelFrame(padre, text=titulo, padding=12)
        panel.grid(row=0, column=columna, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        nombre = ttk.Label(panel, text="—", font=("Helvetica", 14, "bold"))
        nombre.grid(row=0, column=0, sticky="w")
        clase = ttk.Label(panel, text="sin clase", foreground="#555555")
        clase.grid(row=1, column=0, sticky="w")
        hp_texto = ttk.Label(panel, text="HP — / —")
        hp_texto.grid(row=2, column=0, sticky="w", pady=(10, 2))
        barra = ttk.Progressbar(panel, maximum=100, value=0)
        barra.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        stats = ttk.Label(panel, text="ATQ — · DEF —")
        stats.grid(row=4, column=0, sticky="w")

        widgets = {
            "nombre": nombre,
            "clase": clase,
            "hp_texto": hp_texto,
            "barra": barra,
            "stats": stats,
        }
        return panel, widgets

    # -- callbacks ----------------------------------------------------------

    def _iniciar_combate(self) -> None:
        nombre = self.var_nombre.get().strip()
        if not nombre:
            self._avisar("Escribe un nombre para tu personaje.", error=True)
            self.entrada_nombre.focus_set()
            return

        try:
            jugador = crear_personaje(nombre, self.var_clase.get())
            enemigo = crear_enemigo(self._rng_ui)
            combate = Combate(jugador, enemigo, semilla=self.semilla)
        except ValueError as exc:
            self._avisar(f"No se pudo iniciar el combate: {exc}", error=True)
            return

        self._cancelar_pendiente()
        self.combate = combate
        self._limpiar_log()
        self._escribir(combate.log)
        self._refrescar()
        self._avisar(f"¡Comienza el combate contra {enemigo.nombre}! Pulsa Atacar.")
        self._actualizar_botones()

    def _atacar(self) -> None:
        if self.combate is None:
            self._avisar("Primero inicia un combate.", error=True)
            return
        if self.combate.terminado or self._esperando_enemigo:
            return

        eventos = self.combate.turno_jugador()
        self._escribir(eventos)
        self._refrescar()

        if self.combate.terminado:
            self._terminar()
            return

        # El enemigo responde solo, con un pequeño retraso visual.
        self._esperando_enemigo = True
        self._actualizar_botones()
        self._avisar(f"{self.combate.enemigo.nombre} prepara su ataque…")
        self._pendiente = self.ventana.after(600, self._turno_enemigo)

    def _turno_enemigo(self) -> None:
        self._pendiente = None
        self._esperando_enemigo = False
        if self.combate is None or self.combate.terminado:
            self._actualizar_botones()
            return

        eventos = self.combate.turno_enemigo()
        self._escribir(eventos)
        self._refrescar()

        if self.combate.terminado:
            self._terminar()
        else:
            self._avisar("Tu turno: pulsa Atacar o la tecla A.")
            self._actualizar_botones()

    def _terminar(self) -> None:
        self._esperando_enemigo = False
        self._actualizar_botones()
        if self.combate is None:
            return
        if self.combate.ganador == self.combate.jugador.nombre:
            self._avisar(
                f"Victoria: {self.combate.enemigo.nombre} ha caído. "
                "Puedes guardar la partida o reiniciar."
            )
        else:
            self._avisar("Derrota. Pulsa Reiniciar para volver a intentarlo.", error=True)

    def _guardar(self) -> None:
        if self.combate is None:
            self._avisar("No hay ningún combate que guardar.", error=True)
            return

        try:
            ruta = guardar_partida(self.combate, self.ruta_partida)
        except OSError as exc:
            messagebox.showerror(
                "No se pudo guardar",
                f"No se pudo escribir la partida:\n{exc}",
            )
            self._avisar("Error al guardar. Revisa la ruta y los permisos.", error=True)
            return

        self._escribir([("sistema", f"Partida guardada en {ruta}.")])
        self._avisar(f"Partida guardada en {ruta.name}.")

    def _cargar(self) -> None:
        try:
            combate = cargar_partida(self.ruta_partida)
        except FileNotFoundError:
            self._avisar("Todavía no hay ninguna partida guardada.", error=True)
            return
        except (OSError, ValueError) as exc:
            messagebox.showerror(
                "Partida inválida",
                f"No se pudo cargar la partida:\n{exc}",
            )
            self._avisar("Error al cargar: el archivo no es una partida válida.", error=True)
            return

        self._cancelar_pendiente()
        self.combate = combate
        self.var_nombre.set(combate.jugador.nombre)
        self.var_clase.set(combate.jugador.clase)
        self._limpiar_log()
        self._escribir(combate.log)
        self._refrescar()
        self._avisar(f"Partida cargada: {combate.jugador.nombre} vs {combate.enemigo.nombre}.")
        self._actualizar_botones()

    def _reiniciar(self) -> None:
        self._cancelar_pendiente()
        self.combate = None
        self.var_nombre.set("Aventurero")
        self.var_clase.set("guerrero")
        self._refrescar()
        self._actualizar_botones()
        self._limpiar_log()
        self._escribir(
            [
                ("sistema", "Elige nombre y clase, y pulsa «Iniciar combate»."),
                ("sistema", "Tecla A: atacar. Clic sobre el enemigo: inspeccionar."),
            ]
        )
        self._avisar("Listo para un nuevo combate.")

    def _inspeccionar_enemigo(self, evento: tk.Event | None = None) -> None:
        if self.combate is None:
            self._avisar("Todavía no hay enemigo al que inspeccionar.", error=True)
            return
        enemigo = self.combate.enemigo
        self._escribir(
            [
                (
                    "sistema",
                    f"Inspección: {enemigo.nombre} · HP {enemigo.hp}/{enemigo.hp_max} "
                    f"· ATQ {enemigo.ataque} · DEF {enemigo.defensa}.",
                )
            ]
        )
        self._avisar(f"Inspeccionas a {enemigo.nombre}.")

    def _al_pulsar_tecla(self, evento: tk.Event) -> None:
        # No interferir mientras se escribe en un campo de texto.
        if isinstance(self.ventana.focus_get(), (tk.Entry, ttk.Entry, ttk.Combobox)):
            return
        tecla = (evento.keysym or "").lower()
        if tecla == "a":
            self._atacar()
        elif tecla == "r":
            self._reiniciar()

    def _cerrar(self) -> None:
        self._cancelar_pendiente()
        self.ventana.destroy()

    # -- vista --------------------------------------------------------------

    def _refrescar(self) -> None:
        self._refrescar_panel(self.ui_jugador, self.combate.jugador if self.combate else None)
        self._refrescar_panel(self.ui_enemigo, self.combate.enemigo if self.combate else None)

    def _refrescar_panel(
        self,
        ui: dict[str, tk.Widget],
        personaje: Personaje | None,
    ) -> None:
        if personaje is None:
            ui["nombre"].configure(text="—")
            ui["clase"].configure(text="sin clase")
            ui["hp_texto"].configure(text="HP — / —")
            ui["stats"].configure(text="ATQ — · DEF —")
            ui["barra"].configure(maximum=100, value=0)
            return

        ui["nombre"].configure(text=personaje.nombre)
        ui["clase"].configure(text=personaje.clase.capitalize())
        ui["hp_texto"].configure(text=f"HP {personaje.hp} / {personaje.hp_max}")
        ui["stats"].configure(text=f"ATQ {personaje.ataque} · DEF {personaje.defensa}")
        ui["barra"].configure(maximum=personaje.hp_max, value=personaje.hp)

    def _actualizar_botones(self) -> None:
        hay_combate = self.combate is not None
        en_curso = (
            hay_combate
            and self.combate is not None
            and not self.combate.terminado
            and not self._esperando_enemigo
        )
        self.btn_atacar.configure(state="normal" if en_curso else "disabled")
        self.btn_guardar.configure(state="normal" if hay_combate else "disabled")
        self.btn_iniciar.configure(state="disabled" if hay_combate else "normal")
        self.combo_clase.configure(state="disabled" if hay_combate else "readonly")
        self.entrada_nombre.configure(state="disabled" if hay_combate else "normal")

    def _avisar(self, mensaje: str, error: bool = False) -> None:
        self.lbl_estado.configure(
            text=("⚠ " if error else "") + mensaje,
            foreground="#b00020" if error else "#1f6f43",
        )

    def _escribir(self, eventos: list[Evento]) -> None:
        self.texto_log.configure(state="normal")
        for tipo, texto in eventos:
            etiqueta = tipo if tipo in {"sistema", "jugador", "enemigo", "turno"} else "sistema"
            self.texto_log.insert("end", texto + "\n", etiqueta)
        self.texto_log.configure(state="disabled")
        self.texto_log.see("end")

    def _limpiar_log(self) -> None:
        self.texto_log.configure(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.configure(state="disabled")

    def _cancelar_pendiente(self) -> None:
        if self._pendiente is not None:
            try:
                self.ventana.after_cancel(self._pendiente)
            except tk.TclError:
                pass
            self._pendiente = None
        self._esperando_enemigo = False


def main() -> None:
    parser = argparse.ArgumentParser(description="Arena de combate por turnos con Tkinter.")
    parser.add_argument(
        "--semilla",
        type=int,
        default=None,
        help="Semilla para que los combates sean reproducibles en las pruebas.",
    )
    args = parser.parse_args()

    try:
        ventana = tk.Tk()
    except tk.TclError as exc:
        raise SystemExit(
            "No se pudo abrir la ventana. Ejecuta el script en un entorno con "
            f"pantalla (DISPLAY o Wayland).\nDetalle: {exc}"
        ) from exc

    ArenaApp(ventana, semilla=args.semilla)
    ventana.mainloop()


if __name__ == "__main__":
    main()
