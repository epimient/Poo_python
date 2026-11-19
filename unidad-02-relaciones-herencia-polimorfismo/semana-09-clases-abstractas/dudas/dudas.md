# Dudas frecuentes — Semana 09

## ¿Por qué no puedo instanciar `Personaje` si tiene constructor?

Porque hereda de `ABC` y tiene al menos un método abstracto sin implementar. El constructor existe, pero el objeto estaría incompleto: la base prometió `atacar()` y no puede cumplirlo.

```python
from abc import ABC, abstractmethod

class Personaje(ABC):
    @abstractmethod
    def atacar(self) -> int:
        ...

Personaje()   # TypeError
```

La solución no es quitar `ABC`, sino crear una subclase concreta que implemente `atacar()`.

## ¿Qué diferencia hay entre `@abstractmethod` y `NotImplementedError`?

`@abstractmethod` **impide crear** el objeto hasta que el contrato esté completo. `NotImplementedError` solo lanza un error cuando alguien llama al método.

```python
# Falla al instanciar: mejor para detectar el problema temprano
class A(ABC):
    @abstractmethod
    def ejecutar(self) -> None:
        ...

# Falla al ejecutar: el objeto se crea sin problema
class B:
    def ejecutar(self) -> None:
        raise NotImplementedError("Falta implementar")
```

Usa `NotImplementedError` en un método abstracto con cuerpo o en una rama que una subclase no debería alcanzar; no como sustituto de `ABC`.

## ¿Un método abstracto puede tener código?

Sí. Puede tener una implementación que las subclases reutilicen con `super()`.

```python
class Personaje(ABC):
    def __init__(self, ataque_base: int) -> None:
        self.ataque_base = ataque_base

    @abstractmethod
    def atacar(self) -> int:
        return self.ataque_base
```

La subclase sigue obligada a implementar `atacar()`, pero puede apoyarse en la base:

```python
class Guerrero(Personaje):
    def atacar(self) -> int:
        return super().atacar() + 8
```

Si el abstracto no tiene cuerpo y llamas a `super().atacar()`, recibirás `None` y el cálculo fallará.

## ¿Qué pasa si una subclase no implementa todos los métodos abstractos?

Sigue siendo abstracta. No se puede instanciar y el `TypeError` indica qué métodos faltan.

```python
class Mago(Personaje):
    pass

Mago()   # TypeError: ... abstract method 'atacar'
```

Esto también aplica a una subclase intermedia: si hereda de otra abstracta y no completa el contrato, la cadena sigue bloqueada.

## ¿Uso `ABC` o `Protocol`?

- Usa **`ABC`** cuando quieras una base con estado o comportamiento común y una relación clara de herencia.
- Usa **`Protocol`** cuando solo te importe que el objeto tenga ciertos métodos o atributos, sin obligarlo a heredar.

```python
# ABC: comparte vida y recibir_dano
class Personaje(ABC):
    ...

# Protocol: solo exige curar()
class Curable(Protocol):
    def curar(self, cantidad: int) -> int:
        ...
```

Regla práctica: si la base aporta código, `ABC`; si solo describe una forma, `Protocol`.

## ¿Qué hace `@runtime_checkable` y qué NO valida?

Permite usar `isinstance()` y `issubclass()` con un `Protocol`.

```python
@runtime_checkable
class Curable(Protocol):
    def curar(self, cantidad: int) -> int:
        ...

isinstance(obj, Curable)   # True si obj tiene curar
```

No valida tipos de parámetros ni de retorno. Un método `curar(self, texto: str)` también pasaría la comprobación. Para verificar firmas necesitas un analizador estático o pruebas.

## ¿Qué es un método plantilla?

Un método concreto de la base que define el orden de un algoritmo y llama a pasos abstractos.

```python
class Personaje(ABC):
    @abstractmethod
    def atacar(self) -> int:
        ...

    def realizar_turno(self, enemigo: "Personaje") -> int:
        dano = self.atacar()
        enemigo.recibir_dano(dano)
        return dano
```

`realizar_turno()` no cambia entre subclases; lo que cambia es `atacar()`. Así evitas copiar el mismo flujo en cada hija.

## ¿Una clase abstracta puede tener atributos y métodos concretos?

Sí, y es lo normal. `ABC` no obliga a que todo sea abstracto. Puedes tener constructor, atributos, métodos utilitarios y solo uno o dos métodos abstractos.

```python
class Personaje(ABC):
    def __init__(self, nombre: str, vida: int) -> None:
        self.nombre = nombre
        self.vida = vida

    def esta_vivo(self) -> bool:
        return self.vida > 0

    @abstractmethod
    def atacar(self) -> int:
        ...
```

Si todos los métodos fueran abstractos y sin estado, estarías modelando una interfaz, no una base con comportamiento compartido.
