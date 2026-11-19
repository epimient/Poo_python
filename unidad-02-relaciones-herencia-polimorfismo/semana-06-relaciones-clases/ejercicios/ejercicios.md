# Ejercicios — Semana 06

## Nivel 1 — Básico: Jugador y personaje (1:1)

**Enunciado.** Crea dos clases: `Personaje` y `Jugador`. Cada jugador tiene exactamente un personaje. El jugador puede cambiar de personaje sin destruir el anterior. Muestra por consola la ficha del jugador antes y después del cambio.

**Requisitos.**
- `Personaje` recibe `nombre`, `clase` y `nivel` (por defecto 1). Valida que el nombre no esté vacío y que el nivel sea al menos 1.
- `Personaje.subir_nivel(cantidad)` aumenta el nivel y recalcula `hp_max = 80 + nivel * 12`.
- `Jugador` recibe `alias` y un objeto `Personaje`. Guarda el objeto, no una copia del nombre.
- `Jugador.cambiar_personaje(nuevo)` reasigna la referencia.
- `__str__` en ambas clases con información legible.

**Entrada esperada.**
No hay entrada interactiva. Usa datos de ejemplo dentro de `if __name__ == "__main__":`:

```text
Ana controla a Kael (Mago, nivel 7)
Caro controla a Tork (Tanque, nivel 5)
```

**Salida esperada.**
```text
Antes:  Ana -> Kael (Mago, nivel 7, 164 HP)
Después: Ana -> Nia (Sanadora, nivel 1, 92 HP)
Kael sigue existiendo con nivel 8 tras subir_nivel().
```

**Criterios de evaluación.**
- [ ] `Jugador.personaje` es una referencia a un objeto `Personaje`.
- [ ] El cambio de personaje no borra ni modifica el personaje anterior.
- [ ] Se valida nombre vacío y nivel inválido con `ValueError`.
- [ ] El script ejecuta de principio a fin con `python3`.
- [ ] Se usan type hints simples y `__str__` en ambas clases.

---

## Nivel 2 — Intermedio: El gremio (1:N con reglas)

**Enunciado.** Implementa `Gremio` y `Aventurero`. Un gremio agrupa aventureros (1:N), con un máximo de 4 integrantes. Un aventurero pertenece como máximo a un gremio. Debes poder inscribir, retirar, listar la plantilla y calcular el nivel promedio.

**Requisitos.**
- `Aventurero`: `alias`, `clase`, `nivel`, y `gremio: Gremio | None = None`.
- `Gremio`: nombre, cupo máximo, lista **privada** de integrantes.
- `inscribir(aventurero)` valida: cupo disponible, que no esté ya en este gremio y que no pertenezca a otro.
- `retirar(alias)` devuelve el aventurero y limpia `aventurero.gremio`.
- `plantilla()` devuelve una lista de textos, no objetos.
- `promedio_nivel()` devuelve `0.0` si el gremio está vacío.
- Propiedad `integrantes` que devuelva una tupla (vista de solo lectura).

**Entrada esperada.**
Datos de ejemplo: un gremio con cupo 3 y cuatro aventureros de niveles 4, 6, 8 y 10. Intenta inscribir a los cuatro.

**Salida esperada.**
```text
Gremio Alba (3/3)
  1. Ana    -> Kael (Mago, nivel 8)
  2. Beto   -> Runa (Arquera, nivel 6)
  3. Caro   -> Tork (Tanque, nivel 10)
Promedio: 8.0
✗ El gremio está lleno (3 cupos).
✗ Duna ya pertenece a Los Eclipse.
```

**Criterios de evaluación.**
- [ ] La lista interna no se puede mutar desde fuera del gremio.
- [ ] Se rechazan duplicados y aventureros que ya tienen gremio.
- [ ] `retirar` deja `aventurero.gremio = None`.
- [ ] Se lanza `ValueError` con mensajes que explican la causa.
- [ ] La demo no depende de `input()`.

---

## Nivel 3 — Reto: Modelado UML de un RPG (N:M)

**Enunciado.** Modela un RPG de partidas cortas con cuatro clases: `Jugador`, `Personaje`, `Equipo` y `Partida`. Entrega primero un diagrama UML en texto con cardinalidades y después el código.

**Requisitos.**
- 1:1 entre `Jugador` y `Personaje`.
- 1:N entre `Equipo` y `Jugador`, con cupo de 4 y equipo único por jugador.
- N:M entre `Jugador` y `Partida`: un jugador puede jugar varias partidas y una partida admite varios jugadores (máximo 4).
- Un jugador no puede inscribirse dos veces en la misma partida.
- La partida debe registrar el equipo ganador mediante `finalizar(equipo_ganador)`; solo se puede finalizar una vez y el ganador debe haber participado.
- `resumen()` de la partida muestra nombre, inscritos y estado.

**Entrada esperada.**
Una demo que:
1. Cree 2 equipos de 2 jugadores cada uno.
2. Inscriba a los 4 jugadores en una partida.
3. Intente inscribir a uno repetido y muestre el error.
4. Finalice la partida con un equipo participante.
5. Intente finalizar de nuevo y muestre el error.

**Salida esperada.**
```text
Partida "Copa de Otoño" (4/4 inscritos) — en curso
✗ Ana ya está inscrita en esta partida.
Partida "Copa de Otoño" (4/4 inscritos) — ganó Los Cometas
✗ La partida ya fue finalizada.
```

**Criterios de evaluación.**
- [ ] El diagrama UML indica 1:1, 1:N y N:M con cardinalidades correctas.
- [ ] Las dos listas de la N:M se actualizan en el mismo método.
- [ ] Se valida el cupo de la partida y la inscripción duplicada.
- [ ] `finalizar` valida que el ganador haya participado y no permite doble cierre.
- [ ] La relación 1:N mantiene coherente `jugador.equipo`.
- [ ] El código ejecuta con `python3` y no usa dependencias externas.

---

## Criterios generales de entrega

- [ ] Los tres archivos ejecutan sin errores con `python3`.
- [ ] Nombres en `snake_case` para variables y métodos, `PascalCase` para clases.
- [ ] Cada clase tiene un docstring breve.
- [ ] Las validaciones usan `ValueError`, nunca `assert`.
- [ ] No se usan `dataclasses`, frameworks ni librerías externas.
