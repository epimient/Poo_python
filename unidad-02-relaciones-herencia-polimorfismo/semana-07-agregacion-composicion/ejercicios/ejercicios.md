# Ejercicios — Semana 07

## Nivel 1 — Básico: Mochila de consumibles

**Enunciado.** Implementa `Mochila` e `Item` con una relación de **composición**. La mochila crea sus ítems, los guarda en una lista privada y los destruye cuando se consumen o cuando la mochila desaparece.

**Requisitos.**
- `Item`: nombre, tipo y valor. Valida nombre no vacío y valor no negativo.
- `Mochila`: dueño, capacidad (por defecto 5) y lista privada.
- `crear_item(nombre, tipo, valor)` valida capacidad y nombres duplicados.
- `consumir(nombre)` elimina el ítem y devuelve un texto descriptivo.
- `fichas()` devuelve una lista de textos, no de objetos.
- `total_valor()` y `__len__`.
- La demo crea tres ítems, consume uno y muestra el total.

**Entrada esperada.**
Sin entrada interactiva. Datos: dueño `"Kael"`, ítems `"Espada corta"` (120), `"Poción"` (40), `"Amuleto"` (90).

**Salida esperada.**
```text
Mochila de Kael (3/5)
  - Espada corta [arma] · 120 de oro
  - Poción [consumible] · 40 de oro
  - Amuleto [accesorio] · 90 de oro
Total: 250
Se consumió Poción.
Mochila de Kael (2/5) · total 210
```

**Criterios de evaluación.**
- [ ] Los ítems se crean dentro del método de la mochila.
- [ ] La lista interna es privada y no se expone.
- [ ] Se validan capacidad, duplicados y valores negativos.
- [ ] Consumir un ítem inexistente lanza `ValueError`.
- [ ] El script ejecuta con `python3` sin dependencias externas.

---

## Nivel 2 — Intermedio: La tienda y el traspaso de dueño

**Enunciado.** Modela una tienda de pociones. `Tienda` **compone** su stock de `Producto`: los crea y es su dueña. `Cliente` **agrega** productos comprados: los recibe de la tienda y sobreviven a ella. Al vender, el producto se retira del stock y se agrega al cliente: hay un traspaso de ownership, no una copia.

**Requisitos.**
- `Producto`: nombre, precio y `propietario` (texto).
- `Tienda`: nombre, lista privada de productos, `crear_producto(nombre, precio)`.
- `vender(cliente, nombre)`: busca el producto, lo retira del stock, cambia su `propietario` al cliente y lo agrega a la lista del cliente. Si no existe, lanza `ValueError`.
- `Cliente`: nombre, saldo y lista privada de compras. `comprar` no puede gastar más que el saldo.
- `Tienda` no puede vender a crédito: verifica saldo antes de retirar el producto.
- La demo muestra el stock antes y después, y qué pasa al borrar la tienda.

**Entrada esperada.**
Tienda `"El Caldero"` con tres productos y un cliente con 100 de oro. Compra una poción de 40.

**Salida esperada.**
```text
Stock inicial: 3 productos
Venta: Poción de vida a Ana por 40 de oro.
Stock restante: 2 productos
Ana posee: Poción de vida (propietario: Ana)
Se elimina la tienda...
Producto comprado por Ana sigue vivo: Poción de vida
Productos del stock liberados con la tienda.
```

**Criterios de evaluación.**
- [ ] `Tienda` crea sus productos internamente (composición).
- [ ] `Cliente` conserva el producto comprado tras borrar la tienda (agregación).
- [ ] La venta cambia el propietario y no duplica el objeto.
- [ ] Se valida saldo insuficiente y producto inexistente.
- [ ] Ninguna lista interna se muta desde fuera de su clase.

---

## Nivel 3 — Reto: Ciclo de vida de una partida

**Enunciado.** Modela una partida por turnos con tres clases: `Partida`, `Turno` y `Personaje`. La partida **compone** sus turnos (los crea ella misma y mueren con ella) y **agrega** a los personajes que participan (existen antes y sobreviven al final de la partida). Demuestra el ciclo de vida con contadores de objetos vivos.

**Requisitos.**
- `Personaje`: nombre, nivel y método `actuar()` que devuelva una acción simple.
- `Turno`: número, personaje y acción. Solo lo crea la partida.
- `Partida`: nombre, lista privada de personajes, lista privada de turnos, estado (`en curso` / `finalizada`).
- `inscribir(personaje)` valida duplicados y un máximo de 4 participantes.
- `jugar_turno()` crea un `Turno` con el siguiente personaje en rotación y guarda su acción. No permite jugar si la partida está finalizada.
- `finalizar()` cambia el estado y no permite doble cierre.
- `resumen()` muestra nombre, estado, participantes y cantidad de turnos.
- Usa `weakref.finalize` para contar `Turno.vivos` y `Personaje.vivos`.
- Demo: crea 2 personajes, juega 3 turnos, borra la partida y muestra que los turnos murieron pero los personajes no.

**Entrada esperada.**
Sin `input()`. Personajes `"Kael"` (nivel 7) y `"Runa"` (nivel 5).

**Salida esperada.**
```text
Partida "Copa de Otoño" — en curso
Participantes: Kael, Runa
Turnos jugados: 3
Turnos vivos: 3
Se elimina la partida...
Turnos vivos: 0
Personajes vivos: 2
Kael sigue disponible.
```

**Criterios de evaluación.**
- [ ] Los turnos se crean únicamente dentro de `Partida.jugar_turno()`.
- [ ] Borrar la partida elimina los turnos y conserva los personajes.
- [ ] Se valida inscripción duplicada, cupo máximo y partida finalizada.
- [ ] El estado de la partida no permite doble `finalizar()`.
- [ ] Los contadores usan `weakref.finalize` y se explica su función en un comentario.
- [ ] El script ejecuta con `python3` y no usa librerías externas.

---

## Criterios generales de entrega

- [ ] Los tres archivos ejecutan sin errores con `python3`.
- [ ] Cada clase documenta en su docstring si **posee** o **referencia** sus partes.
- [ ] Las listas internas son privadas; la lectura se hace con tuplas o textos.
- [ ] Las validaciones usan `ValueError`, nunca `assert`.
- [ ] Se incluye un diagrama UML con rombo hueco o relleno según corresponda.
