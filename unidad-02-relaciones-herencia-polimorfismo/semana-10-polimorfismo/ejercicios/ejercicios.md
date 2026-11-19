# Ejercicios — Semana 10

## Nivel 1 — Básico: El zoológico y el bestiario

**Enunciado.** Practica el mismo mensaje con respuestas distintas en dos jerarquías independientes. Primero modela animales que hablan; después, enemigos que atacan. En ambos casos el programa cliente debe recorrer una lista y llamar al método común sin preguntar el tipo.

**Requisitos.**
- Crea `Animal(ABC)` con `nombre` y el método abstracto `hablar() -> str`. Implementa `Perro`, `Gato` y `Vaca` con sonidos distintos.
- Crea `Enemigo(ABC)` con `nombre`, `hp`, `vivo`, `recibir_dano(cantidad)` y el método abstracto `atacar() -> str`. Implementa `Slime`, `Goblin` y `Dragon` con daños y mensajes propios.
- En `main`, recorre una lista de animales llamando `hablar()` y una lista de enemigos llamando `atacar()`. No uses `isinstance` ni `type(...) is` para decidir qué método ejecutar.

**Entrada esperada.**
Ninguna. Usa datos creados en el código.

**Salida esperada.**
```text
== Zoológico ==
Rex dice: ¡Guau!
Michi dice: ¡Miau!
Lola dice: ¡Muuu!

== Bestiario ==
Slime ataca: 5 de daño
Goblin ataca: 12 de daño
Dragon ataca: 30 de daño
```

**Criterios de evaluación.**
- [ ] `Animal` y `Enemigo` son abstractas y no se pueden instanciar.
- [ ] Las seis subclases sobrescriben el método correspondiente.
- [ ] Los dos bucles llaman al método común sin condiciones por tipo.
- [ ] `recibir_dano()` no permite que el HP baje de cero.

---

## Nivel 2 — Intermedio: Inventario polimórfico con dunders

**Enunciado.** Construye el inventario de un RPG. Los objetos se pueden usar de formas distintas, pero el inventario los trata a todos igual. Además, el contenedor debe integrarse con la sintaxis de Python: `len()`, `for`, `in`, `+` y `print()`.

**Requisitos.**
- Crea `Objeto(ABC)` con `nombre`, `peso` validado (no negativo) y el método abstracto `usar() -> str`. Implementa `Arma` (inflige daño), `Pocion` (cura) y `Municion` (recarga una cantidad).
- Implementa `Inventario` con `__len__`, `__iter__`, `__contains__`, `__add__` y `__str__`. `__add__` debe devolver un inventario nuevo sin modificar los originales y retornar `NotImplemented` si el otro operando no es un inventario.
- En `main`, crea dos inventarios, fusiónalos con `+`, recorre el resultado con `for` y llama `usar()` en cada objeto. Muestra `len(total)`, comprueba si existe `"Poción"` con `in` e imprime el inventario con `print()`.

**Entrada esperada.**
Ninguna. Datos de ejemplo en el código.

**Salida esperada.**
```text
Inventario (4 objetos): Espada (3 kg), Poción (1 kg), Arco (2 kg), Flecha (1 kg)
Objetos totales: 4
¿Hay una poción? True
- Espada usa: 18 de daño
- Poción usa: recupera 25 HP
- Arco usa: dispara una flecha
- Flecha usa: recarga 10 flechas
```

**Criterios de evaluación.**
- [ ] `Inventario` responde correctamente a `len()`, `for`, `in`, `+` y `str()`.
- [ ] `__add__` no muta los inventarios originales.
- [ ] El recorrido llama `usar()` sin preguntar la clase del objeto.
- [ ] El peso negativo lanza `ValueError` con un mensaje claro.

---

## Nivel 3 — Reto obligatorio: Arcade — duelo por turnos

**Enunciado.** Crea un videojuego de consola 1 vs 1. Al iniciar, el jugador elige **un** personaje entre guerrero, mago y arquero. La máquina elige otro distinto al azar. Ambos se enfrentan por turnos hasta que uno llegue a 0 de HP. Cada clase debe tener un ataque propio y el motor del duelo debe ser polimórfico: una lista de personajes y una llamada a `atacar()` dentro del bucle, sin `isinstance`.

**Requisitos.**
- Define `Personaje(ABC)` con `nombre`, `hp`, `hp_maximo`, `vivo`, `recibir_dano(cantidad) -> int` y el método abstracto `atacar(objetivo) -> str`. El HP nunca debe bajar de cero.
- Implementa tres subclases:
  - `Guerrero`: golpe fuerte con daño base alto y una probabilidad de crítico.
  - `Mago`: hechizo con daño alto que consume maná; si no le alcanza, usa un ataque débil con el bastón.
  - `Arquero`: disparo con probabilidad de acertar y probabilidad de crítico. Un fallo hace 0 de daño.
  Usa `random` para las probabilidades y para la elección de la máquina.
- Crea `Duelo` con una lista de dos `Personaje`. El método `jugar()` alterna turnos (el jugador empieza), llama `atacar()` en cada turno y termina cuando uno muere. Está prohibido usar `isinstance`, `type(...) is` o cadenas de `elif` por clase.
- Menú inicial con opciones `1) Guerrero`, `2) Mago`, `3) Arquero`. Valida la entrada: si el usuario escribe algo distinto de `1`, `2` o `3`, muestra un error y vuelve a preguntar sin romper el programa.
- Registro de turnos claro: número de turno, quién ataca, nombre del ataque, daño real, HP restante del rival y aviso de KO.
- Al terminar, muestra al ganador y pregunta `¿Revancha? (s/n)`. Si responde `s`, se vuelve a elegir personaje y se juega otra vez; si responde `n`, se despide y termina. Valida también esa respuesta.
- La máquina debe elegir un personaje distinto al del jugador. Puedes implementarlo con una lista de clases disponibles y `random.choice`.

**Entrada esperada.**
```text
=== ARCADE: DUELO POR TURNOS ===
Elige tu personaje:
1) Guerrero
2) Mago
3) Arquero
> 9
Opción inválida. Escribe 1, 2 o 3.
> 2
Elegiste a Mago. La máquina eligió a Arquero.

--- Turno 1 ---
Mago usa Bola de fuego: 27 de daño. Arquero queda con 73 HP.
Arquero usa Disparo certero: 16 de daño. Mago queda con 79 HP.
...
¿Revancha? (s/n): s
```

**Salida esperada.**
El duelo completo con un turno por cada ataque, mensajes de ataque distintos según la clase, un ganador claro y la opción de revancha. Ejemplo de cierre:

```text
--- Turno 7 ---
Mago usa Bola de fuego: 29 de daño. Arquero queda con 0 HP.
¡Arquero ha caído! Gana Mago.

¿Revancha? (s/n): n
Gracias por jugar.
```

**Criterios de evaluación.**
- [ ] `Personaje` es abstracta y las tres subclases implementan `atacar()`.
- [ ] Cada especialidad tiene una mecánica propia: crítico, maná o probabilidad de acierto.
- [ ] El bucle de `Duelo` recorre la lista y llama `atacar()` sin `isinstance` ni `type(...) is`.
- [ ] El menú y la revancha validan entradas incorrectas sin lanzar excepciones.
- [ ] El registro muestra turno, ataque, daño y HP restante.
- [ ] El duelo termina exactamente cuando un personaje llega a 0 HP.
- [ ] La máquina nunca elige el mismo personaje que el jugador.
- [ ] Se puede jugar una revancha completa sin reiniciar el programa.

:::reto
Ampliación opcional: agrega una cuarta especialidad, `Paladín`, con un ataque que cure 10 HP antes de golpear. Si tu `Duelo` necesita cambios para aceptarla, todavía hay una decisión de tipo escondida en el motor.
:::
