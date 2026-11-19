# Ejercicios formativos — Unidad 1

Veinte ejercicios cortos para reforzar clases, objetos, atributos, métodos, constructores y encapsulamiento. No tienen solución incluida: la idea es escribirlos, ejecutarlos y comparar el resultado con lo que esperabas.

## Clases y objetos

### 1. Ficha de personaje
Crea una clase `Personaje` con nombre, clase (guerrero, mago o arquero) y nivel.

**Requisitos.**
- Define la clase con un constructor que reciba los tres datos.
- Crea dos personajes distintos e imprime sus datos en una línea cada uno.
- Usa `PascalCase` para la clase y `snake_case` para los atributos.

### 2. Armas en una lista
Crea una clase `Arma` con nombre y daño. Guarda tres armas en una lista y recórrela.

**Requisitos.**
- La clase debe tener exactamente dos atributos.
- Imprime cada arma con su daño usando un bucle.
- Calcula e imprime el daño total de las tres.

### 3. ¿El mismo objeto?
Crea una clase `Ficha` con un solo atributo, `nombre`. Instancia dos objetos con el mismo nombre.

**Requisitos.**
- Imprime `ficha1 is ficha2`, `ficha1 == ficha2` y sus `id()`.
- Escribe un comentario explicando por qué los resultados son esos.
- Cambia el nombre de una ficha y comprueba que la otra no cambia.

### 4. Tienda de pociones
Crea una clase `Pocion` con nombre y precio, y una clase `Tienda` con nombre y una lista de pociones.

**Requisitos.**
- La tienda debe empezar con la lista vacía.
- Agrega tres pociones a la tienda desde el programa principal.
- Imprime el nombre de la tienda y cuántas pociones tiene.

## Atributos

### 5. Atributo de clase y de instancia
Crea una clase `Personaje` con el atributo de clase `vidas_maximas = 3` y el atributo de instancia `vidas`.

**Requisitos.**
- Crea dos personajes con vidas distintas.
- Imprime `vidas_maximas` desde la clase y desde cada objeto.
- Cambia `vidas_maximas` en uno de los objetos y explica qué pasa con el otro.

### 6. Mochilas independientes
Crea una clase `Mochila` cuyo atributo `objetos` sea una lista creada dentro del constructor.

**Requisitos.**
- Instancia dos mochilas y agrega un objeto solo a la primera.
- Imprime el contenido de ambas y comprueba que no se comparte.
- Escribe qué ocurriría si usaras `def __init__(self, objetos=[]):`.

### 7. Contador de partidas
Crea una clase `Partida` con un atributo de clase `total_partidas` que aumente cada vez que se crea una instancia.

**Requisitos.**
- Crea tres partidas y muestra el contador desde la clase.
- Muestra también el contador desde una instancia.
- Explica en un comentario por qué el contador no es un atributo de instancia.

### 8. Transacción bancaria
Crea una clase `Transaccion` con monto, tipo (`"deposito"` o `"retiro"`) y fecha como texto.

**Requisitos.**
- Crea dos transacciones con datos distintos.
- Imprime un resumen con formato `fecha · tipo · monto`.
- Guarda las transacciones en una lista y recórrela.

## Métodos

### 9. ¿Sigue vivo?
Agrega a una clase `Personaje` un método `esta_vivo()` que devuelva `True` si la vida es mayor que cero.

**Requisitos.**
- El método no debe imprimir nada: solo devolver un booleano.
- Prueba con vida `10`, con vida `0` y con vida negativa.
- Imprime el resultado de las tres pruebas.

### 10. Retiro de saldo
Crea una clase `Cuenta` con saldo inicial y un método `retirar(monto)` que descuente el monto y devuelva el saldo nuevo.

**Requisitos.**
- El método debe modificar el estado de la cuenta.
- Llama a `retirar` dos veces y muestra el saldo después de cada llamada.
- No agregues validaciones todavía: eso llega en el bloque de encapsulamiento.

### 11. Agregar al equipo
Crea una clase `Equipo` con nombre y una lista de miembros, y un método `agregar(personaje)`.

**Requisitos.**
- El método debe recibir un objeto, no un texto con el nombre.
- Agrega tres personajes y muestra cuántos miembros hay.
- Devuelve la cantidad de miembros después de agregar.

### 12. Un método que usa otro
Crea una clase `Combate` con los atributos `vida_actual` y `vida_maxima`.

**Requisitos.**
- Define `porcentaje_vida()` que devuelva un número entre 0 y 100.
- Define `estado()` que use `porcentaje_vida()` para devolver `"crítico"`, `"herido"` o `"estable"`.
- Prueba los tres estados con objetos distintos.

## Constructores

### 13. Valores por defecto
Crea una clase `Personaje` cuyo constructor reciba nombre, vida con valor por defecto `100` y nivel con valor por defecto `1`.

**Requisitos.**
- Instancia un personaje con solo el nombre.
- Instancia otro con los tres argumentos.
- Imprime ambos para comprobar los valores por defecto.

### 14. Constructor que valida
Crea una clase `Pocion` que reciba nombre y precio, y rechace precios menores o iguales a cero con `ValueError`.

**Requisitos.**
- La validación debe estar en el constructor, antes de guardar el precio.
- Prueba una poción válida y una inválida dentro de `try`/`except`.
- Muestra un mensaje claro cuando el precio sea inválido.

### 15. Lista sin compartir
Crea una clase `Equipo` que reciba nombre y una lista opcional de miembros.

**Requisitos.**
- Usa `None` como valor por defecto y crea la lista dentro del constructor.
- Instancia dos equipos sin miembros y agrega uno distinto a cada uno.
- Comprueba que las listas no se comparten.

### 16. Nivel calculado
Crea una clase `Partida` con los atributos `puntos` y `nivel`, donde el nivel se calcule en el constructor.

**Requisitos.**
- Define una regla simple: menos de 100 puntos es nivel 1, menos de 300 es nivel 2, el resto es nivel 3.
- El nivel no debe recibirse como parámetro.
- Crea tres partidas y muestra puntos y nivel de cada una.

## Encapsulamiento

### 17. Saldo protegido
Crea una clase `Cuenta` con saldo inicial y el atributo `_saldo`.

**Requisitos.**
- Expón el saldo con una propiedad de solo lectura.
- Implementa `depositar(monto)` y `retirar(monto)` con validación de montos positivos y saldo suficiente.
- Comprueba que `cuenta.saldo = 1000` no cambia el saldo real.

### 18. Vida con límites
Crea una clase `Personaje` con `_vida` y una propiedad `vida` cuyo setter limite el valor entre 0 y 100.

**Requisitos.**
- El setter debe rechazar o ajustar valores fuera de rango; elige una estrategia y documéntala.
- Implementa `recibir_danio(cantidad)` y `curar(cantidad)` usando la propiedad.
- Prueba con daño excesivo y con curación por encima del máximo.

### 19. Inventario de solo lectura
Crea una clase `Inventario` con `_objetos` y una propiedad `objetos` que devuelva una tupla.

**Requisitos.**
- Agrega objetos solo mediante un método `agregar`.
- Intenta modificar la tupla devuelta y observa el error.
- Explica por qué devolver una tupla protege mejor que devolver la lista interna.

### 20. PIN de cliente
Crea una clase `Cliente` con nombre y `_pin` de cuatro dígitos.

**Requisitos.**
- Expón el nombre con una propiedad de solo lectura.
- Implementa `verificar_pin(pin)` que devuelva `True` o `False`, sin imprimir el PIN.
- Valida en el constructor que el PIN tenga exactamente cuatro dígitos.
