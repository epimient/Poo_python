# Ejemplo guiado — Combate por turnos

## Qué construye

Un combate de exhibición entre dos equipos de tres personajes. Cada especialidad responde a `atacar()` con una mecánica propia:

- **Guerrero**: golpe fuerte con probabilidad de crítico demoledor.
- **Mago**: hechizo que consume maná y golpe de bastón cuando se queda sin maná.
- **Arquero**: disparo con probabilidad de acierto y de crítico.

El motor `Combate` recorre una lista de `Personaje`, elige un rival y llama `atacar()`. No pregunta clases, no usa `isinstance` y no necesita cambiar cuando agregas una especialidad nueva.

## Archivos

| Archivo | Contenido |
|---|---|
| `combate_turnos.py` | Combate completo de 6 turnos con datos de ejemplo |
| `dunders_y_despacho.py` | Inventario con dunders, `Protocol` y `singledispatch` |

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 combate_turnos.py
python3 dunders_y_despacho.py
```

No pide datos: la demo usa un `random.Random(2026)` para que la salida sea reproducible.

## Salida esperada (fragmento)

```text
=== COMBATE POR TURNOS ===
  Brunilda [Guerrero] (Héroes) 150/150 HP
  Merlín [Mago] (Héroes) 95/95 HP
  ...

--- Turno 1 ---
Brunilda  -> Morgana   golpe de espada: 19 de daño      | Morgana: 71 HP
Merlín    -> Morgana   bola de fuego: 30 de daño ...    | Morgana: 41 HP
Lyra      -> Morgana   flecha certera: 18 de daño       | Morgana: 23 HP
...

=== RESULTADO ===
Equipo ganador: Héroes
```

El segundo script muestra el inventario respondiendo a `len()`, `for`, `in`, `+` y `print()`, dos clases que cumplen un `Protocol` sin heredar de él, y tres tipos de daño resueltos con `singledispatch`.

## Puntos clave

1. **Contrato único.** `Personaje` declara `atacar()` como `@abstractmethod`; las subclases están obligadas a implementarlo.
2. **Lógica compartida.** `recibir_dano()` y `vivo` viven en la clase base para no duplicarlos.
3. **Cliente estable.** `Combate` depende de `Personaje`; agregar un paladín solo requiere una clase nueva.
4. **Estado encapsulado.** El HP se modifica únicamente mediante `recibir_dano()`, que nunca baja de cero.
5. **Azar controlado.** Cada personaje recibe un `random.Random` compartido en la demo, lo que permite repetir la misma batalla.

## Cómo comprobar que es polimórfico

Busca `isinstance` en `combate_turnos.py`:

```bash
grep -n "isinstance" combate_turnos.py
```

No debe haber coincidencias. El único punto donde se decide el comportamiento es el método `atacar()` de cada subclase.
