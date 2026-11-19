# Ejercicios — Semana 03

## Nivel 1 — Básico: Inventario de la tienda

**Enunciado.**
Modela los ítems de la tienda de un RPG. Crea una clase `Item` con atributos de instancia `nombre`, `precio` y `stock`, y atributos de clase `IVA = 0.19` y `total_items` para contar cuántos ítems se han creado. Construye una lista con cuatro ítems y muestra el inventario y su valor total.

**Requisitos.**
- La clase debe llamarse `Item` y definirse con `class`.
- `__init__` debe recibir `nombre`, `precio` y `stock`, y usar `self` para guardar cada uno.
- Incrementar `Item.total_items` dentro de `__init__`, usando el nombre de la clase.
- Calcular el valor del inventario como `precio * stock` y sumarlo con un bucle o con `sum()`.
- Mostrar el precio con IVA usando `Item.IVA`. No lo copies en cada objeto.
- El script no debe pedir datos: usa una lista fija y ejecútalo con `python3 tienda.py`.

**Entrada esperada.**
Un archivo `tienda.py` con estos datos definidos en el código:

```python
items = [
    Item("Poción de vida", 15.0, 10),
    Item("Espada corta", 120.0, 3),
    Item("Escudo de madera", 80.0, 4),
    Item("Llave antigua", 45.0, 1),
]
```

**Salida esperada.**
```text
Ítem                 Precio    Stock   Subtotal
------------------------------------------------
Poción de vida        15.00       10     150.00
Espada corta         120.00        3     360.00
Escudo de madera      80.00        4     320.00
Llave antigua         45.00        1      45.00
------------------------------------------------
Ítems creados: 4
Valor sin IVA: 875.00
Valor con IVA: 1041.25
```

**Criterios de evaluación.**
- [ ] La clase `Item` está definida y se crean cuatro instancias distintas.
- [ ] `nombre`, `precio` y `stock` viven en cada objeto y se consultan con punto.
- [ ] `IVA` y `total_items` son atributos de clase.
- [ ] El contador se actualiza con `Item.total_items`, no con `self`.
- [ ] El total con IVA es correcto y el script corre sin errores.

---

## Nivel 2 — Intermedio: Party de héroes

**Enunciado.**
Crea una clase `Heroe` para armar un equipo de tres integrantes. Cada héroe tiene `nombre`, `clase` (guerrero, maga o arquera), `hp` y `nivel`. La clase debe tener `MAX_HP = 120` y un contador `total_heroes`. El programa debe mostrar la party, detectar al héroe con más vida, calcular el nivel promedio y comprobar que cada héroe pertenece a la clase con `isinstance()`.

**Requisitos.**
- `__init__(self, nombre: str, clase: str, hp: int, nivel: int)` con type hints.
- Si `hp` es menor que 0, guárdalo como `0`; si supera `Heroe.MAX_HP`, guárdalo como `MAX_HP`. Avisa con un `print` cuando ajustes un valor.
- Crear una función `mostrar_party(heroes: list[Heroe])` fuera de la clase que imprima una tabla.
- Calcular el promedio de nivel con `sum(...) / len(...)` y mostrarlo con dos decimales.
- Obtener al héroe con más hp usando `max(heroes, key=lambda h: h.hp)`.
- Imprimir el `__dict__` de cada héroe para verificar que `MAX_HP` no está dentro.

**Entrada esperada.**
```python
party = [
    Heroe("Aria", "maga", 90, 4),
    Heroe("Brom", "guerrero", 150, 3),   # se ajusta a 120
    Heroe("Cyd", "arquera", -10, 5),     # se ajusta a 0
]
```

**Salida esperada.**
```text
Ajuste: el hp de Brom no puede superar 120.
Ajuste: el hp de Cyd no puede ser negativo.

Party del jugador
-----------------
Aria     maga       hp  90/120   nivel 4
Brom     guerrero   hp 120/120   nivel 3
Cyd      arquera    hp   0/120   nivel 5

Integrantes: 3
Nivel promedio: 4.00
Más resistente: Brom (120 hp)
¿Aria es un Heroe? True

Aria: {'nombre': 'Aria', 'clase': 'maga', 'hp': 90, 'nivel': 4}
Brom: {'nombre': 'Brom', 'clase': 'guerrero', 'hp': 120, 'nivel': 3}
Cyd: {'nombre': 'Cyd', 'clase': 'arquera', 'hp': 0, 'nivel': 5}
```

**Criterios de evaluación.**
- [ ] Existen tres objetos `Heroe` independientes en una lista.
- [ ] Los hp fuera de rango se ajustan a los límites sin romper el programa.
- [ ] `MAX_HP` y `total_heroes` se leen desde la clase.
- [ ] La tabla y los cálculos usan los atributos de cada objeto, no listas paralelas.
- [ ] `isinstance()` se usa correctamente y `__dict__` no contiene `MAX_HP`.

---

## Nivel 3 — Reto: Estadísticas globales de la partida

**Enunciado.**
Estás registrando los resultados de varias partidas de un arcade. Crea una clase `Partida` con atributos de instancia `nombre`, `puntajes` (lista de enteros) y `rondas`. La clase debe llevar estadísticas globales: `total_partidas`, `puntaje_global` (suma de todos los puntos anotados) y `mejor_puntaje` (la puntuación más alta registrada). Al final, muestra un resumen de cada partida y el estado global.

**Requisitos.**
- `Partida.__init__(self, nombre: str, puntajes: list[int])` debe copiar la lista recibida en una lista propia: `self.puntajes = list(puntajes)`. No guardes la referencia original.
- `rondas` se calcula como la cantidad de puntajes.
- Define `total_partidas = 0`, `puntaje_global = 0` y `mejor_puntaje = 0` como atributos de clase.
- En `__init__`, actualiza los tres atributos globales con `Partida.total_partidas`, `Partida.puntaje_global` y `Partida.mejor_puntaje`.
- Valida sin excepciones: ignora puntajes negativos y avisa cuántos se descartaron. Si la lista queda vacía, deja `puntajes = [0]` y `rondas = 0`.
- Crea tres partidas con listas distintas y demuestra que modificar la lista original después de crear la partida no altera el objeto.
- Muestra el promedio por partida con dos decimales y el mejor puntaje global.

**Entrada esperada.**
```python
p1 = Partida("Noche de jefes", [120, 300, 80])
p2 = Partida("Carrera de picos", [50, 50, 75, 25])
p3 = Partida("Duelo final", [-20, 400])

# La lista original se modifica después de crear p1
puntajes_originales = [10]
p4 = Partida("Prueba de copia", puntajes_originales)
puntajes_originales.append(999)
```

**Salida esperada.**
```text
Aviso: 1 puntaje negativo descartado en Duelo final.

Noche de jefes      rondas 3   total 500   promedio 166.67
Carrera de picos    rondas 4   total 200   promedio  50.00
Duelo final         rondas 1   total 400   promedio 400.00
Prueba de copia     rondas 1   total  10   promedio  10.00

Partidas registradas: 4
Puntaje global: 1110
Mejor puntaje: 400

Copia segura: {'nombre': 'Prueba de copia', 'puntajes': [10], 'rondas': 1}
```

**Criterios de evaluación.**
- [ ] `puntajes` es una lista propia y no cambia cuando se modifica la lista original.
- [ ] Los tres atributos globales se actualizan correctamente y sobreviven a la creación de varias instancias.
- [ ] Los puntajes negativos se descartan con un aviso, sin usar excepciones.
- [ ] El caso de lista vacía no produce `ZeroDivisionError`.
- [ ] El resumen muestra totales y promedios coherentes con los datos.
- [ ] Se explica en un comentario por qué `puntajes` no puede ser un atributo de clase.
