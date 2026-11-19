# Ejemplo guiado — Semana 07

## Qué construye

`inventario.py` compara las dos relaciones todo-parte en un mismo archivo:

- **Composición:** `Inventario` crea, administra y destruye objetos `Item`.
- **Agregación:** `Equipo` recibe objetos `Personaje` ya creados y no los destruye.
- **Ciclo de vida observable:** cada clase lleva un contador `vivos` actualizado con `weakref.finalize`.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 inventario.py
```

No requiere `input()` ni dependencias externas.

## Salida esperada

Tres bloques y un resumen:

1. **Composición:** un inventario con tres ítems. Al consumir la poción, `Item.vivos` baja de 3 a 2. Al borrar el inventario, baja a 0.
2. **Error de ownership:** una referencia externa a un ítem hace que sobreviva al inventario; al soltarla, el contador vuelve a 0.
3. **Agregación:** un equipo con dos personajes. Al borrar el equipo, `Personaje.vivos` sigue en 3 y los personajes responden con `estado()`.

## Puntos clave

1. **El dueño crea.** `Inventario.crear_item()` construye el `Item` internamente; no acepta ítems externos.
2. **El dueño destruye.** `consumir()` saca el ítem de la lista y lo deja sin referencias; `del inventario` libera el resto.
3. **La agregación no posee.** `Equipo.reclutar()` guarda una referencia; borrar el equipo no afecta a los personajes.
4. **Las referencias filtradas rompen el contrato.** `obtener()` se documenta como consulta y la demo muestra qué pasa si se guarda.
5. **`weakref.finalize` observa, no implementa.** Sirve para demostrar el ciclo de vida; la composición real está en el diseño de la clase.

## Prueba rápida

```python
from inventario import Inventario, Item

inv = Inventario("Kael", capacidad=2)
inv.crear_item("Espada", "arma", 100)
print(len(inv), Item.vivos)   # 1 1
del inv
import gc; gc.collect()
print(Item.vivos)             # 0
```

Si guardas `item = inv.obtener("Espada")` antes del `del`, el contador quedará en 1: acabas de filtrar una referencia interna.
