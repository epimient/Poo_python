# Ejercicios — Semana 08

## Nivel 1 — Básico: Jerarquía de enemigos

**Enunciado.** Crea `enemigos.py` con una clase base `Enemigo` y dos subclases: `Slime` y `Dragon`. La base debe tener `nombre`, `vida` y un método `atacar()` que devuelva un daño básico. Cada subclase sobrescribe `atacar()` con su propia regla y añade un atributo propio.

**Requisitos.**
- `Enemigo` define `__init__(self, nombre: str, vida: int)` y `atacar(self) -> int`.
- `Slime` añade `salto: int` y su ataque suma ese valor.
- `Dragon` añade `aliento: int`; si `aliento > 0`, lo gasta y suma el doble; si no, ataca con el daño base.
- Cada subclase llama a `super().__init__()`.
- El script crea una lista con un `Slime` y un `Dragon`, y muestra el daño de cada uno.

**Entrada esperada.**
Ninguna. El programa usa datos de ejemplo dentro de `if __name__ == "__main__":`.

**Salida esperada.**
```text
Slime viscoso ataca por 7
Dragon rojo ataca por 22
Dragon rojo ataca por 11
```

**Criterios de evaluación.**
- [ ] `Enemigo` contiene solo lo común a todos los enemigos.
- [ ] Las dos subclases usan `super().__init__()`.
- [ ] `atacar()` está sobrescrito en ambas subclases.
- [ ] El bucle recorre una `list[Enemigo]` sin preguntar por la clase.
- [ ] El script ejecuta con `python3 enemigos.py` sin errores.

---

## Nivel 2 — Intermedio: `super()` y estadísticas

**Enunciado.** Amplía una jerarquía de personajes con estadísticas y un ataque especial. Crea `Personaje` con `nombre`, `vida`, `ataque_base` y `energia`. Luego crea `Guerrero`, `Mago` y `Arquero`. Cada uno debe inicializar la base con `super().__init__()`, sobrescribir `atacar()` y ofrecer un método `especial()` que consuma energía.

**Requisitos.**
- `Personaje.recibir_dano(cantidad)` nunca deja la vida por debajo de 0.
- `Personaje.esta_vivo()` devuelve un booleano.
- Cada subclase define su constructor con valores propios y llama a la base.
- `especial()` solo funciona si hay energía suficiente; si no, devuelve 0 e informa el motivo.
- Agrega `resumen()` en la base y sobrescríbelo en al menos una subclase usando `super().resumen()`.
- Simula tres rondas de combate contra un enemigo con 100 PV e imprime el estado al final de cada ronda.
- Valida en el constructor que `vida > 0` y que `energia >= 0`; lanza `ValueError` si no se cumple.

**Entrada esperada.**
Ninguna. Datos de ejemplo: un guerrero, un mago y un arquero contra un enemigo de 100 PV.

**Salida esperada.**
```text
Ronda 1
Ragnar (120 PV) golpea por 16
Morgana (80 PV) lanza un hechizo por 21
Lyra (90 PV) dispara por 12
Enemigo: 51 PV

...
Ragnar | Guerrero | 120 PV | energía 20
```

**Criterios de evaluación.**
- [ ] La base se inicializa una sola vez por objeto.
- [ ] `super().resumen()` se usa sin duplicar el texto de la base.
- [ ] Las validaciones lanzan `ValueError` con un mensaje claro.
- [ ] `especial()` respeta el coste de energía.
- [ ] El combate termina correctamente cuando alguna vida llega a 0.
- [ ] Se usa type hint `list[Personaje]` para el equipo.

---

## Nivel 3 — Reto: Cuándo NO heredar

**Enunciado.** Tienes un inventario de videojuego con armas, armaduras y pociones. El error tentador es hacer `class Espada(Inventario)` para reutilizar la lista de objetos. Tu tarea es diseñar el modelo **sin herencia forzada**: usa composición y una jerarquía pequeña solo donde exista una relación es-un real.

**Requisitos.**
- `Item` es una clase base con `nombre`, `precio` y `describir()`.
- `Arma(Item)` añade `dano`; `Armadura(Item)` añade `defensa`; `Pocion(Item)` añade `curacion`.
- `Inventario` **no hereda** de `Item`: tiene una lista de objetos `Item` y métodos `agregar()`, `valor_total()` y `listar()`.
- `agregar()` valida que el objeto sea un `Item` y que el precio no sea negativo; lanza `TypeError` o `ValueError` según corresponda.
- `Personaje` tiene un `Inventario` (composición) y un método `equipar(item: Item)` que solo acepta armas o armaduras; una poción debe rechazarse con un mensaje claro.
- Si un objeto se agrega dos veces, el inventario debe permitirlo solo si su cantidad lo permite; para simplificar, cada `Item` tiene `cantidad` y `agregar()` suma unidades.
- Escribe al final del archivo un comentario de 3–5 líneas explicando por qué `Inventario` no hereda de `Item` y qué ganaste con composición.

**Entrada esperada.**
Ninguna. El demo agrega una espada, una armadura, dos pociones y un objeto inválido.

**Salida esperada.**
```text
Inventario de Ragnar:
- Espada corta | daño 12 | x1
- Cota de malla | defensa 8 | x1
- Poción menor | cura 20 | x2
Valor total: 210 monedas
Error: una poción no se puede equipar como arma
Error: el precio no puede ser negativo
```

**Criterios de evaluación.**
- [ ] `Inventario` contiene objetos, no hereda de ellos.
- [ ] Solo existe herencia donde hay una relación es-un verificable.
- [ ] Las validaciones usan excepciones y mensajes comprensibles.
- [ ] `equipar()` distingue armas y armaduras sin romper el tipo base.
- [ ] El comentario final justifica la decisión de diseño con argumentos, no con una frase genérica.
- [ ] El script ejecuta de principio a fin con `python3 inventario.py`.
