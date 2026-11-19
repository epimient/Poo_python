# Dudas frecuentes — Semana 10

## ¿Polimorfismo es lo mismo que herencia?

No. La herencia es una forma de conseguir polimorfismo, pero no la única. También puedes lograr que objetos de clases sin parentesco respondan al mismo mensaje mediante duck typing o un `Protocol`. Lo esencial es que el cliente envíe un mensaje común y cada objeto lo resuelva a su manera.

## ¿Sobrescribir es lo mismo que sobrecargar?

No. **Sobrescribir** es redefinir en una subclase un método que ya existe en el padre, con el mismo nombre y una firma compatible. **Sobrecargar** sería tener varias versiones del mismo método con parámetros distintos; Python no lo hace por tipos en tiempo de ejecución. Si necesitas variantes, usa valores por defecto, `*args` o `singledispatch`.

## ¿Cuándo uso una clase abstracta y cuándo `Protocol`?

Usa `ABC` cuando quieras compartir estado o lógica y obligar a las subclases a implementar un contrato. Usa `Protocol` cuando solo te interese la forma del objeto y no quieras obligarlo a heredar de nada:

```python
from typing import Protocol


class Curador(Protocol):
    def curar(self, cantidad: int) -> int:
        ...


def aplicar_curacion(objeto: Curador, cantidad: int) -> None:
    print(objeto.curar(cantidad))
```

`Protocol` documenta el contrato para el editor y para el equipo; en ejecución, cualquier objeto con `curar()` funciona.

## ¿Duck typing significa que cualquier objeto sirve?

No. Significa que Python no exige una relación de herencia, pero el objeto debe responder a los mensajes que usas. Si llamas `personaje.atacar()` y el objeto no tiene `atacar()`, obtendrás `AttributeError`. El contrato sigue existiendo: solo que es implícito. Documéntalo con un `Protocol`, un docstring o pruebas.

## ¿Por qué está mal usar `isinstance` en el bucle de combate?

Porque el bucle necesita conocer cada subclase y se rompe al agregar una nueva. Esto es un diseño cerrado a la extensión:

```python
if isinstance(personaje, Guerrero):
    personaje.golpe_espada()
elif isinstance(personaje, Mago):
    personaje.lanzar_hechizo()
```

La alternativa es mover la decisión a cada clase y dejar el bucle estable:

```python
for personaje in personajes:
    personaje.atacar(objetivo)
```

## ¿Entonces `isinstance` nunca se usa?

Sí se usa, pero en los bordes del sistema: validar datos de entrada, implementar `__add__` o recibir un parámetro que puede venir en varios formatos. El problema es usarlo en la lógica central para elegir comportamiento entre subclases. Una cadena de `isinstance` en el corazón del programa suele indicar que falta un contrato.

## ¿Cómo funciona `singledispatch`?

Registra una implementación distinta según el tipo del **primer** argumento. La función base actúa como respaldo:

```python
from functools import singledispatch


@singledispatch
def describir(dano: object) -> str:
    return "Daño desconocido"


@describir.register
def _(dano: DanoFisico) -> str:
    return "Daño físico"


@describir.register
def _(dano: DanoMagico) -> str:
    return "Daño mágico"
```

Úsalo cuando las variantes dependen del tipo del dato (tipos de daño, formatos de archivo, monedas) y no del personaje que ejecuta la acción.

## ¿Qué dunder necesito para cada operación?

| Quieres escribir | Implementa |
|---|---|
| `len(inventario)` | `__len__` |
| `for objeto in inventario` | `__iter__` |
| `"Poción" in inventario` | `__contains__` |
| `inventario + otro` | `__add__` |
| `print(inventario)` | `__str__` |
| `inventario[0]` | `__getitem__` |

Si `__add__` recibe un operando incompatible, devuelve `NotImplemented`; no lances una excepción ni devuelvas `None`.

## ¿Cómo compruebo que mi diseño es realmente polimórfico?

Agrega una subclase nueva y observa cuántos archivos tocas. Si solo creas la clase y el motor sigue funcionando, el diseño es polimórfico. Si tienes que editar el bucle, agregar un `elif` o importar la clase nueva en `Combate`, todavía depende de los tipos concretos. Esa prueba es más útil que cualquier definición memorizada.
