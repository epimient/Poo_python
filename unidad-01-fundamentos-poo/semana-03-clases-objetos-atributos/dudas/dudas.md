# Dudas frecuentes — Semana 03

## ¿Cuál es la diferencia entre una clase y un objeto?

La clase es la definición del tipo: describe qué atributos tendrá cada objeto. El objeto es una instancia concreta creada a partir de esa clase, con sus propios valores en memoria.

```python
class Personaje:
    pass

print(Personaje)     # <class '__main__.Personaje'>
print(Personaje())   # <__main__.Personaje object at 0x...>
```

`Personaje` es la clase; `Personaje()` es un objeto nuevo cada vez que se evalúa.

## ¿Por qué `__init__` lleva `self` si no lo paso al llamar?

Porque Python lo pasa automáticamente. `aria = Personaje("Aria")` equivale, en la práctica, a llamar `Personaje.__init__(aria, "Aria")`: el primer argumento es el objeto que se está inicializando. Si olvidas `self` en la definición, los argumentos se desplazan y aparece un `TypeError` por argumentos faltantes o de más.

```python
class Personaje:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

Personaje("Aria")  # self = el objeto; nombre = "Aria"
```

## ¿Un atributo de clase es lo mismo que una variable global?

No. Un atributo de clase pertenece a la clase y se accede con `Clase.atributo`. Una variable global vive en el módulo y cualquier función puede modificarla. El atributo de clase permite agrupar la constante o el contador junto al tipo al que pertenece, y se hereda si más adelante creas subclases.

```python
class Personaje:
    MAX_HP = 100

print(Personaje.MAX_HP)
print(globals().get("MAX_HP"))  # None: no existe como global
```

## ¿Por qué `aria.MAX_HP` funciona si `MAX_HP` no está en `aria.__dict__`?

Porque Python busca primero en la instancia y, si no encuentra el nombre, lo busca en la clase. Es el mismo mecanismo que usarás con la herencia más adelante. Por eso leer un atributo de clase desde un objeto es válido, pero asignarlo desde el objeto crea una copia local.

```python
class Personaje:
    MAX_HP = 100

aria = Personaje()
print(aria.MAX_HP)          # 100: lo encuentra en la clase
aria.MAX_HP = 120           # crea un atributo de instancia
print(aria.MAX_HP)          # 120
print(Personaje.MAX_HP)     # 100: la clase sigue igual
```

## ¿Por qué mi lista de inventario aparece compartida entre todos los personajes?

Porque la definiste en el cuerpo de la clase. Ese código se ejecuta una sola vez, cuando se crea la clase, y todas las instancias apuntan a la misma lista. Crea la lista dentro de `__init__` para que cada objeto tenga la suya.

```python
# Incorrecto
class Personaje:
    inventario = []

# Correcto
class Personaje:
    def __init__(self) -> None:
        self.inventario: list[str] = []
```

## ¿Debo usar `type()` o `isinstance()`?

`isinstance()` casi siempre. Acepta tu clase y también sus subclases, que es lo que querrás cuando trabajes con herencia. `type(x) is Personaje` exige coincidencia exacta y falla con una subclase. Reserva `type()` para imprimir o depurar.

```python
print(isinstance(aria, Personaje))  # True, también para subclases
print(type(aria) is Personaje)      # True solo si es exactamente Personaje
```

## ¿Cómo sé qué atributos tiene un objeto en tiempo de ejecución?

Con `vars(objeto)` o `objeto.__dict__`, que devuelven un diccionario con los atributos de instancia. No incluyen los de clase. Para ver también esos, revisa `vars(type(objeto))` o consulta directamente `Clase.__dict__`.

```python
print(vars(aria))               # atributos propios
print(Personaje.__dict__.keys())  # atributos y métodos de la clase
```

## ¿Los atributos de clase se pueden modificar?

Sí, pero hazlo siempre a través de la clase: `Personaje.total_personajes += 1`. Si lo haces desde una instancia, creas o modificas un atributo de instancia y el compartido queda intacto. Para constantes como `MAX_HP`, lo sano es no modificarlas durante la ejecución.
