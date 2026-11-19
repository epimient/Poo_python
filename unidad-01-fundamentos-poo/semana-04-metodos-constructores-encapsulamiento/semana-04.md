# Semana 04 — Métodos, constructores y encapsulamiento

> Un objeto sano no permite que lo dejen en un estado imposible.

## Objetivos de aprendizaje

- Escribir métodos de instancia que lean y modifiquen el estado del objeto.
- Definir constructores con valores por defecto y crear fábricas con `@classmethod`.
- Usar `@staticmethod` para utilidades que no dependen del estado.
- Aplicar atributos protegidos `_`, privados `__` y entender el name mangling.
- Exponer y validar atributos con `@property` y setters.
- Implementar `__str__` y `__repr__` con propósitos distintos.
- Lanzar `ValueError` cuando un valor rompe una regla del dominio.

## ¿Por qué importa?

En la Semana 03 tu clase `Personaje` aceptaba cualquier valor. Podías crear un personaje con `hp = -50`, curarlo hasta `hp = 300` o atacar cuando ya estaba derrotado. Nada en el código impedía ese estado absurdo: la clase era un contenedor de datos, no un modelo con reglas.

Lo mismo pasa en un banco. Si el saldo es un atributo público, cualquier parte del programa puede escribir `cuenta.saldo = -1000000`. El error no aparece donde se comete, sino tres pantallas después, cuando los totales no cuadran.

:::warning
Un objeto que acepta datos inválidos es una bomba de tiempo. Cuanto antes falla y más claro es el mensaje, más barato resulta el arreglo.
:::

El encapsulamiento no consiste en esconder todo por deporte. Consiste en que el objeto sea el único responsable de mantener sus reglas: la vida entre `0` y el máximo, el saldo nunca negativo, el nombre no vacío.

## Concepto central

Un **método de instancia** es una función que vive dentro de la clase y recibe `self`. Puede leer atributos, modificarlos y devolver un resultado. Mientras los atributos son el estado, los métodos son el comportamiento.

```python
class Personaje:
    def __init__(self, nombre: str, hp: int = 100) -> None:
        self.nombre = nombre
        self.hp = hp

    def saludar(self) -> str:
        return f"Soy {self.nombre} y tengo {self.hp} hp."
```

`aria.saludar()` ejecuta el método con `self = aria`. No hace falta pasar el objeto: Python lo enlaza solo. Ese proceso se llama *binding* y es la razón por la que `Personaje.saludar(aria)` y `aria.saludar()` producen lo mismo.

### Constructores con valores por defecto

`__init__` puede declarar valores por defecto para que crear un objeto común sea corto:

```python
class Personaje:
    MAX_HP = 100

    def __init__(self, nombre: str, hp: int = MAX_HP, ataque: int = 10) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque


brom = Personaje("Brom")              # hp 100, ataque 10
aria = Personaje("Aria", 80, 18)      # hp 80, ataque 18
```

Los valores por defecto deben ser inmutables. Un `def __init__(self, inventario: list[str] = [])` comparte la misma lista entre todas las instancias, igual que el error de la semana pasada. La solución es usar `None` y crear la lista dentro:

```python
def __init__(self, nombre: str, inventario: list[str] | None = None) -> None:
    self.nombre = nombre
    self.inventario = [] if inventario is None else list(inventario)
```

### `@classmethod` como fábrica

A veces quieres construir un objeto desde otro formato: una línea de texto, un registro de la base de datos o una configuración. Un `@classmethod` recibe la clase (`cls`) en lugar de la instancia y devuelve un objeto ya armado.

```python
class Personaje:
    def __init__(self, nombre: str, hp: int, ataque: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque

    @classmethod
    def desde_ficha(cls, ficha: str) -> "Personaje":
        nombre, hp, ataque = (parte.strip() for parte in ficha.split(","))
        return cls(nombre, int(hp), int(ataque))


brom = Personaje.desde_ficha("Brom, 120, 15")
```

La ventaja de `cls(...)` sobre `Personaje(...)` es que una subclase que herede `desde_ficha` construirá su propio tipo, no siempre `Personaje`.

### `@staticmethod`

Un método estático no recibe `self` ni `cls`: es una función relacionada con la clase por tema, no por estado. Sirve para cálculos auxiliares.

```python
class Personaje:
    @staticmethod
    def calcular_danio(ataque: int, defensa: int) -> int:
        return max(1, ataque - defensa)


print(Personaje.calcular_danio(18, 4))  # 14
```

Si no usa `self` ni `cls` y tampoco toca atributos de la clase, un `@staticmethod` es honesto. Si no tiene relación con el dominio de la clase, mejor una función suelta en el módulo.

| Decorador | Primer parámetro | Puede tocar el objeto | Uso típico |
|---|---|---|---|
| método normal | `self` | Sí | atacar, curar, depositar |
| `@classmethod` | `cls` | No, pero crea instancias | fábricas, configuración |
| `@staticmethod` | ninguno | No | cálculos y validaciones puras |

### Protegido, privado y name mangling

Python no tiene modificadores de acceso como otros lenguajes. Usa convenciones:

- `nombre`: público, parte de la interfaz estable.
- `_nombre`: protegido por convención; puede usarse en subclases, pero no desde fuera.
- `__nombre`: privado por convención; Python lo renombra a `_Clase__nombre` (name mangling).

```python
class CuentaBancaria:
    def __init__(self, titular: str, saldo: float) -> None:
        self.titular = titular
        self._saldo = saldo        # protegido
        self.__clave = "0000"      # nombre mangled

cuenta = CuentaBancaria("Ada", 250.0)
print(cuenta._saldo)               # 250.0 (funciona, pero no deberías)
print(cuenta._CuentaBancaria__clave)  # "0000" (mangling)
# print(cuenta.__clave)            # AttributeError
```

El name mangling no es seguridad: es una señal de “no toques esto” y evita choques de nombres entre clases. La verdadera protección está en no ofrecer una vía pública para romper el estado.

### `@property`: acceso controlado

Una propiedad permite leer un atributo con sintaxis normal, pero ejecutando un método. Así puedes validar, calcular o transformar sin cambiar la forma en que se usa el objeto.

```python
class Personaje:
    def __init__(self, nombre: str, hp_max: int = 100) -> None:
        self.nombre = nombre
        self.hp_max = hp_max
        self._hp = hp_max

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("El hp debe ser entero.")
        if not 0 <= valor <= self.hp_max:
            raise ValueError(f"El hp debe estar entre 0 y {self.hp_max}.")
        self._hp = valor
```

Ahora `aria.hp = 500` lanza `ValueError` y `aria.hp = -1` también. El atributo real es `_hp`; `hp` es la puerta de entrada con reglas. Un setter no debe devolver nada: `return` en un setter se ignora y confunde.

:::info
Dentro del setter escribe `self._hp = valor`, nunca `self.hp = valor`. Lo segundo vuelve a llamar al setter y provoca una recursión infinita hasta `RecursionError`.
:::

### `__str__`, `__repr__` y `ValueError`

`__str__` devuelve la versión legible para el usuario; `print(objeto)` la usa. `__repr__` devuelve la versión técnica para depurar y debería parecerse al código que reconstruye el objeto.

```python
def __str__(self) -> str:
    return f"{self.nombre} ({self.hp}/{self.hp_max} hp)"

def __repr__(self) -> str:
    return f"Personaje(nombre={self.nombre!r}, hp={self._hp}, hp_max={self.hp_max})"
```

`ValueError` se lanza cuando el tipo es correcto pero el valor no cumple la regla: un hp negativo, un retiro mayor que el saldo, una ficha con menos campos. Para un tipo equivocado —pasar un texto donde va un número— `TypeError` es más preciso.

## Código paso a paso

**Paso 1. Métodos que cambian el estado.** Sin validación todavía, para ver el problema.

```python
class Personaje:
    def __init__(self, nombre: str, hp: int = 100) -> None:
        self.nombre = nombre
        self.hp = hp

    def recibir_danio(self, cantidad: int) -> int:
        self.hp -= cantidad
        return cantidad

aria = Personaje("Aria", 10)
aria.recibir_danio(50)
print(aria.hp)  # -40: estado imposible
```

**Paso 2. Cierra la puerta con una propiedad.** El daño se acota en el método y el hp se valida en el setter.

```python
class Personaje:
    def __init__(self, nombre: str, hp_max: int = 100) -> None:
        self.nombre = nombre
        self.hp_max = hp_max
        self._hp = hp_max

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, valor: int) -> None:
        if not 0 <= valor <= self.hp_max:
            raise ValueError(f"hp fuera de rango: {valor}")
        self._hp = valor

    def recibir_danio(self, cantidad: int) -> int:
        antes = self._hp
        self.hp = max(0, self._hp - cantidad)
        return antes - self._hp
```

**Paso 3. Añade una fábrica y una utilidad.** `desde_ficha` valida el formato y `calcular_danio` concentra la fórmula.

```python
    @classmethod
    def desde_ficha(cls, ficha: str) -> "Personaje":
        partes = [parte.strip() for parte in ficha.split(",")]
        if len(partes) != 2:
            raise ValueError("Formato esperado: 'Nombre,hp_max'.")
        return cls(partes[0], int(partes[1]))

    @staticmethod
    def calcular_danio(ataque: int, defensa: int) -> int:
        return max(1, ataque - defensa)
```

**Paso 4. Aplica lo mismo a una cuenta.** El saldo solo cambia por operaciones válidas y cada movimiento queda registrado.

```python
class CuentaBancaria:
    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        if not titular.strip():
            raise ValueError("El titular no puede estar vacío.")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.titular = titular.strip()
        self._saldo = round(saldo_inicial, 2)
        self._historial: list[str] = []

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        self._saldo = round(self._saldo + monto, 2)
        self._historial.append(f"Depósito: +{monto:.2f}")

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente.")
        self._saldo = round(self._saldo - monto, 2)
        self._historial.append(f"Retiro: -{monto:.2f}")
```

**Paso 5. Da una representación decente.** `print` usa `__str__`; la consola interactiva y `repr()` usan `__repr__`.

```python
    def __str__(self) -> str:
        return f"Cuenta de {self.titular}: ${self._saldo:,.2f}"

    def __repr__(self) -> str:
        return f"CuentaBancaria(titular={self.titular!r}, saldo={self._saldo:.2f})"
```

## Diagrama / modelo

```text
Estado válido de un Personaje
        recibir_danio(x)
   hp_max ───────────────► 0
      ▲                    │
      │      curar(x)      │
      └────────────────────┘
        [0, hp_max] siempre

Setter hp  ──► valida tipo ──► valida rango ──► _hp
                                   │
                                   └── ValueError si falla
```

El atributo `_hp` es el dato; `hp` es la puerta; `recibir_danio` y `curar` son las operaciones que mueven el estado dentro de los límites. Ninguna ruta pública permite salir del intervalo.

## Errores comunes

**Recursión en el setter.** `self.hp = valor` dentro de `@hp.setter` se llama a sí mismo. Usa `self._hp = valor`.

**Validar después de asignar.** Si primero haces `self._hp = valor` y luego compruebas el rango, el objeto ya quedó inválido. Valida antes de escribir.

**Usar un mutable como valor por defecto.** `def __init__(self, items: list[str] = [])` comparte la lista. Usa `None`.

**Devolver algo desde un setter.** El valor de retorno se ignora; si quieres informar, lanza una excepción o expón otro método.

**Confundir `__str__` con `__repr__`.** `__str__` es para personas; `__repr__` para depuración. Si solo defines uno, define `__repr__`: `str()` cae en él cuando falta `__str__`.

**Creer que `__` es privado de verdad.** Se puede acceder con `_Clase__atributo`. Es una convención, no un candado. La protección real es no exponer operaciones que rompan las reglas.

**Capturar la excepción y no hacer nada.** Si `try/except ValueError: pass` oculta el error, el estado queda a medias. En el demo se captura para mostrar el mensaje, no para ignorarlo.

:::error
`__str__` y `__repr__` deben devolver un `str`. Si devuelves un número o `None`, Python lanza `TypeError: __str__ returned non-string`.
:::

## Buenas prácticas

- Valida en el punto de entrada: `__init__` y setters, no en cada uso.
- Un setter, una regla clara; los mensajes deben decir qué se esperaba y qué llegó.
- Usa `_` para detalles internos y `__` solo cuando quieras evitar colisiones o señalar fuertemente que no se toque.
- Prefiere propiedades de solo lectura (sin setter) para datos derivados como `vivo`, `saldo` o `total`.
- Mantén los métodos pequeños y con retorno útil: cuánto daño se aplicó, cuánto se retiró.
- Implementa `__repr__` siempre y `__str__` cuando haya una representación para el usuario.
- No uses `print` dentro de la lógica de la clase; devuelve datos y deja que el demo imprima.

## Checklist de la semana

- [ ] Escribo métodos que reciben `self` y modifican el estado del objeto.
- [ ] Creo objetos con valores por defecto sin compartir mutables.
- [ ] Implemento una fábrica con `@classmethod` y explico qué recibe `cls`.
- [ ] Uso `@staticmethod` para un cálculo que no necesita estado.
- [ ] Distingo `_atributo` de `__atributo` y sé qué hace el name mangling.
- [ ] Valido con `@property` y lanza `ValueError` cuando corresponde.
- [ ] Defino `__str__` y `__repr__` con propósitos diferentes.
- [ ] Mis dos scripts de la semana se ejecutan con `python3` sin errores.

## Resumen

Los métodos convierten datos en comportamiento. El constructor puede tener valores por defecto, pero nunca mutables compartidos. `@classmethod` construye objetos desde otros formatos y `@staticmethod` agrupa utilidades sin estado. El encapsulamiento protege las reglas del dominio: `_` y `__` son señales, y `@property` con setters validados es la herramienta concreta. `ValueError` comunica que un valor rompe una regla, mientras `__str__` y `__repr__` hacen que el objeto se explique al usuario y a quien depura. Con esto tus clases ya no son contenedores: son modelos que se defienden.

## Siguiente paso

La Semana 05 es la evaluación de la unidad: construirás el **creador de personajes RPG** en consola, con atributos, métodos, validaciones y una ficha final bien presentada. Llega con `combate_basico.py` y `cuenta_bancaria.py` entendidos y ejecutando; el proyecto reutiliza exactamente estas piezas.
