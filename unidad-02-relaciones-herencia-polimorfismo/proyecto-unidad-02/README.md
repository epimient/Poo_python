# P2 · Arcade de combate por turnos

**Unidad 2 — Relaciones, herencia y polimorfismo** · Semana 11 · **30% de la nota final** · Equipos de 2 a 3 personas

---

## Contexto

El prototipo de RPG de la unidad anterior creció: ahora hay guerreros, magos y arqueros que deben enfrentarse en un **arcade de combate por turnos**. El jugador elige un personaje, la máquina elige otro y la batalla se resuelve turno a turno. Cada clase ataca distinto, pero el motor de combate no debe preguntar de qué tipo es cada personaje: solo debe enviarle el mensaje `atacar()`.

Tu equipo debe construir ese arcade en consola, aplicando relaciones entre clases, herencia, clases abstractas y polimorfismo.

---

## Objetivo

Diseñar un videojuego de consola donde dos personajes (jugador vs. máquina), elegidos entre **guerrero, mago y arquero**, se enfrenten por turnos hasta que uno quede sin HP, manteniendo una arquitectura orientada a objetos limpia y extensible.

---

## Requisitos funcionales

1. **Menú principal** con: nueva partida, instrucciones, historial de la última partida y salir.
2. **Selección de personaje**: el jugador elige entre guerrero, mago o arquero; la máquina elige otro al azar.
3. **Combate por turnos**:
   - El jugador ataca o usa su habilidad especial.
   - La máquina responde automáticamente.
   - Se muestra el daño, el HP restante y el estado de cada personaje.
4. **Habilidades propias**:
   - Guerrero: golpe fuerte que consume furia.
   - Mago: hechizo que consume maná y puede ser más potente.
   - Arquero: disparo con opción de crítico y munición limitada.
5. **Condición de victoria**: gana quien deje al otro en 0 HP. Debe anunciarse el ganador y permitir revancha.
6. **Historial** de la última partida con el resumen de turnos.
7. **Validación de entradas** y mensajes claros; el programa no debe caerse.

---

## Requisitos técnicos

### CE2.1 — Relaciones entre clases (50%)

- Modela al menos **tres entidades relacionadas**, por ejemplo:
  - `Personaje` y `Arma` (asociación).
  - `Inventario` e `Item` (composición).
  - `Equipo` y `Personaje` (agregación).
  - `Combate` y `Personaje` (asociación con multiplicidad 2).
- Implementa **agregación** y **composición** en el modelo, no solo en el discurso.
- Documenta las relaciones con un **diagrama UML** en el README (texto o imagen).
- Justifica por qué cada relación es asociación, agregación o composición.
- Las entidades deben tener responsabilidades claras y no convertir una clase en un “dios”.

### CE2.2 — Clases abstractas, contratos y polimorfismo (50%)

- Define una clase abstracta `Personaje(ABC)` con al menos:
  - Método abstracto `atacar()`.
  - Método abstracto `habilidad_especial()`.
  - Atributos comunes: nombre, hp, hp_max, ataque, defensa, vivo.
- Implementa **tres subclases**: `Guerrero`, `Mago` y `Arquero`, cada una con su propia versión de los métodos.
- Usa `super().__init__()` correctamente.
- El motor de combate debe recorrer una lista de `Personaje` y llamar `atacar()` **sin usar `isinstance()` ni `if tipo == ...`** para decidir el ataque.
- Implementa al menos un **contrato de comportamiento adicional**: un `Protocol` (`Curable`, `Defendible`) o una segunda clase abstracta (`Habilidad`).
- Usa `__str__` o `estado()` para mostrar la información de combate.
- Incluye una **extensión polimórfica**: que agregar un cuarto personaje (por ejemplo, `Paladin`) no obligue a modificar el bucle de combate.

---

## Entregables

| Entregable | Descripción |
|---|---|
| Código fuente | Organizado en módulos: `main.py`, `personajes.py`, `combate.py`, `objetos.py` (o similar) |
| `README.md` | Instrucciones, diagrama UML, decisiones de diseño y ejemplo de partida |
| Video de 3–5 minutos | Demostración de una partida completa y explicación del diseño |
| Sustentación | Cada integrante explica una parte distinta: modelo, combate, UI de consola |

---

## Ejemplo de partida

```text
=== ARCADE: DUELO POR TURNOS ===
1. Nueva partida
2. Instrucciones
3. Historial
4. Salir

Elige una opción: 1

Elige tu personaje:
1. Guerrero  (HP 120 · ATK 18 · Furia 0/100)
2. Mago      (HP 80  · ATK 12 · Maná 100/100)
3. Arquero   (HP 95  · ATK 15 · Flechas 10)

> 2

La máquina eligió: Guerrero

--- TURNO 1 ---
Tu mago lanza Bola de fuego. ¡28 de daño!
Guerrero enemigo: 92/120 HP.

El guerrero enemigo usa Golpe aplastante. ¡16 de daño!
Tu mago: 64/80 HP.

--- TURNO 2 ---
...
```

---

## Rúbrica de evaluación

**P2 = CE2.1 (50%) + CE2.2 (50%)**

### CE2.1 — Relaciones entre clases (50%)

| Nivel | Descriptor |
|---|---|
| Excelente (5.0) | Modela e implementa correctamente asociación, agregación, composición y herencia; justifica su selección y logra una solución coherente. |
| Sobresaliente (4.6–4.9) | Implementa correctamente las relaciones requeridas, con pequeñas inconsistencias de diseño. |
| Bueno (4.0–4.5) | Implementa las relaciones principales de manera funcional. |
| Aceptable (3.0–3.9) | Reconoce las relaciones, pero presenta dificultades para seleccionarlas o implementarlas correctamente. |
| No aceptable (1.0–2.9) | No diferencia ni implementa adecuadamente las relaciones entre clases. |

### CE2.2 — Abstractas, contratos y polimorfismo (50%)

| Nivel | Descriptor |
|---|---|
| Excelente (5.0) | Integra abstracción y polimorfismo de forma correcta, reutilizable y extensible; evidencia un diseño sólido. |
| Sobresaliente (4.6–4.9) | Implementa adecuadamente abstracción y polimorfismo, con errores mínimos. |
| Bueno (4.0–4.5) | Utiliza clases abstractas y polimorfismo de manera funcional, con oportunidades de mejora. |
| Aceptable (3.0–3.9) | Implementa parcialmente estos mecanismos y requiere orientación para integrarlos. |
| No aceptable (1.0–2.9) | No logra implementar clases abstractas, contratos o comportamiento polimórfico. |

---

## Checklist de autoevaluación

- [ ] El juego ejecuta con `python3 main.py` y permite jugar una partida completa.
- [ ] Existe `Personaje(ABC)` con métodos abstractos.
- [ ] Existen `Guerrero`, `Mago` y `Arquero`, todos usan `super().__init__()`.
- [ ] El bucle de combate no usa `isinstance()` para decidir ataques.
- [ ] Cada clase tiene ataque y habilidad especial distintos.
- [ ] Se usa agregación y composición en el modelo.
- [ ] El README incluye el diagrama UML y justifica las relaciones.
- [ ] El historial de la partida se muestra correctamente.
- [ ] Las entradas inválidas no rompen el programa.
- [ ] Agregar un nuevo personaje solo requiere crear una subclase.

---

## Preguntas de sustentación

1. ¿Por qué el bucle de combate no necesita saber si el personaje es guerrero, mago o arquero?
2. ¿Cuál es la diferencia entre agregación y composición en tu modelo? Señala un ejemplo concreto.
3. ¿Qué ventaja aporta `ABC` frente a una clase base con `raise NotImplementedError`?
4. ¿Dónde se cumple el principio de sustitución de Liskov en tu jerarquía?
5. Si el juego necesitara un `Paladín`, ¿qué archivos cambiarías y por qué?
6. ¿Qué parte del código concentra demasiadas responsabilidades y cómo la dividirías?

---

## Política de entrega

- Entrega en la fecha indicada; se revisa avance y versión final.
- Un proyecto que no ejecuta obtiene como máximo **3.0**.
- Trabajo copiado entre equipos: **0 automático**.
- La sustentación es obligatoria. Todos los integrantes deben poder explicar cualquier parte del código.
