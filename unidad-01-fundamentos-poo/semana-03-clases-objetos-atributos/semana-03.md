# Semana 03 — Clases, objetos y atributos

> Una clase es el plano; cada objeto es una copia con sus propios datos.

## Objetivos de aprendizaje

- Definir clases con `class` y crear objetos llamando a la clase.
- Escribir `__init__` y usar `self` para guardar datos en cada instancia.
- Distinguir atributos de instancia de atributos de clase.
- Comprobar identidad, tipo y pertenencia con `id()`, `type()` e `isinstance()`.
- Inspeccionar los atributos de un objeto con `__dict__`.
- Evitar el error clásico de compartir listas o diccionarios como atributos de clase.
- Aplicar `PascalCase` a clases y `snake_case` a atributos y variables.

## ¿Por qué importa?

Hasta ahora has guardado datos en variables sueltas. Funciona para tres valores, pero un videojuego tiene decenas de personajes, cada uno con nombre, vida, nivel, inventario y estadísticas. Si usas listas paralelas, cualquier cambio exige recordar el índice correcto y nada impide que se desincronicen.

```python
nombres = ["Aria", "Brom", "Cyd"]
hps = [80, 100, 45]
niveles = [3, 2, 5]
```

Si eliminas a Brom de `nombres` y olvidas borrarlo de `hps`, el personaje número dos tendrá el nombre de Cyd y la vida de Brom. Una clase resuelve eso: agrupa los datos que pertenecen a la misma entidad y crea una copia independiente por cada objeto.

:::info
Una clase no es un personaje. Es la definición de qué datos y qué comportamiento tendrá cualquier personaje. El objeto concreto —Aria, Brom, Cyd— es la instancia.
:::

## Concepto central

Piensa en una clase como el plano de una casa y en los objetos como las casas construidas a partir de él. El plano indica que hay dos habitaciones y una puerta; cada casa tiene su propia dirección, sus muebles y su estado. Cambiar la puerta de una casa no cambia la de la otra.

En Python, definir una clase es tan simple como esto:

```python
class Personaje:
    pass
```

El nombre va en `PascalCase` porque representa un tipo. Para crear objetos se llama a la clase como si fuera una función:

```python
aria = Personaje()
brom = Personaje()

print(aria is brom)          # False: son objetos distintos
print(type(aria).__name__)   # Personaje
print(isinstance(aria, Personaje))  # True
```

Cada llamada reserva un objeto nuevo en memoria. `is` compara identidad, no contenido: dos personajes con los mismos datos siguen siendo objetos diferentes. `id()` devuelve el identificador interno de esa identidad.

### `__init__` y `self`

Una clase vacía no sirve de mucho. El método `__init__` se ejecuta automáticamente al crear el objeto y recibe los datos iniciales. Su primer parámetro es `self`, la referencia al objeto que se está construyendo.

```python
class Personaje:
    def __init__(self, nombre: str, hp: int, nivel: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.nivel = nivel
```

`self.nombre = nombre` significa: guarda el valor en un atributo del objeto. El `self` no se escribe al llamar; Python lo pasa solo.

```python
aria = Personaje("Aria", 80, 3)
print(aria.nombre)  # Aria
```

:::warning
`__init__` no es técnicamente el constructor, sino el inicializador: el objeto ya existe cuando se ejecuta. En la práctica del curso lo llamaremos constructor, como en el resto de la industria. Lo importante es que no debe devolver nada (`return` vacío o nada); si devuelve un valor, Python lanza `TypeError`.
:::

### Atributos de instancia y atributos de clase

Un atributo de instancia vive dentro de un objeto concreto. Un atributo de clase se define en el cuerpo de la clase y lo comparten todas las instancias.

```python
class Personaje:
    MAX_HP = 100              # atributo de clase
    total_personajes = 0      # contador compartido

    def __init__(self, nombre: str, hp: int = MAX_HP) -> None:
        self.nombre = nombre  # atributo de instancia
        self.hp = hp
        Personaje.total_personajes += 1
```

| Pregunta | Atributo de instancia | Atributo de clase |
|---|---|---|
| ¿Dónde se define? | Dentro de `__init__`, con `self.x` | En el cuerpo de la clase |
| ¿Quién lo ve? | Solo ese objeto | Todas las instancias |
| ¿Dónde vive? | `objeto.__dict__` | `Clase.__dict__` |
| Uso típico | nombre, hp, nivel | constantes, contadores, configuración |
| Ejemplo | `aria.hp` | `Personaje.MAX_HP` |

Los atributos de clase se leen también desde la instancia (`aria.MAX_HP`), pero no se copian en el objeto. Eso explica por qué `MAX_HP` no aparece en `aria.__dict__`.

```python
aria = Personaje("Aria")
print(aria.__dict__)            # {'nombre': 'Aria', 'hp': 100}
print(Personaje.__dict__["MAX_HP"])  # 100
print("MAX_HP" in aria.__dict__)     # False
```

## Código paso a paso

**Paso 1. La clase mínima y sus objetos.** Comprueba identidad, tipo y pertenencia antes de añadir datos.

```python
class Personaje:
    pass


uno = Personaje()
dos = Personaje()
print(uno is dos, id(uno) == id(dos), type(uno).__name__)
```

**Paso 2. Añade estado con `__init__`.** Cada instancia recibe sus propios valores.

```python
class Personaje:
    def __init__(self, nombre: str, hp: int = 100, nivel: int = 1) -> None:
        self.nombre = nombre
        self.hp = hp
        self.nivel = nivel


aria = Personaje("Aria", 80, 3)
brom = Personaje("Brom")
brom.hp = 95
print(aria.hp, brom.hp)  # 80 95: no se afectan
```

**Paso 3. Agrega atributos de clase.** `MAX_HP` es una regla compartida y `total_personajes` cuenta cuántos objetos se han creado.

```python
class Personaje:
    MAX_HP = 100
    total_personajes = 0

    def __init__(self, nombre: str, hp: int = MAX_HP, nivel: int = 1) -> None:
        self.nombre = nombre
        self.hp = hp
        self.nivel = nivel
        Personaje.total_personajes += 1
```

Fíjate en `Personaje.total_personajes` y no en `self.total_personajes`. La primera forma modifica el contador compartido; la segunda crearía un atributo nuevo en ese objeto y dejaría el contador global intacto.

**Paso 4. Construye un equipo y recorre la colección.** Una lista de objetos se trata como cualquier otra lista.

```python
equipo = [
    Personaje("Aria", 80, 3),
    Personaje("Brom", 100, 2),
    Personaje("Cyd", 45, 5),
]

for personaje in equipo:
    print(f"{personaje.nombre}: {personaje.hp} hp, nivel {personaje.nivel}")

print(Personaje.total_personajes)  # 3
```

**Paso 5. Cuidado con los mutables compartidos.** Este es el error clásico de la semana:

```python
class Gremio:
    miembros = []  # ¡una sola lista para todos los gremios!

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre


alba = Gremio("Alba")
sombra = Gremio("Sombra")
alba.miembros.append("Aria")

print(sombra.miembros)  # ['Aria']: la lista es la misma
```

La solución es crear la lista dentro de `__init__`, para que cada objeto tenga la suya:

```python
class Gremio:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.miembros: list[str] = []
```

## Diagrama / modelo

```text
Personaje (clase)
├── MAX_HP = 100                 ← atributo de clase
├── total_personajes = 3         ← atributo de clase
├── aria  → {nombre, hp, nivel}  ← instancia 1
├── brom  → {nombre, hp, nivel}  ← instancia 2
└── cyd   → {nombre, hp, nivel}  ← instancia 3
```

La clase es el molde y el contenedor de lo compartido; cada instancia es un `__dict__` independiente. Si el diagrama lo dibujas como una tabla, la clase es la cabecera y cada objeto es una fila.

## Errores comunes

**Olvidar `self` en la definición.** `def __init__(nombre):` falla al crear el objeto porque Python pasa la instancia como primer argumento. Todos los métodos de instancia llevan `self` como primer parámetro.

**Confundir la clase con una instancia.** `Personaje` es la clase; `Personaje()` es un objeto. Si imprimes `Personaje`, verás `<class '__main__.Personaje'>`; si imprimes `Personaje()`, verás una referencia como `<__main__.Personaje object at 0x...>`.

**Usar una lista como atributo de clase.** Todas las instancias comparten la misma lista y los datos se mezclan. Los mutables van en `__init__`.

**Reasignar el contador desde la instancia.** `self.total_personajes += 1` no actualiza el contador global: crea un atributo de instancia que lo tapa. Usa siempre `Personaje.total_personajes`.

**Creer que `__dict__` muestra todo.** Solo muestra los atributos propios del objeto. Los de clase están en `Clase.__dict__` o se leen por herencia de búsqueda.

**Nombrar clases en minúscula o atributos en mayúscula.** `class personaje` y `Personaje.HP_Actual` funcionan, pero rompen la convención y hacen difícil distinguir tipos de valores.

:::error
Un `__init__` que retorna algo produce `TypeError: __init__() should return None`. No escribas `return self.nombre` al final del inicializador.
:::

## Buenas prácticas

- Una clase, una responsabilidad: `Personaje` guarda datos del personaje, no gestiona la ventana del juego.
- Usa valores por defecto inmutables (`int`, `str`, `tuple`, `None`), nunca `[]` o `{}`.
- Declara las constantes compartidas en mayúsculas: `MAX_HP`, `VELOCIDAD_BASE`.
- Accede a los contadores con el nombre de la clase, no con `self`.
- Añade type hints simples y un docstring de una línea a cada clase.
- Prefiere `isinstance(x, Personaje)` a `type(x) is Personaje` cuando más adelante existan subclases.
- Mantén los nombres en singular (`Personaje`, no `Personajes`) y los atributos en `snake_case`.

## Checklist de la semana

- [ ] Sé definir una clase con `class` y crear al menos dos instancias.
- [ ] Explico qué hace `__init__` y por qué recibe `self`.
- [ ] Distingo un atributo de instancia de uno de clase sin mirar el código.
- [ ] Uso `Personaje.total_personajes` para actualizar un contador compartido.
- [ ] Inspecciono un objeto con `__dict__` y explico qué aparece y qué no.
- [ ] Evito listas y diccionarios como atributos de clase.
- [ ] Compruebo tipo e identidad con `type()`, `isinstance()` e `is`.
- [ ] Mi ejemplo `personaje.py` se ejecuta con `python3` sin errores.

## Resumen

Una clase agrupa datos y define un tipo; un objeto es una instancia concreta con su propio estado. `__init__` inicializa ese estado y `self` es la referencia al objeto en construcción. Los atributos de instancia viven en cada objeto y los de clase se comparten entre todos. Los mutables deben crearse dentro de `__init__`, y los contadores se actualizan a través del nombre de la clase. Con esto ya puedes modelar un equipo, una tienda o una partida; en la próxima semana añadirás comportamiento y protección de datos.

## Siguiente paso

En la Semana 04 convertirás estos atributos en un estado seguro: métodos que atacan y curan, constructores con valores por defecto, fábricas con `@classmethod`, validaciones con `@property` y atributos que no se pueden romper desde fuera. Llega con tu clase `Personaje` funcionando y con ganas de hacerle daño a alguien (dentro del juego).
