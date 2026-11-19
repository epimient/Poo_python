# Semana 09 — Clases abstractas

> Una clase abstracta no dice cómo hacer el trabajo: exige que alguien lo haga.

## Objetivos de aprendizaje

- Declarar clases abstractas con `abc.ABC` y `@abstractmethod`.
- Entender por qué una base incompleta no debe instanciarse.
- Diseñar contratos de comportamiento claros para las subclases.
- Diferenciar una clase abstracta de una interfaz y de un `Protocol`.
- Usar `typing.Protocol` para aceptar cualquier objeto que cumpla un contrato.
- Aplicar el patrón **método plantilla** para fijar un algoritmo y delegar pasos.

:::info
La semana pasada `Personaje` era una base cómoda pero opcional: podías crear un personaje genérico y atacar con él. Esta semana esa posibilidad desaparece a propósito.
:::

## ¿Por qué importa?

En la jerarquía de la semana 08 había un hueco: `Personaje("Genérico", 100, 5)` era válido. El objeto no representaba nada del juego, pero el programa lo aceptaba y `atacar()` devolvía 5. Si un compañero agregaba una subclase y olvidaba implementar `atacar()`, el error aparecía en pleno combate, lejos del sitio donde se escribió la clase.

Una clase abstracta convierte ese descuido en un error inmediato: si una subclase no implementa lo obligatorio, **no se puede instanciar**. El fallo salta al crear el objeto, no tres rondas después.

En banca pasa algo parecido con una `Cuenta` base. Una cuenta genérica no existe: o es de ahorros, o es corriente, o es de crédito. La base puede decir que toda cuenta debe poder `retirar()`, pero no puede decidir sola cómo se aplica la comisión.

## Concepto central

Una **clase abstracta** es una clase que define un contrato y no está pensada para crear objetos directamente. En Python se construye heredando de `ABC` y marcando los métodos obligatorios con `@abstractmethod`.

```python
from abc import ABC, abstractmethod


class Personaje(ABC):
    def __init__(self, nombre: str, vida: int) -> None:
        self.nombre = nombre
        self.vida = vida

    @abstractmethod
    def atacar(self) -> int:
        """Toda subclase concreta debe implementar este método."""

    def recibir_dano(self, cantidad: int) -> None:
        self.vida = max(0, self.vida - cantidad)
```

`Personaje` mezcla dos cosas: métodos **concretos** que ya funcionan (`recibir_dano`) y métodos **abstractos** que solo declaran una obligación (`atacar`). Esa combinación es precisamente el valor de una clase abstracta frente a una interfaz pura.

```python
p = Personaje("Genérico", 100)
# TypeError: Can't instantiate abstract class Personaje
# with abstract method atacar
```

El error no es un capricho: el objeto estaría incompleto. La base prometió que todo personaje sabe atacar y no puede cumplir la promesa por sí misma.

### El contrato

Un contrato de comportamiento responde tres preguntas:

| Pregunta | Ejemplo |
|---|---|
| ¿Qué método existe? | `atacar()` |
| ¿Qué recibe y qué devuelve? | Sin parámetros; devuelve un `int` |
| ¿Qué garantiza? | Un daño no negativo y coherente con el estado del personaje |

Las subclases pueden implementarlo como quieran, pero deben respetar esa firma. Si `Mago.atacar()` devolviera un texto, el código que suma daño se rompería aunque Python no lo impida en tiempo de ejecución.

### Clase abstracta, interfaz y `Protocol`

| Herramienta | Qué exige | Cómo se relaciona |
|---|---|---|
| Clase abstracta (`ABC`) | Herencia explícita y métodos implementados | `class Mago(Personaje)` |
| Interfaz (estilo Java) | Solo firmas, sin estado | En Python se simula con un `ABC` lleno de métodos abstractos |
| `Protocol` | Solo la forma: que existan los métodos | No requiere herencia; basta con cumplir |

Python no tiene la palabra clave `interface`. Cuando necesitas un contrato sin implementación, puedes usar un `ABC` con todos sus métodos abstractos. Cuando quieres aceptar objetos de cualquier clase que **se comporten** de cierta manera, usa `Protocol`.

### `NotImplementedError`: el contrato manual

Antes de `abc` se usaba lanzar una excepción:

```python
class Personaje:
    def atacar(self) -> int:
        raise NotImplementedError("Cada subclase debe implementar atacar()")
```

Esto avisa en tiempo de ejecución, pero no impide crear el objeto. `ABC` lo impide antes. `NotImplementedError` sigue siendo útil dentro de un método abstracto con cuerpo o en una rama que una subclase no debería alcanzar.

### `Protocol` y duck typing

El *duck typing* dice: si camina como pato y grazna como pato, es un pato. En Python, si un objeto tiene `curar()`, puedes usarlo aunque no herede de nada.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Curable(Protocol):
    nombre: str

    def curar(self, cantidad: int) -> int:
        ...


def curar_aliado(objetivo: Curable, cantidad: int) -> None:
    curado = objetivo.curar(cantidad)
    print(f"{objetivo.nombre} recupera {curado} PV")
```

Cualquier objeto con `nombre` y `curar()` funciona: un `Sacerdote`, una `Poción`, un `Altar`. No hay herencia ni registro. `runtime_checkable` permite usar `isinstance(obj, Curable)`, aunque solo comprueba que los métodos existan, no que las firmas sean correctas.

### Método plantilla

El patrón **método plantilla** fija el esqueleto de un algoritmo en la base y deja pasos abstractos a las hijas:

```python
class Personaje(ABC):
    @abstractmethod
    def atacar(self) -> int:
        ...

    @abstractmethod
    def gastar_recurso(self) -> None:
        ...

    def realizar_turno(self) -> int:
        dano = self.atacar()
        self.gastar_recurso()
        return dano
```

`realizar_turno()` no se sobrescribe: siempre hace lo mismo, en el mismo orden. Lo que cambia es cómo ataca y qué recurso gasta cada subclase. Es una forma elegante de reutilizar un flujo sin copiarlo.

:::warning
No conviertas la base en una lista de deseos. Si tiene doce métodos abstractos, cada subclase está obligada a implementar doce cosas, incluso las que no usa. Divide el contrato en piezas más pequeñas.
:::

## Código paso a paso

**Paso 1. Importar y declarar la base.**

```python
from abc import ABC, abstractmethod


class Personaje(ABC):
    def __init__(self, nombre: str, vida: int, ataque_base: int) -> None:
        self.nombre = nombre
        self.vida = vida
        self.ataque_base = ataque_base

    @abstractmethod
    def atacar(self) -> int:
        """Devuelve el daño del ataque de este personaje."""

    def recibir_dano(self, cantidad: int) -> None:
        self.vida = max(0, self.vida - cantidad)

    def esta_vivo(self) -> bool:
        return self.vida > 0
```

**Paso 2. Implementar el contrato en cada subclase.**

```python
class Guerrero(Personaje):
    def __init__(self, nombre: str, fuerza: int = 6) -> None:
        super().__init__(nombre, vida=120, ataque_base=10)
        self.fuerza = fuerza

    def atacar(self) -> int:
        return self.ataque_base + self.fuerza
```

Como el método abstracto no tiene cuerpo, la subclase usa los atributos concretos que sí heredó. Si quieres compartir la lógica base, dale cuerpo al método abstracto:

```python
class Personaje(ABC):
    @abstractmethod
    def atacar(self) -> int:
        return self.ataque_base
```

Entonces la hija puede ampliarlo con `super().atacar() + self.fuerza`. Ambas opciones son válidas; lo importante es no llamar a `super()` cuando el método no devuelve nada.

**Paso 3. Comprobar que la base no se instancia.**

```python
try:
    Personaje("Genérico", 100, 5)
except TypeError as error:
    print(f"Base no instanciable: {error}")
```

**Paso 4. Usar el método plantilla.**

```python
class Mago(Personaje):
    def atacar(self) -> int:
        if self.mana >= 10:
            self.mana -= 10
            return self.ataque_base + 15
        return self.ataque_base


for personaje in equipo:
    dano = personaje.realizar_turno()
    print(f"{personaje.nombre} causa {dano}")
```

El bucle no sabe qué subclase tiene delante. Solo confía en el contrato.

**Paso 5. Aceptar cualquier objeto curable.**

```python
def curar_equipo(objetivos: list[Curable], cantidad: int) -> None:
    for objetivo in objetivos:
        objetivo.curar(cantidad)
```

`list[Curable]` documenta la intención. En ejecución, Python acepta cualquier objeto con `curar()`; un verificador estático como el de VS Code comprobará la forma.

## Diagrama / modelo

```text
                 «contrato»
                  Personaje (ABC)
        nombre · vida · ataque_base
        ─────────────────────────
        atacar()          ← abstracto, obligatorio
        recibir_dano()    ← concreto, reutilizable
        realizar_turno()  ← plantilla: atacar + gastar
                    ▲
        ┌───────────┼───────────┐
    Guerrero       Mago      Arquero
    atacar()      atacar()   atacar()
    gastar()      gastar()   gastar()
```

Las subclases no pueden existir sin implementar `atacar()` y `gastar_recurso()`. La base aporta el flujo y el estado común.

## Errores comunes

1. **Olvidar heredar de `ABC`.** Una clase con `@abstractmethod` pero sin `ABC` no bloquea la instanciación; el decorador queda sin efecto.
2. **No implementar todos los métodos abstractos.** Al crear el objeto aparece un `TypeError` que nombra los métodos pendientes. Lee el mensaje completo.
3. **Llamar a `super().atacar()` cuando el abstracto no tiene cuerpo.** Devuelve `None` y el daño se vuelve `None`, o falla al sumar.
4. **Usar `isinstance()` con un `Protocol` sin `runtime_checkable`.** Lanza `TypeError: Instance and class checks can only be used with @runtime_checkable protocols`.
5. **Confundir comprobar la forma con comprobar la firma.** `runtime_checkable` verifica que el método exista, no que reciba los parámetros correctos.
6. **Crear una interfaz gigantesca.** Obliga a las subclases a implementar métodos que no necesitan.

:::error
`@abstractmethod` no impide heredar, solo impide instanciar. Puedes crear una subclase que siga siendo abstracta; simplemente tampoco podrás crear objetos de ella hasta completar el contrato.
:::

## Buenas prácticas

- Usa una clase abstracta cuando la base tenga **estado o comportamiento común** que valga la pena reutilizar.
- Si solo necesitas una forma, prefiere `Protocol`: no obliga a heredar.
- Mantén pocos métodos abstractos y con nombres claros.
- Documenta qué debe devolver cada método; el contrato incluye el tipo.
- Implementa el método plantilla en la base y deja abstractos solo los pasos variables.
- No uses `ABC` para clases de datos que nunca se van a especializar.

## Checklist de la semana

- [ ] Declaré una clase que hereda de `ABC`.
- [ ] Marqué al menos un método con `@abstractmethod`.
- [ ] Comprobé que la base lanza `TypeError` al instanciarse.
- [ ] Implementé el contrato en dos o tres subclases.
- [ ] Escribí una función que acepta un `Protocol` y probé con dos clases distintas.
- [ ] Identifiqué un método plantilla y expliqué qué pasos delega.

## Resumen

Una clase abstracta define un contrato y evita que se creen objetos incompletos. `ABC` y `@abstractmethod` hacen que Python bloquee la instanciación hasta que la subclase implemente lo obligatorio. La base puede aportar métodos concretos y un método plantilla que fija el orden del algoritmo. Para contratos basados solo en la forma, `Protocol` ofrece duck typing verificable sin herencia. `NotImplementedError` sigue existiendo como aviso manual, pero no reemplaza la garantía de `ABC`. La regla práctica: abstrae cuando quieras obligar, no cuando solo quieras reutilizar.

## Siguiente paso

En la semana 10 usarás estas bases para trabajar el **polimorfismo** a fondo: listas de objetos con distintos comportamientos, funciones que aceptan contratos y un duelo por turnos donde el mismo bucle gobierna a todos los personajes.
