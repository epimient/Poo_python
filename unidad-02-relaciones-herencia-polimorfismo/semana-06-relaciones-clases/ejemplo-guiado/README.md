# Ejemplo guiado — Semana 06

## Qué construye

`equipo.py` modela tres relaciones a la vez:

```text
Personaje  <-- 1:1 -->  Jugador  <-- 1:N -->  Equipo
```

- `Personaje`: ficha de juego independiente (nombre, clase, nivel, HP).
- `Jugador`: alias, un personaje (asociación 1:1) y un equipo opcional (navegabilidad inversa).
- `Equipo`: nombre, cupo máximo y lista privada de jugadores (asociación 1:N).

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 equipo.py
```

Menú interactivo (opcional, requiere teclado):

```bash
python3 equipo.py --interactivo
```

## Salida esperada

La demo imprime cinco bloques:

1. **Asociación 1:N**: tres jugadores fichados y el promedio de nivel.
2. **Reglas**: rechazo del cuarto jugador por cupo y de un jugador que ya tiene equipo.
3. **Asociación 1:1**: Caro cambia de personaje; el anterior no se destruye.
4. **Retirar**: Beto sale, se libera su cupo y Duna entra.
5. **Recorrido inverso**: `ana.equipo` y `equipo.jugadores` muestran la misma verdad.

## Puntos clave

1. **Se guardan objetos, no textos.** `jugador.personaje` es una referencia: cambiar el nivel del personaje se refleja sin sincronizar copias.
2. **La lista es privada.** `_jugadores` solo se modifica mediante `agregar()` y `retirar()`; la propiedad `jugadores` devuelve una tupla.
3. **Los dos lados se actualizan juntos.** `Equipo.agregar()` asigna `jugador.equipo = self`; `retirar()` lo devuelve a `None`.
4. **Las reglas viven en la clase.** Cupo máximo, duplicados y equipo único se validan con `ValueError`, no con `assert`.
5. **La navegabilidad se justifica.** La referencia inversa existe porque la demo pregunta «¿en qué equipo juega Ana?».

## Prueba rápida

Después de la demo, en una consola de Python:

```python
from equipo import Equipo, Jugador, Personaje

ana = Jugador("Ana", Personaje("Kael", "Mago", 7))
equipo = Equipo("Los Cometas")
equipo.agregar(ana)
print(ana.equipo.nombre)       # Los Cometas
print(len(equipo.jugadores))   # 1
```

Si intentas `equipo.agregar(ana)` de nuevo, debes recibir un `ValueError`.
