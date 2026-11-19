# Ejercicios — Semana 02

## Nivel 1 — Básico: Refactorizar un código procedural a POO

**Enunciado.** El siguiente script funciona, pero mezcla datos y funciones. Refactorízalo en `refactor_poo.py` usando una clase `Personaje` con atributos y métodos. Conserva la misma salida del combate y agrega validaciones en el constructor.

```python
# Código de partida: completo y ejecutable, pero procedural
def crear_personaje(nombre, hp, ataque):
    return {"nombre": nombre, "hp": hp, "ataque": ataque}


def atacar(atacante, objetivo):
    dano = atacante["ataque"]
    objetivo["hp"] = max(0, objetivo["hp"] - dano)
    print(f"{atacante['nombre']} ataca a {objetivo['nombre']} y causa {dano} de daño.")


kaede = crear_personaje("Kaede", 120, 18)
rook = crear_personaje("Rook", 90, 24)
atacar(kaede, rook)
atacar(rook, kaede)
print(f"Kaede: {kaede['hp']} HP | Rook: {rook['hp']} HP")
```

**Requisitos.**
- Define `class Personaje` con `nombre`, `hp` y `ataque` en `__init__`.
- Agrega el método `atacar(objetivo)`; no uses funciones externas para esa acción.
- Valida `hp > 0` y `ataque >= 0`; lanza `ValueError` con un mensaje claro si no se cumple.
- Incluye `esta_vivo()` y úsalo al final para informar quién sigue en pie.
- Conserva la secuencia de ataques y los valores iniciales.
- El programa debe correr con `python3 refactor_poo.py` sin `input()`.

**Entrada esperada.** Los mismos datos del código de partida:

```python
kaede = Personaje("Kaede", 120, 18)
rook = Personaje("Rook", 90, 24)
```

**Salida esperada.**

```text
Kaede ataca a Rook y causa 18 de daño.
Rook ataca a Kaede y causa 24 de daño.
Kaede: 96 HP | Rook: 72 HP
Kaede sigue en pie.
Rook sigue en pie.
```

**Criterios de evaluación.**
- [ ] La clase reemplaza al diccionario y concentra el estado.
- [ ] `atacar` es un método, no una función que recibe dos diccionarios.
- [ ] Las validaciones rechazan `hp=0` y `ataque=-1`.
- [ ] La salida coincide con la esperada (puedes agregar líneas, no quitarlas).
- [ ] El código ejecuta sin errores y conserva `if __name__ == "__main__":`.

---

## Nivel 2 — Intermedio: Diagrama UML de un RPG

**Enunciado.** Diseña el diagrama de clases de un RPG sencillo por turnos. Debes entregar `uml_rpg.md` con el diagrama en texto (o una imagen referenciada) y una explicación breve de cada clase y relación. Todavía no se pide implementación completa: el objetivo es modelar antes de codificar.

**Requisitos.**
- Incluye al menos cinco clases: `Personaje`, `Arma`, `Inventario`, `Enemigo` y `Partida`.
- Cada clase debe tener entre dos y cinco atributos y al menos dos métodos.
- Usa notación UML: `+` público, `-` privado, tipos en atributos y retornos en métodos.
- Muestra al menos:
  - Una **asociación** entre `Personaje` y `Arma`.
  - Una **composición** entre `Partida` y `Equipo` (el equipo no existe sin la partida).
  - Una **herencia** de `Enemigo` hacia una clase base `Personaje` o hacia una clase `Criatura`.
- Indica cardinalidades en las relaciones (`1`, `0..*`, `1..*`).
- Explica en dos o tres líneas por qué elegiste composición en un caso y asociación en otro.

**Entrada esperada.** Un archivo Markdown con un bloque de código que contenga el diagrama, por ejemplo:

```text
┌───────────────────┐        ┌───────────────────┐
│     Personaje     │        │       Arma        │
├───────────────────┤        ├───────────────────┤
│ - nombre: str     │ 1    0..*│ - nombre: str    │
│ - hp: int         │────────│ - dano: int       │
├───────────────────┤        ├───────────────────┤
│ + atacar(): None  │        │ + calcular(): int │
└───────────────────┘        └───────────────────┘
```

**Salida esperada.** El diagrama completo, legible en texto plano, más una tabla como esta:

| Relación | Clases | Tipo | Cardinalidad | Justificación |
|---|---|---|---|---|
| porta | Personaje–Arma | Asociación | 1 → 0..* | Un personaje puede no llevar arma |
| contiene | Partida–Equipo | Composición | 1 → 1..* | El equipo se crea y se destruye con la partida |
| hereda | Enemigo–Criatura | Herencia | — | Enemigo es un tipo de criatura |

**Criterios de evaluación.**
- [ ] Las cinco clases aparecen con atributos y métodos coherentes.
- [ ] La notación de visibilidad y tipos es consistente.
- [ ] Las cardinalidades tienen sentido con las reglas del juego.
- [ ] La composición y la asociación están justificadas, no solo dibujadas.
- [ ] El diagrama se entiende sin necesidad de leer el código.
- [ ] No hay clases «Datos» o «Utilidades» sin responsabilidad clara.

---

## Nivel 3 — Reto: Plan de trabajo de un equipo

**Enunciado.** Forma un equipo de tres personas y prepara `plan_equipo.md` para construir un prototipo de combate por turnos durante las próximas tres semanas. El plan debe convertir una idea general en entregas verificables, usando Git y una metodología iterativa. Este documento será la base del trabajo en equipo del P2 y del P3.

**Requisitos.**
- Define el **alcance mínimo** del prototipo: qué entra y qué queda fuera en esta iteración.
- Asigna **roles rotativos** (coordinación, código, pruebas/documentación) y responsabilidades concretas.
- Construye un **backlog** de al menos ocho tareas, priorizadas con `Alta`, `Media` o `Baja`.
- Divide el trabajo en **tres iteraciones semanales** con un objetivo demostrable cada una.
- Define al menos **tres riesgos** con probabilidad, impacto y mitigación.
- Especifica el flujo Git: rama principal, ramas de funcionalidad, revisión y criterio para integrar.
- Incluye una **definición de terminado**: qué debe cumplir una tarea para considerarse completa.
- Agrega una tabla de seguimiento con fecha, responsable y estado.

**Entrada esperada.** Un escenario como este:

```text
Equipo: Arena Trio
Integrantes: Ana, Bruno, Carla
Producto: combate por turnos de 3 personajes contra 3 enemigos
Duración: 3 semanas
Restricción: solo biblioteca estándar, ejecución por consola
```

**Salida esperada.** Un documento con esta estructura mínima:

```text
1. Alcance y fuera de alcance
2. Roles y responsabilidades
3. Backlog priorizado (tabla)
4. Iteración 1 / 2 / 3 (objetivo, tareas, demo)
5. Riesgos (tabla)
6. Flujo Git y definición de terminado
7. Seguimiento semanal
```

Ejemplo parcial del backlog:

| ID | Tarea | Prioridad | Responsable | Iteración | Estado |
|---|---|---|---|---|---|
| T1 | Clase Personaje con validaciones | Alta | Ana | 1 | Hecho |
| T2 | Menú de selección de equipo | Alta | Bruno | 1 | En curso |
| T3 | Turnos y cálculo de daño | Alta | Carla | 2 | Pendiente |
| T4 | Pruebas de casos límite | Media | Ana | 2 | Pendiente |

**Criterios de evaluación.**
- [ ] El alcance es realista para tres semanas y tres personas.
- [ ] Cada iteración termina con algo ejecutable y demostrable.
- [ ] Las tareas tienen responsable y prioridad; no hay «hacer el juego» como tarea única.
- [ ] Los riesgos incluyen mitigación concreta, no solo «falta de tiempo».
- [ ] El flujo Git indica cuándo se crea una rama y cuándo se integra.
- [ ] La definición de terminado incluye ejecución, prueba y documentación.
- [ ] El plan se puede revisar en cinco minutos y muestra el estado real.

:::reto
Publica el plan como un *issue* o proyecto en GitHub con etiquetas `alta`, `media`, `baja` y `hecho`. Al final de cada iteración, actualiza el tablero y escribe una nota de retrospectiva: qué funcionó, qué se trabó y qué cambiará en la siguiente semana.
:::
