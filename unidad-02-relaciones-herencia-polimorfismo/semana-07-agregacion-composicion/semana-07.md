# Semana 07 — Agregación y composición

> No es lo mismo tener algo prestado que ser dueño de ello: el dueño decide cuándo termina.

## Objetivos de aprendizaje

- Reconocer una relación **todo-parte** y distinguirla de una asociación cualquiera.
- Diferenciar **agregación** (débil) de **composición** (fuerte) por su ciclo de vida.
- Implementar ambas en Python con referencias, listas y creación interna.
- Decidir cuál usar según la identidad y la supervivencia de las partes.
- Detectar errores de **ownership**: partes compartidas, referencias filtradas y dueños múltiples.
- Observar el ciclo de vida de los objetos y explicarlo.

## ¿Por qué importa?

En la semana 06 aprendiste a relacionar clases. Pero «tiene un» es una frase ambigua. Un equipo *tiene* jugadores, pero si el equipo se disuelve, los jugadores siguen existiendo y se van a otro equipo. Un inventario *tiene* ítems, y si el inventario desaparece, la espada y las pociones desaparecen con él: no tienen sentido sueltas. Ambas son relaciones todo-parte, pero el **dueño** y el **ciclo de vida** son distintos.

Esta diferencia decide bugs reales. Si dos inventarios comparten la misma poción y uno la consume, el otro queda con un ítem fantasma. Si un personaje guarda una referencia a un ítem de un inventario que ya se borró, el ítem sobrevive sin dueño y nadie lo administra. Si tratas una agregación como composición y borras el equipo, destruyes personajes que el jugador todavía necesitaba.

En banca el patrón se repite: un `Cliente` **agrega** cuentas (el cliente se va, la cuenta puede transferirse o cerrarse por separado) mientras una `Transaccion` **compone** sus movimientos (un movimiento no existe fuera de su transacción). Elegir mal complica la auditoría y la eliminación de datos.

:::info
La pregunta que resuelve todo: **si borro el todo, ¿la parte debe dejar de existir?** Si la respuesta es sí, es composición. Si la parte tiene vida propia, es agregación.
:::

## Concepto central

Una relación **todo-parte** dice que un objeto contiene o agrupa a otros. La **agregación** es la versión débil: el todo referencia partes que existen por su cuenta y que pueden pertenecer a otro todo con el tiempo. La **composición** es la versión fuerte: el todo crea, administra y destruye sus partes, y una parte pertenece a un único todo.

| Criterio | Agregación | Composición |
|---|---|---|
| Fuerza | Débil | Fuerte |
| ¿Quién crea la parte? | Alguien externo, antes del todo | El propio todo |
| ¿Quién la destruye? | Nadie en particular | El todo, al desaparecer |
| ¿Puede existir sola? | Sí, tiene identidad propia | No, carece de sentido fuera del todo |
| ¿Puede compartirse? | Sí | No |
| UML | Rombo hueco `◇` | Rombo relleno `◆` |
| Ejemplo | `Equipo` ◇— `Personaje` | `Inventario` ◆— `Item` |

Python no impone estas reglas: son un **contrato de diseño**. El lenguaje te da referencias y recolección de basura, pero no te impide compartir un ítem entre dos inventarios. Por eso la composición se implementa con disciplina: la clase dueña crea sus partes en un método propio, no las recibe desde fuera, y evita entregar referencias internas que permitan conservarlas.

El **ciclo de vida** es la secuencia nacer → usarse → morir. En composición, el ciclo de vida de la parte está contenido en el del todo: cuando el inventario deja de existir, sus ítems también. En agregación, los ciclos son independientes: borrar el equipo no toca a los personajes.

## Código paso a paso

### 1. Composición: el inventario crea sus ítems

```python
class Item:
    def __init__(self, nombre: str, tipo: str, valor: int) -> None:
        if not nombre.strip():
            raise ValueError("El ítem necesita un nombre.")
        if valor < 0:
            raise ValueError("El valor no puede ser negativo.")
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor


class Inventario:
    def __init__(self, dueno: str, capacidad: int = 6) -> None:
        self.dueno = dueno
        self.capacidad = capacidad
        self._items: list[Item] = []

    def crear_item(self, nombre: str, tipo: str, valor: int) -> None:
        if len(self._items) >= self.capacidad:
            raise ValueError("El inventario está lleno.")
        if self.obtener(nombre) is not None:
            raise ValueError("Ya existe un ítem con ese nombre.")
        self._items.append(Item(nombre, tipo, valor))
```

Fíjate en que el ítem **nace dentro** de `crear_item()`. No hay un parámetro `item` que venga de fuera. Esa es la señal de composición: el todo controla la creación de la parte.

### 2. Composición: consumir es dejar morir

```python
def consumir(self, nombre: str) -> str:
    item = self.obtener(nombre)
    if item is None:
        raise ValueError(f"No hay ningún ítem llamado {nombre!r}.")
    self._items.remove(item)
    return f"Se consumió {item.nombre}."
```

Al quitarlo de la lista, nadie más lo referencia y el objeto queda disponible para la recolección de basura. Si tu diseño necesita que el ítem sobreviva al inventario, entonces no era composición: era agregación disfrazada.

### 3. Agregación: el equipo recibe personajes existentes

```python
class Equipo:
    def __init__(self, nombre: str, maximo: int = 3) -> None:
        self.nombre = nombre
        self.maximo = maximo
        self._integrantes: list[Personaje] = []

    def reclutar(self, personaje: Personaje) -> None:
        if personaje in self._integrantes:
            raise ValueError("Ese personaje ya está en el equipo.")
        if len(self._integrantes) >= self.maximo:
            raise ValueError("No hay cupos libres.")
        self._integrantes.append(personaje)
```

Aquí el equipo **no crea** al personaje: lo recibe ya construido. Tampoco lo destruye al retirarlo:

```python
def retirar(self, nombre: str) -> Personaje | None:
    for personaje in self._integrantes:
        if personaje.nombre.lower() == nombre.lower():
            self._integrantes.remove(personaje)
            return personaje
    return None
```

El personaje retirado sigue siendo válido y puede unirse a otro equipo. Ese es el comportamiento esperado de una agregación.

### 4. Observar el ciclo de vida

Para comprobar quién muere con quién, puedes contar instancias vivas con `weakref.finalize`. No es obligatorio en producción, pero es una excelente herramienta didáctica:

```python
import weakref

class Item:
    vivos = 0

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        Item.vivos += 1
        self._finalizador = weakref.finalize(self, Item._al_liberar)

    @classmethod
    def _al_liberar(cls) -> None:
        cls.vivos -= 1
```

En la demo de `inventario.py` verás que, al borrar el inventario, el contador baja a cero. En cambio, al borrar el equipo, los personajes siguen vivos. El contador no es la composición: solo hace visible el contrato.

:::warning
En Python no hay una garantía instantánea de destrucción en todos los intérpretes. El conteo de referencias de CPython libera de inmediato, pero otros entornos pueden tardar. No diseñes reglas de negocio que dependan de que un objeto muera en el instante exacto; usa el contenedor como dueño lógico.
:::

## Diagrama / modelo

```text
COMPOSICIÓN (fuerte)                 AGREGACIÓN (débil)

Inventario ◆──────── Item            Equipo ◇──────── Personaje
   crea y posee        muere con       referencia       sobrevive
   sus ítems           el todo         partes           al todo

Ciclo de vida:
  inventario = Inventario(...)         equipo = Equipo(...)
      ├── Item("Espada")                   ├── Personaje("Kael")  ← creado antes
      ├── Item("Poción")                   └── Personaje("Runa")  ← creado antes
      └── del inventario                   └── del equipo
            → ítems liberados                    → personajes intactos
```

En UML, el rombo va **en el extremo del todo**. Relleno para composición, hueco para agregación. Si el rombo está en el lado equivocado, el diagrama dice lo contrario de lo que pretendes.

## Errores comunes

- **Compartir una parte de composición.** Agregar el mismo `Item` a dos inventarios rompe la exclusividad. Si necesitas compartir, el modelo correcto es agregación (o una entidad propia con identidad).
- **Entregar referencias internas.** Si un método devuelve el `Item` y el llamador lo guarda, el ítem sobrevive al inventario. Devuelve textos, copias de datos o una vista controlada.
- **Confundir el rombo.** Rombo relleno = composición; hueco = agregación. El rombo siempre toca al todo.
- **Usar `__del__` para reglas de negocio.** Es frágil: no se ejecuta cuando esperas y puede fallar en silencio. Prefiere métodos explícitos (`consumir`, `cerrar`, `retirar`).
- **Crear la parte fuera y llamarla composición.** Si `inventario.agregar(item_externo)` acepta cualquier ítem, no controlas su origen ni su exclusividad.
- **Borrar el todo y seguir usando la parte «porque todavía existe».** En composición es un error de diseño: la parte ya no tiene dueño ni garantías.
- **Agregar sin validar pertenencia.** Un personaje podría quedar en dos equipos si no revisas su estado antes de reclutarlo.

## Buenas prácticas

- Pregunta primero por el ciclo de vida, no por la estructura. La respuesta «debe morir con el todo» elige composición.
- En composición, crea las partes con un método de fábrica de la clase dueña y no aceptes partes externas.
- En agregación, recibe objetos ya construidos y documenta que el todo no se hace responsable de destruirlos.
- Mantén las listas privadas y ofrece operaciones con nombre de dominio: `crear_item`, `consumir`, `reclutar`, `retirar`.
- Documenta el ownership en el docstring de la clase: «posee sus ítems» o «solo referencia personajes».
- Prueba el ciclo de vida explícitamente: crea, elimina el contenedor y verifica qué queda vivo.
- Prefiere composición por defecto para partes sin identidad propia; usa agregación cuando la parte se comparte o trasciende al todo.

:::reto
Modela una `Mochila` con capacidad limitada. Los ítems comunes son composición (la mochila los crea), pero las armas únicas son agregación (existen en el mundo y se pueden prestar). Implementa ambas relaciones en la misma clase y demuestra con una demo qué sobrevive al borrar la mochila.
:::

## Checklist de la semana

- [ ] Explico la diferencia entre agregación y composición con un ejemplo propio.
- [ ] Identifico el rombo hueco y el relleno en un diagrama UML.
- [ ] Implementé una composición donde el todo crea sus partes.
- [ ] Implementé una agregación con partes creadas fuera del todo.
- [ ] Verifiqué con una demo qué objetos sobreviven al eliminar el contenedor.
- [ ] Evité filtrar referencias internas y validé la pertenencia.
- [ ] Ejecuté `inventario.py` y expliqué los contadores de objetos vivos.

## Resumen

Agregación y composición son las dos caras de «todo-parte». La agregación es un préstamo: el equipo referencia personajes que existen por su cuenta y los devuelve intactos al disolverse. La composición es un contrato de dueño único: el inventario crea sus ítems y, cuando desaparece, ellos también. En Python el contrato se sostiene con diseño —creación interna, listas privadas, métodos de dominio— porque el lenguaje no lo impone. Cuando dudes, pregunta qué debe sobrevivir al borrado del todo: esa respuesta es tu decisión de ownership.

## Siguiente paso

La semana 08 entra en la **herencia**: cómo una clase hija reutiliza y especializa a una clase base. Verás `super()`, la sobrescritura de métodos y el orden de resolución (MRO), y podrás combinar jerarquías con las relaciones todo-parte que ya dominas.
