# Ejercicios — Semana 01

## Nivel 1 — Básico: Ficha de personaje

**Enunciado.** Crea un programa `ficha.py` que guarde los datos de un personaje de videojuego en variables y muestre una ficha con formato. No necesitas clases todavía: el objetivo es practicar variables, tipos y `f-string`.

**Requisitos.**
- Declara al menos: `nombre` (texto), `clase` (texto), `nivel` (entero), `hp` (entero), `ataque` (entero) y `esta_vivo` (booleano).
- Calcula el daño de un golpe crítico como `ataque * 2` en una variable nueva.
- Imprime una ficha con bordes y columnas alineadas.
- Usa un comentario breve para explicar qué representa cada grupo de datos.

**Entrada esperada.** Datos escritos directamente en el código, por ejemplo:

```python
nombre = "Kaede"
clase = "Guerrera"
nivel = 7
hp = 120
ataque = 18
esta_vivo = True
```

**Salida esperada.** (Los valores pueden variar, el formato no.)

```text
==============================
 FICHA DE PERSONAJE
==============================
 Nombre : Kaede
 Clase  : Guerrera
 Nivel  : 7
 HP     : 120
 Ataque : 18
 Estado : en pie
 Crítico: 36
==============================
```

**Criterios de evaluación.**
- [ ] El programa ejecuta con `python3 ficha.py` sin errores.
- [ ] Usa los seis tipos de dato solicitados.
- [ ] El daño crítico se calcula con una operación, no está escrito a mano.
- [ ] La salida está alineada y se lee con claridad.
- [ ] El archivo tiene un docstring o comentario inicial que explica su propósito.

---

## Nivel 2 — Intermedio: Tres personajes

**Enunciado.** Crea `tres_personajes.py` con una clase `Personaje` y tres objetos distintos. Cada personaje debe presentarse y atacar a otro. Al final, el programa muestra una tabla con el estado del equipo.

**Requisitos.**
- La clase debe llamarse `Personaje` y recibir `nombre`, `hp` y `ataque` en `__init__`.
- Incluye los métodos `presentarse()`, `atacar(objetivo)` y `esta_vivo()`.
- Valida en el constructor: `hp` debe ser mayor que cero y `ataque` no puede ser negativo. Si un valor no cumple, lanza `ValueError` con un mensaje claro.
- `atacar` no debe dejar la vida por debajo de cero.
- Crea tres personajes con nombres, vidas y ataques diferentes.
- Muestra el estado antes y después de una ronda de ataques.
- Usa `if __name__ == "__main__":` para ejecutar el demo.

**Entrada esperada.**

```python
kaede = Personaje("Kaede", 120, 18)
rook = Personaje("Rook", 90, 24)
nima = Personaje("Nima", 100, 14)
```

**Salida esperada.**

```text
Soy Kaede y tengo 120 HP.
Soy Rook y tengo 90 HP.
Soy Nima y tengo 100 HP.

--- Estado inicial ---
Kaede    | HP 120 | en pie
Rook     | HP  90 | en pie
Nima     | HP 100 | en pie

Kaede ataca a Rook y causa 18 de daño.
Rook queda con 72 HP.
...

--- Estado final ---
Kaede    | HP  96 | en pie
Rook     | HP  58 | en pie
Nima     | HP 100 | en pie
```

**Criterios de evaluación.**
- [ ] Los tres objetos son independientes: modificar uno no cambia a los otros.
- [ ] El constructor rechaza `hp=0` y `ataque=-1` con `ValueError`.
- [ ] `atacar` usa `self` y el objeto recibido, no variables globales.
- [ ] La vida nunca aparece negativa.
- [ ] El demo se ejecuta sin pedir datos por teclado.

---

## Nivel 3 — Reto: Menú simple de selección

**Enunciado.** Crea `menu_equipo.py`: un programa de consola que administra un equipo de personajes. El usuario elige opciones con un número y el programa responde hasta que escriba `0`. Este es el primer paso hacia una aplicación interactiva; en semanas posteriores el menú se conectará a más reglas del juego.

**Requisitos.**
- Define una clase `Personaje` con `nombre`, `hp` y `ataque`, más un método `estado()` que devuelva una línea de texto.
- Valida en el constructor que `hp` sea mayor que cero y que `ataque` sea mayor o igual que cero.
- Mantén una lista con al menos tres personajes creados al inicio.
- Implementa este menú:

```text
=== EQUIPO ===
1. Ver personajes
2. Seleccionar personaje
3. Atacar al primer enemigo
0. Salir
```

- La opción `2` pide un nombre o un número de la lista y guarda la selección. Si no existe, muestra un error y no cambia la selección.
- La opción `3` usa el personaje seleccionado para atacar a un enemigo fijo. Si no hay selección, avisa que primero debe elegir uno.
- Una opción fuera de rango no debe cerrar el programa: muestra un mensaje y vuelve al menú.
- El programa termina solo con `0`.

**Entrada esperada.** Una secuencia de prueba como esta:

```text
1
2
Rook
3
9
0
```

**Salida esperada.** (Resumida; tu texto puede variar si mantiene la información.)

```text
=== EQUIPO ===
1. Ver personajes
2. Seleccionar personaje
3. Atacar al primer enemigo
0. Salir
Opción: 1
- Kaede | HP 120 | ATQ 18
- Rook | HP 90 | ATQ 24
- Nima | HP 100 | ATQ 14
Opción: 2
Nombre del personaje: Rook
Seleccionado: Rook
Opción: 3
Rook ataca al enemigo y causa 24 de daño.
Opción: 9
Opción inválida. Elige un número del menú.
Opción: 0
Hasta la próxima partida.
```

**Criterios de evaluación.**
- [ ] El menú se repite hasta que el usuario escribe `0`.
- [ ] La selección se conserva entre iteraciones.
- [ ] Una opción inválida o un nombre inexistente no rompe el programa.
- [ ] Atacar sin selección muestra un aviso comprensible.
- [ ] Las validaciones del constructor están probadas con al menos un caso incorrecto.
- [ ] El código está separado en funciones pequeñas (`mostrar_menu`, `listar`, `seleccionar`, `atacar`) y una clase con responsabilidad clara.

:::reto
Cuando termines, agrega una opción `4. Curar personaje` que pregunte cuánto curar y no permita superar el HP máximo inicial. Guarda ese máximo como atributo `hp_max` en el constructor.
:::
