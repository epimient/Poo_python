# Dudas frecuentes — Semana 04

## ¿Cuál es la diferencia entre un método normal, `@classmethod` y `@staticmethod`?

El método normal recibe `self` y trabaja con el estado de una instancia. `@classmethod` recibe `cls` y trabaja con la clase; se usa para fabricar objetos o leer configuración compartida. `@staticmethod` no recibe ni `self` ni `cls`: es una función agrupada por tema.

```python
class Personaje:
    def saludar(self) -> str:
        return f"Hola, soy {self.nombre}"

    @classmethod
    def desde_ficha(cls, ficha: str) -> "Personaje":
        nombre, hp = ficha.split(",")
        return cls(nombre.strip(), int(hp))

    @staticmethod
    def calcular_danio(ataque: int, defensa: int) -> int:
        return max(1, ataque - defensa)
```

Si el método necesita datos del objeto, normal. Si necesita crear una instancia o conocer la clase, `classmethod`. Si no necesita ninguno de los dos, `staticmethod` o una función del módulo.

## ¿`__init__` es el constructor?

En el uso cotidiano sí lo llamamos constructor, pero técnicamente es el inicializador. Python crea el objeto primero y después ejecuta `__init__` para llenar su estado. El método que realmente crea la instancia es `__new__`, que casi nunca necesitarás sobrescribir.

```python
class Personaje:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

aria = Personaje("Aria")  # __new__ crea, __init__ inicializa
```

Lo importante: `__init__` debe devolver `None`. Si devuelves otra cosa, Python lanza `TypeError`.

## ¿Cómo tengo varios constructores en Python?

No se sobrecarga `__init__` como en otros lenguajes. Se combinan valores por defecto con fábricas `@classmethod`. El constructor principal recibe los datos ya listos y cada fábrica se encarga de interpretar otro formato.

```python
class Personaje:
    def __init__(self, nombre: str, hp: int = 100, ataque: int = 10) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque

    @classmethod
    def aleatorio(cls, nombre: str) -> "Personaje":
        return cls(nombre, hp=80, ataque=12)

    @classmethod
    def desde_ficha(cls, ficha: str) -> "Personaje":
        nombre, hp, ataque = (parte.strip() for parte in ficha.split(","))
        return cls(nombre, int(hp), int(ataque))
```

Así `Personaje("Aria")`, `Personaje.aleatorio("Brom")` y `Personaje.desde_ficha("Cyd, 90, 14")` construyen objetos válidos sin duplicar la validación.

## ¿Por qué mi setter entra en recursión infinita?

Porque dentro de `@hp.setter` asignas a `self.hp`, que vuelve a llamar al mismo setter. El atributo real debe ser otro, normalmente `_hp`, y el setter escribe en él.

```python
# Incorrecto: RecursionError
@hp.setter
def hp(self, valor: int) -> None:
    self.hp = valor

# Correcto
@hp.setter
def hp(self, valor: int) -> None:
    if not 0 <= valor <= self.hp_max:
        raise ValueError("hp fuera de rango")
    self._hp = valor
```

Regla mental: el nombre de la propiedad es la puerta; el nombre con guion bajo es el cuarto donde se guarda el dato.

## ¿Los atributos con `_` y `__` son privados de verdad?

No. `_nombre` es una convención que dice “esto es interno, no lo uses desde fuera”. `__nombre` activa el name mangling: Python lo renombra a `_Clase__nombre`, así que sigue siendo accesible si conoces el truco. Ninguno de los dos impide el acceso; solo lo desaconsejan.

```python
class Cuenta:
    def __init__(self) -> None:
        self._saldo = 100
        self.__clave = "1234"

c = Cuenta()
print(c._saldo)              # 100
print(c._Cuenta__clave)      # 1234
# print(c.__clave)           # AttributeError
```

La protección real es no ofrecer métodos públicos que permitan romper las reglas. El guion bajo comunica intención; la validación hace el trabajo.

## ¿Uso `@property` o escribo métodos `get_saldo` y `set_saldo`?

En Python se prefiere `@property`: el uso queda como un atributo normal (`cuenta.saldo`) y, si más adelante necesitas validar, cambias la implementación sin romper a quien ya usaba el objeto.

```python
class Cuenta:
    def __init__(self, saldo: float) -> None:
        self._saldo = saldo

    @property
    def saldo(self) -> float:
        return self._saldo
```

Si el dato es de solo lectura, define la propiedad sin setter. Si necesitas una operación con efecto —depositar, retirar—, usa un método con verbo: `cuenta.depositar(50)`, no `cuenta.saldo = 50`.

## ¿Cuándo lanzo `ValueError` y cuándo `TypeError`?

`TypeError` cuando el tipo de dato es incompatible: pasaste un `str` donde se espera un número. `ValueError` cuando el tipo es correcto pero el valor no cumple la regla: un hp negativo, un retiro mayor que el saldo, una ficha con menos campos.

```python
def retirar(monto: float) -> None:
    if not isinstance(monto, (int, float)):
        raise TypeError("El monto debe ser un número.")
    if monto <= 0:
        raise ValueError("El monto debe ser mayor que cero.")
    if monto > self._saldo:
        raise ValueError("Saldo insuficiente.")
```

Un mensaje útil dice qué se esperaba y qué llegó. `raise ValueError("error")` no ayuda a nadie.

## ¿Qué diferencia hay entre `__str__` y `__repr__`?

`__str__` es la versión legible para el usuario y la usa `print()`. `__repr__` es la versión técnica para depurar y la usan `repr()`, la consola interactiva y los contenedores. Si solo defines `__repr__`, `str()` lo reutiliza; si solo defines `__str__`, la depuración sigue mostrando la dirección de memoria.

```python
def __str__(self) -> str:
    return f"Aria ({self.hp}/{self.hp_max} hp)"

def __repr__(self) -> str:
    return f"Personaje(nombre={self.nombre!r}, hp={self.hp}, hp_max={self.hp_max})"
```

Un buen `__repr__` se parece al código que reconstruiría el objeto. Ambos deben devolver un `str`; si devuelven otra cosa, Python lanza `TypeError`.
