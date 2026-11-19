# P1 · Creador de personajes RPG

**Unidad 1 — Fundamentos de POO** · Semana 5 · **25% de la nota final** · Individual

---

## Contexto

Un estudio pequeño está prototipando un RPG por turnos y necesita una herramienta de consola para crear y administrar los personajes del juego antes de invertir en gráficos. Tu tarea es construir ese **creador de personajes** aplicando clases, objetos, constructores, atributos, métodos y encapsulamiento.

No se permite usar bases de datos, interfaces gráficas ni librerías externas. Todo debe resolverse con Python 3.12 y la biblioteca estándar.

---

## Objetivo

Diseñar una aplicación de consola que permita crear personajes, consultar su estado, entrenarlos, curarlos y simular combates básicos, manteniendo siempre la **consistencia del estado** de cada objeto.

---

## Requisitos funcionales

1. **Crear personaje** solicitando nombre, clase (guerrero, mago o arquero) y nivel inicial.
2. **Listar personajes** creados con su estado actual.
3. **Ver el detalle** de un personaje: atributos, si está vivo y su poder de ataque.
4. **Entrenar** un personaje para subir de nivel y mejorar sus estadísticas.
5. **Curar** un personaje sin superar su HP máximo.
6. **Simular un combate** de práctica entre dos personajes creados.
7. **Salir** del programa con un mensaje de despedida.

El programa debe funcionar en un bucle de menú, tolerar entradas inválidas y no caerse ante errores del usuario.

---

## Requisitos técnicos

### CE1.1 — Clases, objetos, atributos, métodos y constructores

- Define una clase `Personaje` con constructor `__init__`.
- Usa al menos **8 atributos de instancia** (nombre, clase, nivel, hp, hp_max, ataque, defensa, vivo, entre otros).
- Usa al menos **un atributo de clase** (por ejemplo `MAX_NIVEL = 100` o un contador de personajes creados).
- Implementa al menos **6 métodos**, entre ellos `atacar()`, `recibir_danio()`, `curar()` y `subir_nivel()`.
- Crea una segunda clase de apoyo (`Menu`, `Juego` o `GestorPersonajes`) que coordine la aplicación.
- Instancia objetos y demuestra su uso en el flujo real del programa.
- Implementa `__str__` para mostrar el estado del personaje de forma legible.

### CE1.2 — Encapsulamiento y validaciones

- Todos los atributos sensibles deben ser **privados o protegidos** (`__nombre`, `__hp`, `__nivel`, etc.).
- El acceso y la modificación deben hacerse mediante **properties** y métodos públicos.
- Valida como mínimo:
  - El nombre no puede estar vacío ni tener menos de 3 caracteres.
  - El nivel debe estar entre 1 y `MAX_NIVEL`.
  - El HP debe estar entre 0 y `hp_max`.
  - El ataque y la defensa no pueden ser negativos.
  - La clase debe ser una de las permitidas.
- Lanza `ValueError` con mensajes claros cuando una validación falla.
- Ninguna operación debe dejar al personaje en un estado inconsistente (por ejemplo, HP negativo o nivel fuera de rango).
- Captura los errores en el menú y muestra un mensaje amigable, sin cerrar el programa.

---

## Entregables

| Entregable | Descripción |
|---|---|
| `main.py` | Punto de entrada de la aplicación |
| `personaje.py` | Clase `Personaje` y clases de apoyo del modelo |
| `README.md` | Instrucciones de ejecución, decisiones de diseño y ejemplo de uso |
| Video de 3–5 minutos | Demostración del programa y explicación del código |
| Sustentación | Cada estudiante explica cualquier parte de su código |

Puedes organizar el código en un solo archivo si lo prefieres, pero la separación por módulos es recomendable.

---

## Ejemplo de ejecución

```text
=== CREADOR DE PERSONAJES RPG ===
1. Crear personaje
2. Listar personajes
3. Ver detalle
4. Entrenar
5. Curar
6. Combatir
7. Salir

Elige una opción: 1
Nombre: Lyra
Clase (guerrero/mago/arquero): mago
Nivel inicial (1-100): 5

✔ Personaje creado:
Lyra · Mago · Nivel 5
HP 80/80 · ATK 18 · DEF 8 · Vivo
```

```text
Elige una opción: 4
¿Qué personaje? Lyra
Lyra subió al nivel 6. HP máximo: 88. Ataque: 20.
```

```text
Elige una opción: 5
¿Qué personaje? Lyra
Curación aplicada. HP: 88/88.
```

---

## Rúbrica de evaluación

**P1 = CE1.1 (50%) + CE1.2 (50%)**

### CE1.1 — Define e instancia clases, atributos, métodos y constructores (50%)

| Nivel | Descriptor |
|---|---|
| Excelente (5.0) | Diseña e implementa correctamente la clase, sus atributos, métodos y constructor; instancia objetos y los integra de forma autónoma y coherente en la aplicación. |
| Sobresaliente (4.6–4.9) | Implementa correctamente los elementos de la clase y los objetos, con errores mínimos que no afectan la solución. |
| Bueno (4.0–4.5) | Implementa una clase y objetos funcionales con algunas inconsistencias menores. |
| Aceptable (3.0–3.9) | Implementa parcialmente la clase y los objetos; requiere orientación para completar la solución. |
| No aceptable (1.0–2.9) | Presenta dificultades significativas para definir clases, objetos, atributos, métodos y constructores. |

### CE1.2 — Encapsulamiento y validaciones (50%)

| Nivel | Descriptor |
|---|---|
| Excelente (5.0) | Aplica correctamente encapsulamiento, properties y validaciones; garantiza la consistencia del estado de los objetos en todos los flujos. |
| Sobresaliente (4.6–4.9) | Aplica adecuadamente encapsulamiento y validaciones, con errores mínimos. |
| Bueno (4.0–4.5) | Implementa mecanismos básicos de encapsulamiento y validación de forma funcional. |
| Aceptable (3.0–3.9) | Implementa parcialmente el encapsulamiento, con deficiencias en las validaciones o en el control del estado. |
| No aceptable (1.0–2.9) | No aplica encapsulamiento ni garantiza la integridad de los objetos. |

---

## Checklist de autoevaluación

- [ ] El programa ejecuta con `python3 main.py` sin errores.
- [ ] Existe una clase `Personaje` con constructor y al menos 8 atributos.
- [ ] Existe al menos un atributo de clase.
- [ ] Hay al menos 6 métodos, incluidos `atacar()`, `recibir_danio()`, `curar()` y `subir_nivel()`.
- [ ] Los atributos sensibles son privados o protegidos.
- [ ] Se usan properties con validación.
- [ ] Se lanzan y capturan errores con mensajes claros.
- [ ] El menú no se cae con entradas inválidas.
- [ ] El HP nunca queda negativo ni supera el máximo.
- [ ] El nivel nunca sale del rango permitido.
- [ ] El README explica cómo ejecutar y qué decisiones se tomaron.
- [ ] El video muestra el programa funcionando de principio a fin.

---

## Preguntas de sustentación

1. ¿Cuál es la diferencia entre un atributo de clase y uno de instancia? Da un ejemplo de tu código.
2. ¿Por qué usaste `__atributo` en lugar de `atributo`? ¿Qué ocurre si alguien intenta modificarlo directamente?
3. ¿Qué pasa si se llama `curar()` con un valor negativo? ¿Dónde se controla?
4. ¿Qué responsabilidad tiene la clase de menú frente a la clase `Personaje`?
5. ¿Qué cambiarías si mañana el juego necesitara tres tipos de personaje con ataques distintos?

---

## Política de entrega

- Entrega en la fecha indicada por el docente; se revisa avance y versión final.
- Un proyecto que no ejecuta obtiene como máximo **3.0**.
- Trabajo copiado entre compañeros: **0 automático**.
- La sustentación es obligatoria. Si un integrante no puede explicar su código, se revisa su nota individual.
