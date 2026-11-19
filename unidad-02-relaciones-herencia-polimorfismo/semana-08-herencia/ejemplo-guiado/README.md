# Ejemplo guiado — Jerarquía de personajes

## Qué construye

`jerarquia.py` define una clase base `Personaje` y tres subclases (`Guerrero`, `Mago` y `Arquero`) que:

- inicializan la base con `super().__init__()`;
- sobrescriben `atacar()` con una regla propia;
- se guardan en una misma lista y se usan sin preguntar por su clase;
- demuestran `isinstance()`, `issubclass()` y `__mro__`.

El combate contra un ogro de práctica es solo el escenario para ver el polimorfismo en acción.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 jerarquia.py
```

No pide datos ni requiere dependencias externas.

## Salida esperada

```text
Equipo:
  Ragnar (120 PV)
  Morgana (80 PV)
  Lyra (90 PV)

Ronda 1
  Ragnar golpea con la espada: 18 de daño
  Morgana lanza una bola de fuego: 21 de daño (maná 10)
  Lyra dispara una flecha: 12 de daño (quedan 1)
  Ogro de práctica (9 PV) restante
  El ogro golpea a Ragnar (113 PV)

Ronda 2
  Ragnar golpea con la espada: 18 de daño
  Morgana lanza una bola de fuego: 21 de daño (maná 0)
  Lyra dispara una flecha: 12 de daño (quedan 0)
  Ogro de práctica (0 PV) restante

¡El equipo ganó!
--- Jerarquía ---
MRO de Guerrero: Guerrero -> Personaje -> object
MRO de Mago: Mago -> Personaje -> object
MRO de Arquero: Arquero -> Personaje -> object
issubclass(Guerrero, Personaje) = True

--- Consultas de tipo ---
Ragnar   | Guerrero: True  | Personaje: True
Morgana  | Guerrero: False | Personaje: True
Lyra     | Guerrero: False | Personaje: True
```

## Puntos clave

1. **La base concentra lo común.** `Personaje` guarda `nombre`, `vida` y `ataque_base`, y aporta `recibir_dano()` y `esta_vivo()`. Las subclases no repiten ese código.
2. **`super().__init__()` inicializa la parte heredada.** `Guerrero` solo se ocupa de `fuerza`; el resto lo hace la base. Si se omite esa llamada, `self.nombre` no existe.
3. **Sobrescribir es especializar.** `Mago.atacar()` llama a `super().atacar()` y le suma 15, pero descuenta maná. `Arquero` cambia el comportamiento según las flechas que le queden.
4. **La lista heterogénea es el premio.** `simular_combate()` recorre `list[Personaje]` y llama `personaje.atacar()` sin ningún `if` por tipo. Cada objeto responde con su versión.
5. **La jerarquía se puede inspeccionar.** `isinstance()` responde por el objeto, `issubclass()` por la clase y `__mro__` muestra el orden real de búsqueda: `Guerrero -> Personaje -> object`.

## Para experimentar

- Agrega una subclase `Paladin` con poca vida, mucha defensa y un ataque que cure al aliado más herido.
- Cambia el orden de la lista y observa quién recibe el golpe del ogro.
- Intenta crear un `Personaje` genérico y atacar con él: funciona, porque todavía no es abstracto. En la semana 09 esa puerta se cierra.
