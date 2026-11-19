# Ejemplo guiado — Semana 02

## Qué construye

`paradigmas.py` resuelve el mismo combate de tres personajes con dos enfoques:

1. **Procedural:** diccionarios para el estado y funciones (`crear_personaje`, `atacar_procedural`) para las acciones.
2. **Orientado a objetos:** una clase `Personaje` con atributos y métodos (`estado`, `atacar`).

Ambas versiones usan los mismos datos y la misma secuencia de ataques, así que el estado final coincide. El objetivo es comparar la organización del código, no el resultado numérico.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 paradigmas.py
```

No requiere dependencias externas ni entrada por teclado.

## Salida esperada

```text
=== VERSIÓN PROCEDURAL ===
Kaede    | HP 120 | ATQ 18
Rook     | HP  90 | ATQ 24
Nima     | HP 100 | ATQ 14

Kaede ataca a Rook y causa 18 de daño.
Rook queda con 72 HP.
Rook ataca a Kaede y causa 24 de daño.
Kaede queda con 96 HP.
Nima ataca a Rook y causa 14 de daño.
Rook queda con 58 HP.

Estado final:
Kaede    | HP  96 | ATQ 18
Rook     | HP  58 | ATQ 24
Nima     | HP 100 | ATQ 14

=== VERSIÓN ORIENTADA A OBJETOS ===
Kaede    | HP 120 | ATQ 18
Rook     | HP  90 | ATQ 24
Nima     | HP 100 | ATQ 14

Kaede ataca a Rook y causa 18 de daño.
Rook queda con 72 HP.
Rook ataca a Kaede y causa 24 de daño.
Kaede queda con 96 HP.
Nima ataca a Rook y causa 14 de daño.
Rook queda con 58 HP.

Estado final:
Kaede    | HP  96 | ATQ 18
Rook     | HP  58 | ATQ 24
Nima     | HP 100 | ATQ 14

=== COMPARACIÓN ===
Ambas versiones terminan con el mismo estado:
Kaede: 96 HP | Rook: 58 HP | Nima: 100 HP
La diferencia está en dónde viven los datos y las reglas.
```

## Puntos clave

1. **Mismo dominio, distinta estructura.** El diccionario guarda el estado, pero cualquier función puede modificarlo. La clase declara qué operaciones tienen sentido y concentra las reglas del personaje.
2. **`self` elimina el primer parámetro repetido.** En procedural, cada función recibe el diccionario; en POO, el objeto ya sabe quién es y solo recibe al objetivo.
3. **La lectura cambia.** `atacar_procedural(kaede, rook)` describe una función externa; `kaede.atacar(rook)` describe una acción del personaje. La segunda se parece más al juego.
4. **La salida no prueba superioridad.** Que ambas impriman lo mismo demuestra que el paradigma es una decisión de diseño. La ventaja de la POO aparecerá al agregar tipos de personaje, validaciones y relaciones.
5. **Los diccionarios siguen siendo útiles.** Para datos temporales, configuraciones o respuestas de una API no necesitas una clase. El criterio es si hay comportamiento y reglas que deban vivir juntos.

## Diagrama del ejemplo

```text
┌──────────────────────────┐
│        Personaje         │
├──────────────────────────┤
│ - nombre: str            │
│ - hp: int                │
│ - ataque: int            │
├──────────────────────────┤
│ + estado(): str          │
│ + atacar(objetivo): None │
└──────────────────────────┘
```

La versión procedural no tiene este diagrama: sus «entidades» son diccionarios sin métodos propios. Ese es, precisamente, el contraste.

## Para experimentar

- Agrega una validación en el constructor de `Personaje` para rechazar `hp <= 0` y compara cuántos lugares tendrías que tocar en la versión procedural.
- Crea un cuarto personaje en ambas versiones con los mismos valores y verifica que el estado final siga coincidiendo.
- Agrega un método `curar(cantidad: int)` solo a la clase y explica por qué en la versión procedural necesitarías otra función.
- Cambia el orden de los ataques y comprueba que el resultado deje de coincidir con la línea de comparación del final (tendrás que ajustarla).
