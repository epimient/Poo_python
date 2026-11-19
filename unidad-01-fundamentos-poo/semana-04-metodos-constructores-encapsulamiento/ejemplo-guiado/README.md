# Ejemplo guiado — Semana 04

## Qué construye

Dos scripts independientes que aplican métodos, constructores y encapsulamiento:

- `combate_basico.py`: clase `Personaje` con `hp` validado entre `0` y `hp_max`, ataque, defensa, `recibir_danio`, `curar`, fábrica `desde_ficha` con `@classmethod` y cálculo `calcular_danio` con `@staticmethod`. El demo simula un combate por turnos y muestra los errores de las operaciones inválidas.
- `cuenta_bancaria.py`: clase `CuentaBancaria` con saldo protegido, `depositar`, `retirar`, historial de solo lectura, fábrica `desde_registro` y formato de dinero con `@staticmethod`. El demo ejecuta operaciones válidas, intenta romper las reglas y lista el historial.

## Cómo ejecutarlos

```bash
cd ejemplo-guiado
python3 combate_basico.py
python3 cuenta_bancaria.py
```

Ambos usan datos fijos, no piden entrada y no requieren dependencias externas.

## Salida esperada de `combate_basico.py`

```text
=== Combate básico (Semana 04) ===
Combatientes: Aria (90/90 hp, en pie) vs. Brom (120/120 hp, en pie)

-- Ronda 1 --
Aria golpea a Brom: -12 hp -> Brom (108/120 hp, en pie)
Brom golpea a Aria: -11 hp -> Aria (79/90 hp, en pie)

...

-- Ronda 10 --
Aria golpea a Brom: -12 hp -> Brom (0/120 hp, derrotado)

-- Resultado --
Ganador: Aria

-- Validaciones --
hp = -5: El hp debe estar entre 0 y 90.
hp = 999: El hp debe estar entre 0 y 90.
hp = 'mucho': El hp debe ser un número entero.
curar(0): La curación debe ser mayor que cero.
curar(-3): La curación debe ser mayor que cero.
ficha inválida: La ficha debe tener 4 campos: nombre,hp_max,ataque,defensa.

-- Representaciones --
str(aria): Aria (6/90 hp, en pie)
repr(aria): Personaje(nombre='Aria', hp=6, hp_max=90, ataque=18, defensa=4)
```

El combate dura 10 rondas: Aria ataca primero, Brom responde y en la ronda 3 Aria usa una poción de 15 hp. Al final Aria gana con 6 hp.

## Salida esperada de `cuenta_bancaria.py`

```text
=== Cuenta bancaria (Semana 04) ===
Cuenta de Ada Lovelace: $250.00

-- Operaciones --
Depósito: +$120.50
Saldo: $370.50
Retiro: -$80.00
Saldo: $290.50

-- Validaciones --
retirar(10000): Saldo insuficiente: intentas retirar $10,000.00 y tienes $290.50.
depositar(0): El monto debe ser mayor que cero.
depositar(-20): El monto debe ser mayor que cero.
depositar('50'): El monto debe ser un número.
titular vacío: El titular no puede estar vacío.
saldo negativo: El saldo inicial no puede ser negativo.

-- Historial --
  Apertura: +$250.00 | saldo $250.00
  Depósito: +$120.50 | saldo $370.50
  Retiro: -$80.00 | saldo $290.50
Movimientos: 3

-- Fábrica desde registro --
Cuenta de Grace Hopper: $900.25
repr: CuentaBancaria(titular='Grace Hopper', saldo=900.25)
Cuentas creadas: 2
Nota: las construcciones inválidas no incrementan el contador.
```

## Puntos clave

1. **El estado real es privado por convención.** `_hp` y `_saldo` guardan el dato; `hp` y `saldo` son propiedades de lectura que aplican las reglas. Un setter escribe en `_hp`, nunca en `hp`, para no recursar.
2. **Validar antes de modificar.** `recibir_danio` calcula `max(0, ...)` y `retirar` comprueba el saldo antes de restar. Si la operación no es válida, se lanza `ValueError` y el objeto queda intacto.
3. **Cada método devuelve algo útil.** `atacar` devuelve el daño aplicado, `curar` la vida recuperada, `retirar` el monto entregado. El demo imprime; la clase no.
4. **Las fábricas leen otros formatos.** `Personaje.desde_ficha("Brom, 120, 15, 6")` y `CuentaBancaria.desde_registro("Grace Hopper; 900.25")` usan `@classmethod` y `cls(...)`.
5. **`__str__` y `__repr__` no son lo mismo.** `str(aria)` es legible para el jugador; `repr(aria)` muestra los datos necesarios para depurar. La cuenta expone `historial` como tupla para que nadie altere la lista interna.

## Para experimentar

- Cambia el ataque de Aria a `30` y observa en cuántas rondas termina el combate.
- Intenta `aria.hp = 0` y luego `aria.atacar(brom)`: el método rechaza atacar estando derrotado.
- Deposita `0.005` y explica por qué el redondeo a dos decimales es importante en dinero.
- Añade una fábrica `CuentaBancaria.con_bono(titular, bono)` que reutilice `cls(...)`.
