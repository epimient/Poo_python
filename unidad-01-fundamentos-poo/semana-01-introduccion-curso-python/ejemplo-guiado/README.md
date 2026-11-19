# Ejemplo guiado — Semana 01

## Qué construye

`personaje.py` define la clase `Personaje` con tres atributos (`nombre`, `hp`, `ataque`) y tres métodos:

- `presentarse()` devuelve una frase con el estado inicial.
- `atacar(objetivo)` descuenta vida al personaje recibido y muestra el daño.
- `esta_vivo()` responde si aún le queda vida.

El bloque `demo()` crea tres personajes de videojuego, imprime una tabla de estado, ejecuta una ronda de ataques y vuelve a mostrar el estado del equipo.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 personaje.py
```

No necesita dependencias externas ni datos por teclado. Funciona con Python 3.12 en Linux, Windows y macOS.

## Salida esperada

```text
=== Presentaciones ===
Soy Kaede y tengo 120 HP.
Soy Rook y tengo 90 HP.
Soy Nima y tengo 100 HP.

--- Estado del equipo ---
Kaede    | HP 120 | ATQ 18 | en pie
Rook     | HP  90 | ATQ 24 | en pie
Nima     | HP 100 | ATQ 14 | en pie

=== Ronda de combate ===
Kaede ataca a Rook y causa 18 de daño.
Rook queda con 72 HP.
Rook ataca a Kaede y causa 24 de daño.
Kaede queda con 96 HP.
Nima ataca a Rook y causa 14 de daño.
Rook queda con 58 HP.

--- Estado del equipo ---
Kaede    | HP  96 | ATQ 18 | en pie
Rook     | HP  58 | ATQ 24 | en pie
Nima     | HP 100 | ATQ 14 | en pie

La ronda termina y todos siguen en pie.
```

## Puntos clave

1. **La clase es el molde, los objetos son las copias.** `Personaje` se define una vez; `kaede`, `rook` y `nima` son tres instancias con atributos independientes.
2. **`__init__` construye el estado inicial.** Todo objeto nace con nombre, vida y ataque; no hay atributos a medio crear.
3. **`self` es el objeto actual.** En `kaede.atacar(rook)`, `self` es `kaede` y `objetivo` es `rook`. Por eso el método puede leer el ataque de uno y modificar la vida del otro.
4. **Los métodos pueden cambiar el estado.** `atacar` no devuelve un número: modifica `objetivo.hp`. Esa mutación es visible después, como en un juego real.
5. **El bloque `if __name__ == "__main__":` separa definición y ejecución.** Puedes importar `Personaje` desde otro archivo sin que el demo se ejecute solo.

## Para experimentar

- Cambia el ataque de `Rook` a `40` y observa cuántas rondas resiste `Kaede`.
- Agrega un método `curar(cantidad: int)` que aumente `hp` sin pasar de un máximo.
- Crea un cuarto personaje y agrégalo a la lista `equipo`.
- Intenta imprimir `Personaje.hp` sin crear un objeto y explica el error.
