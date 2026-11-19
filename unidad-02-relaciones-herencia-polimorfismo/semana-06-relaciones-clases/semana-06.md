# Semana 06 — Relaciones entre clases

> Una clase sola es una ficha; dos clases relacionadas son una historia.

## Objetivos de aprendizaje

- Explicar por qué un sistema orientado a objetos necesita clases que se relacionen.
- Distinguir **asociación** de **dependencia** con ejemplos concretos.
- Leer y escribir multiplicidades **1:1**, **1:N** y **N:M**.
- Implementar relaciones con referencias a objetos y listas, no con textos sueltos.
- Decidir la **navegabilidad** de una relación y mantener coherentes ambos lados.
- Dibujar un diagrama UML con cardinalidades y traducirlo a Python.

## ¿Por qué importa?

Hasta ahora tus clases viven aisladas: un `Personaje` con nombre y nivel, una `Cuenta` con saldo. Eso alcanza para un ejercicio, no para un juego ni para un sistema real. En cuanto modelas un RPG necesitas saber **quién** controla a **qué** personaje y **en qué** equipo juega. En banca pasa lo mismo: un cliente tiene cuentas, una cuenta registra transacciones, una transferencia toca dos cuentas.

Sin relaciones, terminas guardando textos como `"equipo": "Los Cometas"` dentro de cada jugador. Ese texto no te deja preguntar cuántos integrantes hay, no valida nada y se desincroniza en cuanto alguien cambia de equipo. Las relaciones con referencias resuelven eso: un objeto **apunta** a otro objeto real y puedes navegar de uno al otro con un punto.

:::info
Una relación no es un adorno del diagrama: es una decisión de diseño que define qué operaciones son posibles y quién es responsable de mantener la información coherente.
:::

## Concepto central

Una **asociación** es un vínculo estructural y duradero entre objetos. El jugador *tiene* un personaje; el equipo *agrupa* jugadores. El vínculo existe mientras ambos objetos existan y suele necesitar reglas: un jugador no puede estar en dos equipos a la vez, un equipo tiene un cupo máximo.

Una **dependencia** es un vínculo temporal y débil: un objeto usa a otro durante una operación y lo olvida al terminar. Si `Partida.calcular_dano(atacante, defensor)` recibe dos personajes, la partida **depende** de ellos para ese cálculo, pero no los guarda como atributos. La prueba es simple: si el vínculo desaparece cuando el método termina, es dependencia; si sigue vivo en un atributo, es asociación.

La **multiplicidad** indica cuántos objetos participan en cada extremo:

| Multiplicidad | Significado | Ejemplo del curso | Implementación típica |
|---|---|---|---|
| 1:1 | Un objeto se relaciona con exactamente uno | Jugador ↔ Personaje | atributo `personaje` |
| 1:N | Un objeto se relaciona con muchos | Equipo → Jugadores | `list[Jugador]` en el equipo |
| N:M | Muchos con muchos | Jugadores ↔ Partidas | lista de partidas en el jugador y lista de jugadores en la partida |
| 0..1 | Puede no tener ninguno | Jugador → Equipo | `Equipo \| None` |

La **navegabilidad** responde a «¿desde dónde puedo llegar?». Si `jugador.personaje` existe, la relación es navegable del jugador al personaje. Si además `equipo.jugadores` existe, el equipo navega hacia sus jugadores. Puedes tener una sola flecha (unidireccional) o dos (bidireccional). La regla práctica: hazla navegable solo en los sentidos que realmente usas; cada dirección extra es información que debes mantener sincronizada.

## Código paso a paso

### 1. Asociación 1:1 con referencia

```python
class Personaje:
    def __init__(self, nombre: str, clase: str, nivel: int = 1) -> None:
        self.nombre = nombre
        self.clase = clase
        self.nivel = nivel


class Jugador:
    def __init__(self, alias: str, personaje: Personaje) -> None:
        self.alias = alias
        self.personaje = personaje  # asociación 1:1
```

El jugador no copia el nombre del personaje: guarda el objeto. Si el personaje sube de nivel, `jugador.personaje.nivel` refleja el cambio sin sincronizar nada. Esa es la primera ventaja de modelar con referencias.

### 2. Asociación 1:N con lista

```python
class Equipo:
    def __init__(self, nombre: str, maximo: int = 3) -> None:
        self.nombre = nombre
        self.maximo = maximo
        self._jugadores: list[Jugador] = []

    def agregar(self, jugador: Jugador) -> None:
        if len(self._jugadores) >= self.maximo:
            raise ValueError("El equipo está lleno.")
        if any(j.alias == jugador.alias for j in self._jugadores):
            raise ValueError("Ese jugador ya está en el equipo.")
        self._jugadores.append(jugador)
```

La lista es privada (`_jugadores`). Si la expones tal cual, cualquiera puede hacer `equipo.jugadores.append(...)` y saltarse las validaciones. Ofrece una vista de solo lectura:

```python
@property
def jugadores(self) -> tuple[Jugador, ...]:
    return tuple(self._jugadores)
```

### 3. Navegabilidad inversa y coherencia

Si quieres preguntar «¿en qué equipo juega Ana?», agrega la referencia inversa y actualízala **en el mismo método** que modifica la lista:

```python
class Jugador:
    def __init__(self, alias: str, personaje: Personaje) -> None:
        self.alias = alias
        self.personaje = personaje
        self.equipo: Equipo | None = None

# dentro de Equipo.agregar, al final:
self._jugadores.append(jugador)
jugador.equipo = self
```

Y al retirar, limpia los dos lados:

```python
def retirar(self, alias: str) -> Jugador:
    for jugador in self._jugadores:
        if jugador.alias.lower() == alias.lower():
            self._jugadores.remove(jugador)
            jugador.equipo = None
            return jugador
    raise ValueError(f"No existe {alias!r} en el equipo.")
```

:::warning
Una relación bidireccional se actualiza en un solo lugar: el método que la cambia. Si escribes `equipo._jugadores.append(j)` por fuera, el jugador quedará con `equipo = None` y tendrás datos contradictorios.
:::

### 4. N:M con dos listas

Jugadores y partidas son muchos con muchos. Cada partida guarda sus participantes y cada jugador guarda su historial:

```python
class Partida:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.jugadores: list[Jugador] = []

    def inscribir(self, jugador: Jugador) -> None:
        if jugador in self.jugadores:
            raise ValueError("El jugador ya está inscrito.")
        self.jugadores.append(jugador)
        jugador.partidas.append(self)


class Jugador:
    # ...
    def __init__(self, alias: str, personaje: Personaje) -> None:
        self.alias = alias
        self.personaje = personaje
        self.equipo: Equipo | None = None
        self.partidas: list[Partida] = []
```

La tabla intermedia en memoria son las dos listas. En una base de datos, esa N:M se convierte en una tabla puente; aquí basta con que ambas listas se actualicen juntas.

## Diagrama / modelo

```text
       1           1                1            0..*            1
  Jugador ─────────────── Personaje          Equipo ─────────── Jugador
     │   tiene un personaje                   agrupa 1..3      │
     │                                                         │
     │ 0..*                                          pertenece │
     └──────────────── Partida ────────────────────────────────┘
              *                          *
```

Lectura: un jugador tiene **exactamente un** personaje; un equipo agrupa **de uno a muchos** jugadores; un jugador pertenece **como máximo a un** equipo; jugadores y partidas se relacionan en **N:M**.

En UML, la cardinalidad se escribe junto al extremo contrario. En el diagrama de arriba, el `1` junto a `Personaje` significa «cada jugador apunta a un personaje». No confundas el número con la cantidad de jugadores: siempre describe el extremo al que está pegado.

## Errores comunes

- **Guardar el nombre en lugar del objeto.** `self.equipo = "Los Cometas"` impide validar cupos o consultar integrantes. Usa una referencia.
- **Exponer la lista interna.** `equipo.jugadores.append(j)` evade todas las reglas. Devuelve una tupla o una copia.
- **Actualizar solo un lado.** Agregas a la lista pero no asignas `jugador.equipo`. Al día siguiente la relación miente.
- **Permitir duplicados.** Un jugador puede entrar dos veces al mismo equipo si no comparas antes. Compara por identidad (`in`) y por alias cuando corresponda.
- **Confundir dependencia con asociación.** Si el objeto solo se usa dentro de un método y no se guarda, no lo declares como atributo.
- **Poner la cardinalidad en el extremo equivocado del diagrama.** Practica leyendo el diagrama en voz alta: «un equipo tiene muchos jugadores».
- **Validar con `assert`.** Las `assert` se desactivan con `python -O`. Usa `raise ValueError`.

## Buenas prácticas

- Modela primero el diagrama y recién después escribe clases: es más barato borrar una flecha que refactorizar código.
- Nombra los atributos de relación en plural cuando guardan varios objetos: `jugadores`, `partidas`, `transacciones`.
- Centraliza la mutación en métodos como `agregar`, `retirar`, `inscribir`; nunca dejes que el exterior toque la lista.
- Decide la navegabilidad por necesidad real. Si nadie pregunta «en qué equipo juega», no agregues la referencia inversa.
- Escribe una validación por regla y mensajes que digan qué falló: `"Los Cometas está lleno (3 cupos)"` es mejor que `"Error"`.
- Prueba los casos límite: agregar al equipo lleno, agregar un duplicado, retirar a alguien que no existe, cambiar de personaje.

:::reto
Toma el modelo del ejemplo y agrega una clase `Partida` con inscripción N:M. Regla: un jugador no puede inscribirse dos veces en la misma partida y una partida no admite más de cuatro jugadores. Dibuja el UML antes de programar.
:::

## Checklist de la semana

- [ ] Distingo asociación de dependencia con un ejemplo propio.
- [ ] Sé leer una multiplicidad 1:1, 1:N y N:M en un diagrama UML.
- [ ] Implementé una relación 1:1 con una referencia a objeto.
- [ ] Implementé una relación 1:N con una lista privada y métodos de gestión.
- [ ] Mantuve coherentes los dos lados de una relación bidireccional.
- [ ] Evité exponer la lista interna y validé duplicados y cupos.
- [ ] Ejecuté `equipo.py` y expliqué cada bloque de su salida.

## Resumen

Relacionar clases es pasar de fichas sueltas a un sistema. La **asociación** es un vínculo estable que se guarda en atributos; la **dependencia** es un uso pasajero dentro de un método. La **multiplicidad** dice cuántos participan y la **navegabilidad** dice desde dónde puedes llegar. En Python, una relación 1:1 es un atributo con referencia, una 1:N es una lista privada con métodos de gestión y una N:M son dos listas que se actualizan juntas. Si mantienes la coherencia en un único método y validas las reglas, el modelo se sostiene solo.

## Siguiente paso

La semana 07 profundiza en las relaciones todo-parte: agregación y composición. Verás que no todas las relaciones «tiene un» son iguales, porque algunas implican dueño y ciclo de vida. Llevarás el inventario y el equipo al límite para descubrir qué objeto debe morir con quién.
