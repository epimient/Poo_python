# Dudas frecuentes — Semana 02

## ¿Un lenguaje pertenece a un solo paradigma?

No. Python permite escribir código imperativo, funcional y orientado a objetos en el mismo programa. Lo que define el paradigma es cómo organizas el pensamiento y la estructura principal, no la marca del lenguaje. Java favorece la POO, pero también admite lambdas y streams; Python favorece la mezcla pragmática.

Lo importante es que la estructura elegida sea coherente. Un archivo con clases vacías y funciones sueltas que hacen todo el trabajo no es POO: es un script procedural disfrazado.

## ¿La POO siempre es mejor que el procedural?

No. Para un cálculo pequeño, una transformación de datos o un script de una sola ejecución, una función es más clara y más fácil de probar. La POO brilla cuando hay varias entidades con estado, reglas propias y relaciones que cambian con el tiempo.

La pregunta útil es: **¿quién debería ser dueño de este dato y de esta regla?** Si la respuesta es «un objeto con identidad propia», una clase es razonable. Si es «una operación que transforma una entrada», una función basta.

## ¿Cómo se usa el paradigma funcional en este curso?

Como apoyo, no como estructura principal. Verás comprensiones de listas, `sum()`, `sorted()` con `key`, funciones que devuelven valores sin modificar sus argumentos y, más adelante, funciones como `command` en Tkinter. La idea funcional de **evitar efectos secundarios** mejora cualquier diseño orientado a objetos.

```python
def calcular_dano(ataque: int, defensa: int) -> int:
    return max(1, ataque - defensa)

danos = [calcular_dano(20, defensa) for defensa in (5, 10, 15)]
print(danos)  # [15, 10, 5]
```

Esta función no imprime, no guarda estado y siempre devuelve lo mismo para las mismas entradas. Es fácil de probar y de reutilizar.

## ¿Es obligatorio entregar el diagrama UML?

Sí, cuando el enunciado lo pide. UML no es un adorno: es la evidencia de que pensaste el diseño antes de codificar. No se evalúa la belleza del dibujo, sino la coherencia entre clases, atributos, métodos y relaciones.

Puedes entregarlo en texto plano dentro de un bloque de código o como imagen exportada. Si usas una herramienta externa, verifica que el archivo abra y que el texto sea legible. Un diagrama con cinco clases y una relación clara vale más que uno con veinte clases y flechas cruzadas.

## ¿Ágil significa que no hay que planificar?

Al contrario: ágil significa planificar en ciclos cortos y ajustar con evidencia. Un equipo ágil mantiene un backlog priorizado, define un objetivo por iteración y revisa el resultado con quien lo usa. Lo que evita es el plan rígido de seis meses que nadie actualiza.

Para el curso, un tablero con tres columnas (*Pendiente*, *En curso*, *Hecho*) y una reunión semanal de quince minutos son suficientes. Si el equipo no sabe qué sigue, el problema no es la metodología: es que el backlog no está priorizado.

## ¿Por qué usar ramas en Git si trabajo solo?

Porque una rama te permite experimentar sin romper la versión que funciona. Puedes intentar un refactor, probarlo y, si sale mal, volver a `main` sin perder el trabajo anterior. También te obliga a integrar de forma consciente.

```bash
git switch -c feature/validaciones
# trabajar y probar
git add personaje.py
git commit -m "Agrega validación de hp"
git switch main
git merge feature/validaciones
```

En equipo, la rama evita que dos personas editen la misma línea de `main` al mismo tiempo. La regla mínima: `main` siempre ejecuta; las funcionalidades viven en ramas cortas.

## ¿Cómo se calcula la nota del curso?

La nota final se compone de tres proyectos, sin exámenes escritos:

```text
Nota final = P1 × 0.25 + P2 × 0.30 + P3 × 0.45
```

- **P1 (semana 5, individual):** creador de personajes RPG por consola.
- **P2 (semana 11, equipos de 2–3):** arcade de combate por turnos.
- **P3 (semana 15, equipos de 2–3):** arcade con interfaz gráfica.

Cada proyecto tiene dos criterios que pesan 50/50. Un proyecto que no ejecuta obtiene como máximo 3.0; una copia obtiene 0. La sustentación es obligatoria por integrante: debes poder explicar el código que entregas.

## ¿Qué hago si un integrante del equipo no participa?

Primero, documenta el acuerdo: quién hace qué, con qué fecha y cómo se revisa. Usa el tablero y los commits como evidencia. Habla con la persona antes de escalar; a veces el problema es una tarea mal dimensionada o una fecha poco realista.

Si persiste, informa al docente con evidencia concreta (fechas, tareas asignadas, commits, mensajes) y no esperes al día de la entrega. La evaluación considera la sustentación individual: quien no participó no puede defender lo que no hizo. El objetivo no es castigar, sino que el equipo termine y que cada nota refleje el trabajo real.
