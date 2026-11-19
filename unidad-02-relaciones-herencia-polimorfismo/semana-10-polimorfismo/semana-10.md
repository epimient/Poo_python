# Semana 10 — Polimorfismo

> Un mismo mensaje, muchas respuestas: el código que llama no necesita saber con quién está hablando.

## Objetivos de aprendizaje

- Explicar qué significa "mismo mensaje, distintas respuestas" con un ejemplo propio.
- Implementar polimorfismo mediante herencia, sobrescritura y clases abstractas.
- Reconocer duck typing y escribir contratos estructurales con `typing.Protocol`.
- Usar métodos dunder para que tus objetos se integren con `len()`, `for`, `+` y `str()`.
- Aplicar `functools.singledispatch` cuando el comportamiento depende del tipo de dato.
- Detectar cadenas de `isinstance()` y reemplazarlas por un diseño polimórfico.

## ¿Por qué importa?

Imagina el bucle de combate de un videojuego. Tienes un guerrero, un mago y un arquero. La primera versión suele escribirse así:

```python
for personaje in personajes:
    if isinstance(personaje, Guerrero):
        personaje.golpe_espada()
    elif isinstance(personaje, Mago):
        personaje.lanzar_hechizo()
    elif isinstance(personaje, Arquero):
        personaje.disparar_flecha()
```

Funciona. Hasta que agregas un paladín. Entonces vuelves al bucle, agregas otro `elif`, pruebas todo de nuevo y rezas para no romper el daño del mago. Cada clase nueva obliga a modificar código que ya estaba terminado. Eso es exactamente lo que el polimorfismo evita.

Con un contrato común, el bucle se escribe una sola vez:

```python
for personaje in personajes:
    personaje.atacar(objetivo)
```

El bucle no pregunta qué tipo es `personaje`. Solo confía en que sabe responder al mensaje `atacar()`. Si mañana agregas el paladín, el bucle no cambia: solo agregas una clase nueva. Este es el corazón del principio abierto/cerrado: abierto a extensión, cerrado a modificación.

## Concepto central

Polimorfismo significa que objetos de tipos distintos responden al mismo mensaje de maneras distintas. Para que funcione necesitas tres cosas:

1. **Un contrato común**: un método con el mismo nombre y una firma compatible.
2. **Implementaciones distintas**: cada clase decide cómo responder.
3. **Un cliente que solo conoce el contrato**: el bucle, la función o la clase `Combate` no conoce las subclases.

| Mecanismo | Cómo se logra | Cuándo usarlo |
|---|---|---|
| Herencia + sobrescritura | Subclases redefinen un método del padre | Jerarquías naturales con estado compartido |
| Clase abstracta | `ABC` + `@abstractmethod` | Quieres obligar un contrato y compartir lógica |
| Duck typing | Objetos con el mismo método, sin padre común | Integrar colaboradores ligeros o de terceros |
| `Protocol` | Contrato estructural verificable por el tipado | Quieres documentar duck typing sin herencia |
| `singledispatch` | Una función con variantes por tipo | El comportamiento depende del dato, no del objeto |

:::info
Polimorfismo no es "tener muchas clases". Es que el código cliente pueda tratar todas esas clases igual. Si el cliente necesita preguntar el tipo, todavía no hay polimorfismo: hay un `if` disfrazado.
:::

## Código paso a paso

### 1. Define el contrato con una clase abstracta

```python
from abc import ABC, abstractmethod


class Personaje(ABC):
    def __init__(self, nombre: str, hp: int) -> None:
        self.nombre = nombre
        self._hp = hp

    @property
    def vivo(self) -> bool:
        return self._hp > 0

    def recibir_dano(self, cantidad: int) -> int:
        real = min(max(cantidad, 0), self._hp)
        self._hp -= real
        return real

    @abstractmethod
    def atacar(self, objetivo: "Personaje") -> str:
        """Aplica daño y devuelve una descripción del ataque."""
```

`Personaje` no se puede instanciar: es un contrato. Define lo que todos comparten (nombre, HP, recibir daño) y obliga a implementar `atacar()`.

### 2. Cada subclase responde a su manera

```python
class Guerrero(Personaje):
    fuerza = 20

    def atacar(self, objetivo: Personaje) -> str:
        dano = 20 + self.fuerza
        real = objetivo.recibir_dano(dano)
        return f"golpe de espada: {real} de daño"


class Mago(Personaje):
    poder = 25
    mana = 60

    def atacar(self, objetivo: Personaje) -> str:
        if self.mana >= 15:
            self.mana -= 15
            real = objetivo.recibir_dano(self.poder)
            return f"bola de fuego: {real} de daño"
        real = objetivo.recibir_dano(6)
        return f"golpe de bastón: {real} de daño"
```

El guerrero no gasta maná; el mago sí. El arquero podría fallar según una probabilidad. Lo importante es que los tres métodos se llaman igual y reciben el mismo tipo de objetivo.

### 3. El cliente recorre la lista sin preguntar tipos

```python
class Combate:
    def __init__(self, personajes: list[Personaje]) -> None:
        self.personajes = personajes

    def jugar_turno(self) -> None:
        for personaje in self.personajes:
            if not personaje.vivo:
                continue
            objetivo = self.elegir_rival(personaje)
            if objetivo is None:
                break
            narracion = personaje.atacar(objetivo)
            print(f"{personaje.nombre}: {narracion}")
```

`Combate` depende de `Personaje`, no de `Guerrero`, `Mago` ni `Arquero`. Esa dependencia es la que hace que agregar clases no te obligue a tocar el bucle.

### 4. Duck typing y `Protocol`

Python no exige herencia para aceptar un mensaje. Si un objeto sabe `volar()`, puedes usarlo donde esperas algo que vuela:

```python
from typing import Protocol


class Volador(Protocol):
    def volar(self) -> str:
        ...


class Pajaro:
    def volar(self) -> str:
        return "El pájaro bate las alas"


class Avion:
    def volar(self) -> str:
        return "El avión enciende los motores"


def despegar(volador: Volador) -> None:
    print(volador.volar())
```

`Pajaro` y `Avion` no heredan de `Volador`, pero ambos cumplen el contrato. `Protocol` documenta ese acuerdo y permite que el editor te avise si falta `volar()`. En tiempo de ejecución, Python simplemente llama al método: eso es duck typing.

### 5. Dunders: polimorfismo con la sintaxis del lenguaje

Un inventario puede responder a `len()`, `for`, `in`, `+` y `print()` si implementas los métodos especiales correctos:

```python
class Inventario:
    def __init__(self, objetos: list[str]) -> None:
        self._objetos = list(objetos)

    def __len__(self) -> int:
        return len(self._objetos)

    def __iter__(self):
        return iter(self._objetos)

    def __contains__(self, nombre: object) -> bool:
        return nombre in self._objetos

    def __add__(self, otro: "Inventario") -> "Inventario":
        if not isinstance(otro, Inventario):
            return NotImplemented
        return Inventario(self._objetos + otro._objetos)

    def __str__(self) -> str:
        return "Inventario: " + ", ".join(self._objetos)
```

Ahora `len(mochila)`, `for objeto in mochila`, `"poción" in mochila` y `mochila + cofre` funcionan sin que escribas bucles especiales. Ojo: `__add__` devuelve `NotImplemented` (no lanza excepción) cuando el otro operando no es compatible; Python intentará la operación reflejada.

### 6. `singledispatch`: variantes por tipo de dato

A veces el comportamiento depende del tipo del argumento, no del objeto que recibe el mensaje. El daño es el ejemplo clásico:

```python
from functools import singledispatch


@singledispatch
def aplicar_dano(dano: object, armadura: int = 0) -> int:
    raise TypeError(f"Daño no soportado: {type(dano).__name__}")


@aplicar_dano.register
def _(dano: DanoFisico, armadura: int = 0) -> int:
    return max(1, dano.puntos - armadura)


@aplicar_dano.register
def _(dano: DanoMagico, armadura: int = 0) -> int:
    return max(1, dano.puntos - armadura // 2)
```

Cada tipo de daño tiene su fórmula y no necesitas una cadena de `if isinstance`. `singledispatch` es útil cuando los tipos vienen de fuera o cuando las reglas crecen por variantes del dato, no por subclases del atacante.

## Diagrama / modelo

```text
                Personaje (ABC)
                + atacar()
                + recibir_dano()
                + vivo
               /       |        \
        Guerrero      Mago      Arquero
        atacar()     atacar()    atacar()

Combate ──────> Personaje
   │                 ▲
   └── llama atacar()┘  (no conoce las subclases)
```

La flecha importante es `Combate → Personaje`. Si `Combate` apuntara a cada subclase, tendrías que modificarlo por cada personaje nuevo. Al depender solo del contrato, el cliente queda estable y las variantes crecen por fuera.

## Errores comunes

:::error
**Cadena de `isinstance`.** Si el bucle pregunta el tipo para decidir qué método llamar, no estás usando polimorfismo. Mueve la decisión a cada clase: todas exponen `atacar()` y cada una resuelve su lógica.
:::

- **Olvidar `super().__init__()`.** La subclase no inicializa nombre ni HP y el objeto queda incompleto. Llama primero al constructor del padre.
- **Cambiar la firma al sobrescribir.** Si el padre recibe `(objetivo)` y la subclase recibe `(objetivo, veces)`, el cliente polimórfico fallará. Mantén nombres y parámetros compatibles.
- **Confundir `NotImplemented` con `NotImplementedError`.** El primero es un valor especial para operadores; el segundo es una excepción para métodos no implementados.
- **Duck typing sin contrato documentado.** Aunque Python no exija herencia, el equipo sí necesita saber qué métodos espera una función. Un `Protocol` o un docstring claro evita sorpresas.
- **Usar `hasattr()` como validación universal.** Comprueba que el método existe, no que su firma o su comportamiento sean correctos.

:::warning
`isinstance()` no es el enemigo absoluto. Es válido para validar entradas en un borde del sistema o para implementar `__add__`. El problema es usarlo dentro del bucle de negocio para elegir comportamiento entre subclases.
:::

## Buenas prácticas

- **Programa contra contratos, no contra clases concretas.** Anota `list[Personaje]`, no `list[Guerrero | Mago | Arquero]`.
- **Haz contratos pequeños.** Un método abstracto claro es mejor que cinco métodos que nadie usa.
- **Devuelve datos, no imprimas dentro de la lógica.** `atacar()` puede devolver una descripción; `Combate` decide cómo mostrarla. Así puedes probar el daño sin capturar la salida.
- **Prueba el cliente con un doble de prueba.** Un `PersonajeFalso` con `atacar()` que devuelve `"test"` demuestra que `Combate` no depende de las clases reales.
- **Reserva `singledispatch` para variantes del dato.** Si la variación es del personaje, usa métodos; si es del tipo de daño, usa despacho por tipo.

:::success
Si puedes agregar una clase nueva sin editar `Combate`, tu diseño es polimórfico. Esa es la prueba más rápida y la que más te va a servir en el proyecto de la unidad.
:::

## Checklist de la semana

- [ ] Explico con mis palabras la diferencia entre sobrescribir y sobrecargar.
- [ ] Mi clase base declara `atacar()` como abstracta.
- [ ] El bucle de combate no contiene `isinstance` ni `type(...) is`.
- [ ] Implementé `__str__`, `__len__`, `__iter__` y `__add__` en un inventario.
- [ ] Sé cuándo usar `Protocol` y cuándo usar una clase abstracta.
- [ ] Probé un caso con una subclase nueva sin tocar el cliente.
- [ ] Mi reto del arcade valida la entrada y permite revancha.

## Resumen

El polimorfismo es una forma de repartir responsabilidades: el cliente envía un mensaje y cada objeto decide cómo responder. La herencia y las clases abstractas te dan un contrato explícito; el duck typing y `Protocol` te permiten contratos más ligeros; los dunders integran tus objetos con la sintaxis de Python; y `singledispatch` resuelve variantes basadas en el tipo del dato. La señal de un mal diseño es la cadena de `isinstance` en el bucle principal. La señal de un buen diseño es que puedes agregar una clase y el cliente ni se entera.

## Siguiente paso

En el ejemplo guiado construirás `combate_turnos.py` con tres especialidades y un `Combate` que las trata a todas igual. Después resolverás el reto obligatorio **Arcade: duelo por turnos**, donde tú eliges un personaje, la máquina elige otro y el bucle polimórfico decide el ganador. Antes de la evaluación de la unidad, revisa que tu proyecto pueda agregar una especialidad nueva sin tocar el motor de combate.

:::reto
Toma el combate guiado y agrega una clase `Paladin` con un ataque que cure a un aliado antes de golpear. El bucle de `Combate` no debe cambiar. Si tienes que modificarlo, revisa qué parte del contrato quedó incompleta.
:::
