# Refuerzo — Unidad 2: relaciones, herencia y polimorfismo

20 ejercicios cortos para practicar los conceptos de las semanas 6 a 10. Cada uno indica el enunciado y los requisitos mínimos. No se incluyen soluciones: la idea es que los resuelvas y los pruebes con `python3`.

## Relaciones entre clases

### 1. Ficha de personaje y arma

**Enunciado.** Modela un personaje que porta un arma. El personaje conoce su arma, pero el arma existe por separado y puede asignarse a otro personaje.

**Requisitos.**
- Crea `Arma` con nombre, daño y una descripción breve.
- Crea `Personaje` con nombre, HP y un atributo `arma` que pueda cambiarse.
- Agrega un método `equipar(arma)` que valide que el objeto recibido tiene nombre y daño.

### 2. Equipo y jugadores

**Enunciado.** Un equipo de videojuego tiene varios jugadores. Un jugador pertenece a un solo equipo a la vez.

**Requisitos.**
- Crea `Jugador` con alias y nivel, y `Equipo` con nombre y una lista de jugadores.
- Implementa `agregar(jugador)` y `promedio_nivel()`.
- Evita que el mismo jugador se agregue dos veces al equipo.

### 3. Tienda y cliente

**Enunciado.** Una tienda atiende clientes. El cliente tiene un monedero y la tienda vende objetos. Modela la relación sin que la tienda sea dueña del cliente.

**Requisitos.**
- Crea `Cliente` con nombre y saldo, y `Tienda` con inventario y método `vender(cliente, objeto)`.
- La venta debe descontar el precio del saldo y fallar con un mensaje claro si no alcanza.
- La tienda no debe crear clientes dentro de su constructor.

### 4. Banco y cuentas

**Enunciado.** Un banco tiene varias cuentas. Cada cuenta conoce a su titular. Representa la multiplicidad y permite consultar las cuentas de un cliente.

**Requisitos.**
- Crea `Titular` con documento y nombre, y `Cuenta` con número, saldo y titular.
- Crea `Banco` con una lista de cuentas y un método `cuentas_de(titular)`.
- Valida que el número de cuenta no se repita dentro del banco.

## Agregación y composición

### 5. Mochila y objetos

**Enunciado.** Una mochila contiene objetos que pueden existir fuera de ella. Si eliminas la mochila, los objetos siguen existiendo.

**Requisitos.**
- Crea `Objeto` con nombre y peso, y `Mochila` con capacidad máxima.
- Implementa `agregar()` y `peso_total()`; rechaza agregar si se supera la capacidad.
- Permite sacar un objeto y comprobar que sigue disponible fuera de la mochila.

### 6. Mazo y cartas

**Enunciado.** Un mazo está compuesto por cartas. Si el mazo se destruye, sus cartas también. Modela una composición real.

**Requisitos.**
- Crea `Carta` con valor y palo, y `Mazo` que genere sus cartas internamente.
- Implementa `robar()` y `quedan()`.
- El exterior no debe poder modificar la lista interna de cartas.

### 7. Partida y tablero

**Enunciado.** Una partida contiene un tablero y un historial de movimientos. El tablero no se comparte entre partidas.

**Requisitos.**
- Crea `Tablero` con dimensiones y una matriz de celdas.
- Crea `Partida` que construya su propio tablero en el constructor.
- Implementa `registrar_movimiento()` y `historial()` sin exponer la lista original.

### 8. Factura y líneas

**Enunciado.** Una factura de la tienda del juego se compone de líneas de venta. Cada línea calcula su subtotal y la factura suma todo.

**Requisitos.**
- Crea `Linea` con objeto, cantidad y precio unitario.
- Crea `Factura` que reciba las líneas y calcule el total.
- Valida cantidades positivas y que la factura no quede vacía al emitirse.

## Herencia y sobrescritura

### 9. Personajes del juego

**Enunciado.** Crea una jerarquía `Personaje → Guerrero, Mago, Arquero`. Todos comparten nombre y HP; cada uno calcula su ataque de forma distinta.

**Requisitos.**
- La clase base debe tener un método `atacar()` que las subclases sobrescriban.
- Usa `super().__init__()` en las tres subclases.
- Agrega un método `estado()` en la base que no se duplique en las hijas.

### 10. Armas especializadas

**Enunciado.** Modela `Arma` con daño base y las subclases `Espada`, `Arco` y `Baston`. Cada una modifica el daño según su propia regla.

**Requisitos.**
- `Espada` suma fuerza, `Arco` aplica probabilidad de crítico y `Baston` suma poder mágico.
- Cada subclase sobrescribe `calcular_dano()` manteniendo la misma firma.
- Verifica que una lista de armas se pueda recorrer llamando `calcular_dano()` sin preguntar el tipo.

### 11. Mascotas que evolucionan

**Enunciado.** Una mascota puede evolucionar a una forma más fuerte. Modela `Mascota` y dos evoluciones que cambian el nombre y el poder de ataque.

**Requisitos.**
- La clase base define `atacar()` y `evolucionar()`.
- Cada evolución sobrescribe `atacar()` y reutiliza la lógica común con `super()`.
- Valida que una mascota no pueda evolucionar dos veces.

### 12. Cuentas bancarias

**Enunciado.** Un banco tiene cuentas de ahorro y cuentas corrientes. Ambas comparten saldo y titular, pero cobran comisiones distintas al retirar.

**Requisitos.**
- Crea `Cuenta` con `depositar()` y `retirar()`; la segunda debe validar fondos.
- `CuentaAhorro` cobra una comisión fija y `CuentaCorriente` cobra un porcentaje.
- Recorre una lista de cuentas y aplica el mismo retiro sin preguntar la clase.

## Clases abstractas y contratos

### 13. Habilidad con enfriamiento

**Enunciado.** Todas las habilidades de un personaje tienen nombre, coste y turnos de enfriamiento. Modela el contrato con una clase abstracta.

**Requisitos.**
- Crea `Habilidad(ABC)` con `usar()` abstracto y `disponible()` con lógica compartida.
- Implementa `BolaDeFuego`, `Curacion` y `GolpeHelado`.
- Comprueba que no se pueda instanciar `Habilidad` directamente.

### 14. Enemigo abstracto

**Enunciado.** Un bestiario comparte HP y recompensa, pero cada enemigo ataca distinto. Usa `ABC` para obligar el contrato.

**Requisitos.**
- `Enemigo(ABC)` declara `atacar()` y `describir()` como abstractos.
- Implementa `Slime`, `Goblin` y `Dragon` con HP y daños diferentes.
- Un método `enfrentar(enemigos)` debe recorrer la lista sin usar `isinstance`.

### 15. Contrato de curación con Protocol

**Enunciado.** Algunas clases del juego pueden curar, pero no comparten una jerarquía. Define el contrato con `Protocol` y úsalo en una función.

**Requisitos.**
- Crea `Curador(Protocol)` con `curar(cantidad: int) -> int`.
- Implementa `Pocion`, `Mago` y `Altar` sin heredar del protocolo.
- Escribe `aplicar_curacion(objeto: Curador, cantidad: int)` y pruébala con los tres.

## Polimorfismo

### 16. La lista de combatientes

**Enunciado.** Crea una lista con un guerrero, un mago y un arquero. Recórrela y llama `atacar()` en cada uno sin preguntar el tipo.

**Requisitos.**
- Los tres comparten una clase base abstracta con `atacar(objetivo)`.
- El bucle debe tener una sola línea de llamada al método.
- Agrega una cuarta clase y confirma que el bucle no cambia.

### 17. Inventario con dunders

**Enunciado.** Implementa un inventario que se comporte como un contenedor de Python y que sus objetos se puedan usar de forma polimórfica.

**Requisitos.**
- Implementa `__len__`, `__iter__`, `__contains__`, `__add__` y `__str__`.
- Crea objetos con `usar()` distinto: arma, poción y llave.
- Recorre el inventario llamando `usar()` y muestra el resultado.

### 18. Tipos de daño con singledispatch

**Enunciado.** Un ataque puede producir daño físico, mágico o verdadero. Cada tipo reduce el daño de forma distinta según la defensa del objetivo.

**Requisitos.**
- Crea las clases `DanoFisico`, `DanoMagico` y `DanoVerdadero`.
- Registra una función con `singledispatch` para cada tipo.
- Incluye un caso no soportado que lance `TypeError` con un mensaje claro.

### 19. Procesar pagos sin herencia

**Enunciado.** La tienda acepta pagos con tarjeta, efectivo y monedas del juego. Los tres saben `pagar(monto)`, pero no comparten clase base.

**Requisitos.**
- Implementa las tres clases con el método `pagar(monto) -> bool`.
- Escribe `cobrar(metodo, monto)` usando solo el método común.
- Prueba un objeto sin `pagar()` y explica qué excepción ocurre.

### 20. Refactor de `isinstance`

**Enunciado.** Recibes un bucle con una cadena de `isinstance` para calcular recompensas de tres tipos de enemigo. Refactorízalo para que el motor no conozca las clases.

**Requisitos.**
- Crea una clase base con `recompensa()` y una subclase por tipo de enemigo.
- Sustituye toda la cadena por una llamada polimórfica dentro del bucle.
- Demuestra que agregar un enemigo nuevo solo requiere una clase nueva.
