# Ejemplo guiado — Clases abstractas y protocolos

## Qué construye

Dos scripts independientes:

- **`personaje_abstracto.py`**: convierte `Personaje` en una clase abstracta con `ABC` y `@abstractmethod`. `Guerrero`, `Mago`, `Arquero` y `Ogro` implementan `atacar()`; la base aporta estado, daño recibido y un método plantilla `realizar_turno()`.
- **`habilidades.py`**: define el `Protocol` `Curable` y una función que cura a cualquier objeto que tenga `nombre`, `vida`, `vida_maxima` y `curar()`. `Aldeano` y `Mascota` lo cumplen sin heredar de nada; `Piedra` no.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 personaje_abstracto.py
python3 habilidades.py
```

Ningún script pide datos ni usa dependencias externas.

## Salida esperada — `personaje_abstracto.py`

```text
--- Contrato abstracto ---
Personaje no se puede instanciar:
  Can't instantiate abstract class Personaje without an implementation for abstract method 'atacar'

Una subclase sin atacar() tampoco se instancia:
  Can't instantiate abstract class PersonajeIncompleto without an implementation for abstract method 'atacar'

Métodos abstractos pendientes: frozenset({'atacar'})

--- Combate usando el método plantilla ---
Ragnar causa 18 de daño. Ogro de práctica (72 PV) restante
  Estado: Ragnar (120 PV)
Morgana causa 21 de daño. Ogro de práctica (51 PV) restante
  Estado: Morgana (80 PV, maná 10)
Lyra causa 12 de daño. Ogro de práctica (39 PV) restante
  Estado: Lyra (90 PV, flechas 1)

El ogro contraataca a Ragnar: 9 de daño
  Estado: Ragnar (111 PV)

--- Consultas de tipo ---
isinstance(Ragnar, Personaje): True
issubclass(Guerrero, Personaje): True
¿Queda algún método abstracto en Guerrero? ninguno
```

## Salida esperada — `habilidades.py`

```text
--- Protocolo Curable ---
Ragnar recupera 25 PV (65/120)
Fénix recupera 20 PV (30/30)
Total curado en el primer turno: 45 PV

--- Segunda curación ---
Ragnar recupera 25 PV (90/120)
Fénix recupera 0 PV (30/30)

--- Un objeto que no cumple el contrato ---
¿Roca es Curable? False
Roca no se puede curar: no cumple el contrato

--- Sin herencia de por medio ---
¿Aldeano hereda de Curable? False
¿Mascota hereda de Curable? False
Ambas cumplen el contrato por su forma, no por su árbol genealógico.
```

## Puntos clave

1. **`ABC` bloquea objetos incompletos.** `Personaje("Genérico", ...)` lanza `TypeError`. El fallo aparece al construir, no al usar el objeto en combate.
2. **El contrato se hereda, la implementación no.** `@abstractmethod` obliga a cada subclase a definir `atacar()`. Una hija que no lo hace sigue siendo abstracta y tampoco se instancia.
3. **El método plantilla fija el orden.** `realizar_turno()` calcula el ataque, aplica el daño y devuelve el resultado. Las subclases solo cambian `atacar()`.
4. **`Protocol` no exige herencia.** `Aldeano` y `Mascota` no conocen a `Curable`; aun así, `isinstance(obj, Curable)` devuelve `True` porque tienen los miembros del contrato.
5. **La comprobación es superficial.** `runtime_checkable` verifica que `curar` exista, no que reciba un `int` ni que devuelva otro. La firma correcta sigue siendo responsabilidad del programador.

## Para experimentar

- Quita `atacar()` de `Mago` y comprueba el `TypeError` al crear el objeto.
- Añade `Dragon(Personaje)` con un ataque que dependa de su aliento.
- Crea una clase `Fuente` con `nombre`, `vida`, `vida_maxima` y `curar()`; debería funcionar en `curar_equipo()` sin tocar la función.
- Pasa una `Piedra` a `curar_equipo()` y observa cómo la guarda de `curar_aliado()` la rechaza.
