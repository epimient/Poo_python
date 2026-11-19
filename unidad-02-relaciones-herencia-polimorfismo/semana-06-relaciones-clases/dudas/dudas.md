# Dudas frecuentes — Semana 06

## ¿Cuál es la diferencia real entre asociación y dependencia?
La asociación se guarda en un atributo y dura mientras vivan los objetos: `jugador.personaje`, `equipo.jugadores`. La dependencia existe solo durante una operación: un método recibe un objeto, lo usa y lo olvida al terminar. Si al salir del método el vínculo desaparece, era dependencia.

## ¿Necesito guardar la relación en los dos sentidos?
Solo si usas ambos recorridos. `equipo.jugadores` te deja listar la plantilla; `jugador.equipo` te deja responder «¿en qué equipo juega?». Cada dirección extra hay que sincronizarla, así que agrégala cuando el diseño la pida, no por costumbre.

## ¿Cómo evito que se desincronicen los dos lados?
Centraliza la mutación en un único método y actualiza ambos lados ahí:

```python
def agregar(self, jugador: Jugador) -> None:
    if jugador.equipo is not None:
        raise ValueError("Ya tiene equipo.")
    self._jugadores.append(jugador)
    jugador.equipo = self
```

Nunca modifiques `_jugadores` desde fuera de la clase.

## ¿Por qué no puedo hacer `equipo.jugadores.append(ana)`?
Porque la propiedad devuelve una tupla, no la lista original. Si devolvieras `self._jugadores`, cualquiera podría saltarse las validaciones de cupo y duplicados. La tupla es una vista de solo lectura; para modificar, usa `agregar()` o `retirar()`.

## ¿La multiplicidad 1:N se implementa siempre con una lista?
En memoria sí: el lado «muchos» guarda una lista de referencias. En una base de datos relacional, en cambio, la clave foránea suele vivir en la tabla del lado «muchos». Lo importante es la cardinalidad del modelo, no la estructura física.

## ¿Cómo implemento una N:M sin duplicar datos?
Con dos listas que se actualizan en el mismo método, una en cada extremo. Si además necesitas datos propios de la relación (fecha de inscripción, puntaje), crea una tercera clase intermedia, por ejemplo `Inscripcion`, con referencias al jugador y a la partida.

## ¿Debo validar con `assert` o con `raise`?
Con `raise ValueError`. Las `assert` están pensadas para depuración y desaparecen si ejecutas `python -O`. Una regla de negocio como «el equipo está lleno» debe fallar siempre, no solo en modo de desarrollo.

## ¿Un jugador puede estar en dos equipos a la vez?
En este modelo no: la cardinalidad del lado equipo es `0..1`. Se implementa comprobando `jugador.equipo is not None` antes de agregarlo. Si el dominio permitiera varios equipos, cambiarías el atributo por una lista y la cardinalidad a `0..*`.
