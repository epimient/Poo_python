# Semana 08 — Herencia

> Una clase base bien diseñada evita que copies el mismo código tres veces.

## Objetivos de aprendizaje

- Reconocer una relación **es-un** y distinguirla de una relación **tiene-un**.
- Crear una clase base y varias subclases que reutilicen su comportamiento.
- Inicializar la base con `super().__init__()` sin duplicar asignaciones.
- Sobrescribir métodos y ampliar el comportamiento del padre.
- Consultar jerarquías con `isinstance()`, `issubclass()` y `Clase.__mro__`.
- Entender la herencia múltiple, el problema del diamante y cuándo conviene usar composición.

:::info
Esta semana construyes una jerarquía de personajes. La idea no es escribir más clases, sino escribir **menos código repetido** y lograr que un mismo método funcione con tipos distintos.
:::

## ¿Por qué importa?

Imagina que estás programando el combate de un videojuego. Tienes un guerrero, un mago y un arquero. Los tres tienen nombre, vida y un ataque básico. También los tres reciben daño y pueden morir. Si escribes tres clases independientes, terminarás copiando el mismo bloque de inicialización y el mismo método `recibir_dano()` tres veces.

El problema aparece cuando cambia una regla: decides que al llegar a cero de vida el personaje debe quedar marcado como derrotado. Ahora tienes que corregir tres archivos y rezar para no olvidar ninguno. En una banca ocurre lo mismo con una cuenta de ahorros y una cuenta corriente: comparten saldo, titular y depósitos, pero difieren en comisiones y retiros.

La herencia resuelve ese problema: describes lo común una sola vez en una clase base y cada subclase aporta lo suyo. El código que ya funcionaba sigue funcionando, y los cambios se hacen en un único lugar.

## Concepto central

La herencia modela una relación **es-un**. Un `Guerrero` **es un** `Personaje`; un `Mago` **es un** `Personaje`. En cambio, un `Personaje` **tiene un** inventario: eso es composición, no herencia.

```python
class Personaje:
    def __init__(self, nombre: str, vida: int) -> None:
        self.nombre = nombre
        self.vida = vida

    def atacar(self) -> int:
        return 5


class Guerrero(Personaje):          # Guerrero es-un Personaje
    def __init__(self, nombre: str, vida: int, fuerza: int) -> None:
        super().__init__(nombre, vida)   # inicializa la parte Personaje
        self.fuerza = fuerza

    def atacar(self) -> int:             # sobrescribe el método
        return super().atacar() + self.fuerza
```

Tres piezas aparecen siempre:

| Pieza | Qué hace |
|---|---|
| `class Guerrero(Personaje)` | Declara que `Guerrero` hereda de `Personaje`. |
| `super().__init__(...)` | Inicializa el estado que pertenece a la base. |
| `def atacar(self)` en la hija | Sobrescribe la versión heredada. |

`super()` no significa “el padre” en abstracto: significa “el siguiente método en el **MRO**”, el orden en que Python busca métodos. Por eso es la forma correcta de colaborar con la base, incluso con herencia múltiple.

### Sobrescribir sin romper

Una subclase puede reemplazar por completo un método o ampliarlo llamando a `super()`. Ambas opciones son válidas si respetas el contrato: el mismo nombre, los mismos parámetros y un valor de retorno compatible. Si `Personaje.atacar()` devuelve un `int`, `Mago.atacar()` también debe devolver un `int`.

### Consultar la jerarquía

```python
g = Guerrero("Ragnar", 120, 8)
print(isinstance(g, Guerrero))    # True
print(isinstance(g, Personaje))   # True: un Guerrero también es Personaje
print(issubclass(Guerrero, Personaje))  # True
```

`isinstance()` mira el objeto; `issubclass()` mira la clase. El segundo argumento puede ser una tupla: `isinstance(x, (Mago, Arquero))`.

El MRO se consulta directamente:

```python
print(Guerrero.__mro__)
# (<class 'Guerrero'>, <class 'Personaje'>, <class 'object'>)
```

### Herencia múltiple y el diamante

Python permite heredar de varias clases:

```python
class Volador:
    def mover(self) -> str:
        return "vuela"


class Nadador:
    def mover(self) -> str:
        return "nada"


class Pato(Volador, Nadador):
    pass
```

`Pato().mover()` devuelve `"vuela"` porque `Volador` aparece primero en el MRO. El **problema del diamante** surge cuando dos ramas heredan de una misma base:

```python
class A:
    def saludar(self) -> str:
        return "A"


class B(A):
    pass


class C(A):
    pass


class D(B, C):
    pass


print(D.__mro__)   # D, B, C, A, object
```

Python resuelve el conflicto con el algoritmo C3 y garantiza que `A` aparezca **una sola vez**. La consecuencia práctica: si `B` y `C` usan `super().__init__()` de forma cooperativa, la cadena se ejecuta una vez y sin duplicar estado. Si en cambio llaman a `A.__init__()` directamente, puedes inicializar dos veces. Esa es la razón por la que se recomienda `super()`.

### Herencia o composición

| Criterio | Herencia | Composición |
|---|---|---|
| Relación | es-un | tiene-un |
| Acoplamiento | Alto: la hija depende de la base | Bajo: solo usa una interfaz pública |
| Cambiar en caliente | No | Sí: puedes sustituir la pieza |
| Cuándo usarla | Jerarquía estable y real | Variantes de comportamiento, piezas intercambiables |

:::warning
No heredes solo para reutilizar un método. Si un `Auto` necesita `encender()`, pero no es un `Motor`, usa composición: `Auto` **tiene un** `Motor`.
:::

## Código paso a paso

**Paso 1. La base concentra lo común.**

```python
class Personaje:
    def __init__(self, nombre: str, vida: int, ataque_base: int) -> None:
        self.nombre = nombre
        self.vida = vida
        self.ataque_base = ataque_base

    def atacar(self) -> int:
        return self.ataque_base

    def recibir_dano(self, cantidad: int) -> None:
        self.vida = max(0, self.vida - cantidad)
```

**Paso 2. El guerrero añade fuerza y reutiliza la base.**

```python
class Guerrero(Personaje):
    def __init__(self, nombre: str, fuerza: int) -> None:
        super().__init__(nombre, vida=120, ataque_base=10)
        self.fuerza = fuerza

    def atacar(self) -> int:
        return super().atacar() + self.fuerza
```

**Paso 3. Cada subclase sobrescribe con su propia regla.**

```python
class Mago(Personaje):
    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, vida=80, ataque_base=6)
        self.mana = 30

    def atacar(self) -> int:
        if self.mana >= 10:
            self.mana -= 10
            return super().atacar() + 15
        return super().atacar() // 2
```

**Paso 4. Un solo bucle trata a todos igual.**

```python
equipo: list[Personaje] = [Guerrero("Ragnar", 8), Mago("Morgana")]
for personaje in equipo:
    print(f"{personaje.nombre} ataca por {personaje.atacar()}")
```

Ese bucle es la recompensa de la herencia: no pregunta de qué clase es cada objeto. Solo sabe que todos responden a `atacar()`.

**Paso 5. Comprobar tipos y orden de resolución.**

```python
print(isinstance(equipo[0], Personaje))   # True
print(issubclass(Mago, Personaje))        # True
print(Mago.__mro__)
```

## Diagrama / modelo

```text
              Personaje
        nombre · vida · ataque_base
        atacar() · recibir_dano()
                 ▲
      ┌──────────┼──────────┐
      │          │          │
  Guerrero     Mago      Arquero
  fuerza       maná      flechas
  atacar()     atacar()  atacar()
```

Cada flecha se lee “es un”. Los atributos y métodos del recuadro superior se heredan; los de abajo se añaden o se sobrescriben.

## Errores comunes

1. **Olvidar `super().__init__()`.** La subclase crea `self.fuerza`, pero `self.nombre` nunca existe y aparece un `AttributeError` al imprimir.
2. **Sobrescribir con otra firma.** Cambiar `atacar(self)` por `atacar(self, objetivo)` rompe el código que usaba la base de forma genérica.
3. **Heredar por conveniencia.** `class Tienda(Inventario)` porque ambos tienen listas no es una relación es-un; es composición disfrazada.
4. **Duplicar la inicialización de la base.** Llamar a `Personaje.__init__(self, ...)` dentro de una jerarquía múltiple puede ejecutar la base dos veces.
5. **Usar `isinstance()` para todo.** Si necesitas preguntar por cada subclase para decidir qué hacer, el polimorfismo no está haciendo su trabajo.

:::error
Un error silencioso: definir `atacar` con un nombre distinto, como `Atacar` o `atacar_fisico`, y creer que estás sobrescribiendo. Python crea un método nuevo y el original sigue respondiendo.
:::

## Buenas prácticas

- Mantén la clase base pequeña y coherente: solo lo que **todos** los hijos comparten.
- Usa `super().__init__()` siempre; no repitas asignaciones del padre.
- Documenta el contrato de los métodos que se pueden sobrescribir.
- Respeta el principio de sustitución: cualquier subclase debe poder usarse donde se espera la base.
- Prefiere composición cuando la relación no sea claramente es-un.
- Comprueba el MRO cuando uses herencia múltiple; si no lo entiendes, probablemente no la necesitas.

## Checklist de la semana

- [ ] Sé explicar la diferencia entre es-un y tiene-un con un ejemplo propio.
- [ ] Creé una clase base y al menos dos subclases.
- [ ] Usé `super().__init__()` en todas las subclases.
- [ ] Sobrescribí un método y lo llamé desde una lista heterogénea.
- [ ] Consulté `isinstance()`, `issubclass()` y `__mro__`.
- [ ] Identifiqué un caso donde composición es mejor que herencia.

## Resumen

La herencia permite declarar que una clase **es un** caso particular de otra y reutilizar su estado y comportamiento. La subclase añade atributos propios, inicializa la base con `super().__init__()` y sobrescribe métodos cuando necesita una regla distinta. Con una lista de la clase base puedes tratar a todos los personajes por igual. `isinstance()` y `issubclass()` te ayudan a inspeccionar la jerarquía, y `__mro__` revela el orden de búsqueda. La herencia múltiple existe, pero se usa con cuidado: el diamante se resuelve con C3 y con llamadas cooperativas a `super()`. Cuando la relación no sea es-un, la composición suele ser la decisión más sana.

## Siguiente paso

En la semana 09 darás el paso siguiente: convertir `Personaje` en una **clase abstracta** que no se pueda instanciar y que obligue a cada subclase a implementar `atacar()`. Después conocerás `Protocol`, la alternativa flexible para contratos de comportamiento.
