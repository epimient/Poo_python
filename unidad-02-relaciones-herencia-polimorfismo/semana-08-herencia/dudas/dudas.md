# Dudas frecuentes — Semana 08

## ¿Herencia y composición son lo mismo?

No. La herencia declara que una clase **es un** caso de otra y hereda su estado y sus métodos. La composición declara que una clase **tiene** otra pieza y la usa desde un atributo.

```python
# Herencia: un Guerrero es un Personaje
class Guerrero(Personaje):
    pass

# Composición: un Personaje tiene un Inventario
class Personaje:
    def __init__(self) -> None:
        self.inventario = Inventario()
```

Si la frase «X es un Y» suena falsa, no heredes.

## ¿Para qué sirve `super()` exactamente?

Para ejecutar el método de la base sin nombrarla y seguir el MRO. Lo más común es inicializar la parte heredada:

```python
class Mago(Personaje):
    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, vida=80, ataque_base=6)
        self.mana = 30
```

También sirve para ampliar un método:

```python
def atacar(self) -> int:
    return super().atacar() + 15
```

No es obligatorio llamarlo, pero si la base guarda atributos que la hija necesita, omitirlo produce errores.

## Mi subclase lanza `AttributeError: 'Guerrero' object has no attribute 'nombre'`. ¿Qué pasó?

Casi siempre falta la llamada a `super().__init__()`.

```python
class Guerrero(Personaje):
    def __init__(self, nombre: str, fuerza: int) -> None:
        # Falta: super().__init__(nombre, vida=120, ataque_base=10)
        self.fuerza = fuerza
```

La subclase creó `fuerza`, pero nunca ejecutó el constructor de `Personaje`. Solución: llama a la base antes de asignar los atributos propios.

## ¿Puedo sobrescribir un método y a la vez conservar el del padre?

Sí. Sobrescribes el nombre y dentro llamas a `super()`:

```python
class Arquero(Personaje):
    def atacar(self) -> int:
        if self.flechas > 0:
            self.flechas -= 1
            return super().atacar() + 4
        return super().atacar()
```

Así conservas el contrato y añades la regla nueva. Si no llamas a `super()`, el comportamiento del padre queda reemplazado por completo.

## ¿Qué es el MRO y por qué debería mirarlo?

Es el *Method Resolution Order*: la lista ordenada de clases donde Python busca un método. Se consulta así:

```python
print(Guerrero.__mro__)
# (<class 'Guerrero'>, <class 'Personaje'>, <class 'object'>)
```

Cuando hay herencia múltiple, el MRO decide qué versión de un método se ejecuta. Si dos ramas definen `mover()` y no sabes cuál gana, el MRO te da la respuesta.

## ¿Por qué `D(B, C)` usa el método de `B` y no el de `C`?

Porque en el MRO `B` aparece antes que `C`. Python respeta el orden declarado y, cuando ambas ramas comparten una base, coloca esa base una sola vez al final.

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

El algoritmo C3 garantiza un orden coherente; no es una elección aleatoria.

## ¿Cuándo conviene usar `isinstance()`?

Cuando de verdad necesitas distinguir el tipo, por ejemplo para depurar, para serializar o para una validación puntual. No lo uses para decidir el comportamiento normal de una lista de objetos: para eso está el polimorfismo.

```python
# Innecesario si todos tienen atacar()
for p in equipo:
    if isinstance(p, Mago):
        p.atacar_con_mana()
    elif isinstance(p, Guerrero):
        p.atacar_con_espada()

# Mejor: todos sobrescriben atacar()
for p in equipo:
    p.atacar()
```

## ¿La herencia múltiple es mala?

No es mala por sí misma, pero complica el diseño. Úsala cuando las dos bases representen capacidades independientes y reales, por ejemplo `Volador` y `Nadador`. Evita jerarquías profundas y comprueba el MRO. Si solo quieres reutilizar código, composición suele ser más simple y flexible.
