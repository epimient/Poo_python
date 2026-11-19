# Ejercicios — Semana 04

## Nivel 1 — Básico: Personaje con estado consistente

**Enunciado.**
Crea una clase `Personaje` en la que la vida nunca pueda salir del intervalo `0..hp_max`. Usa un atributo interno `_hp`, una propiedad `hp` con setter validado y los métodos `recibir_danio` y `curar`. El programa debe mostrar el estado antes y después de varias operaciones, y capturar los errores de las operaciones inválidas.

**Requisitos.**
- `__init__(self, nombre: str, hp_max: int = 100)` debe validar que el nombre no esté vacío, que `hp_max` sea mayor que cero y que el hp inicial sea `hp_max`.
- La propiedad `hp` solo acepta enteros entre `0` y `hp_max`; fuera de rango lanza `ValueError`, y con un tipo incorrecto lanza `TypeError`.
- `recibir_danio(cantidad)` resta sin bajar de `0` y devuelve el daño real aplicado.
- `curar(cantidad)` suma sin superar `hp_max` y devuelve la vida real recuperada. Rechaza cantidades menores o iguales a cero con `ValueError`.
- `__str__` devuelve algo como `Aria (55/80 hp, en pie)` y `__repr__` algo como `Personaje(nombre='Aria', hp=55, hp_max=80)`.
- El demo captura tres errores distintos y continúa sin romperse.

**Entrada esperada.**
```python
aria = Personaje("Aria", hp_max=80)
aria.recibir_danio(25)
aria.curar(100)          # se limita a hp_max
aria.hp = -10            # ValueError
aria.recibir_danio(-5)   # ValueError
aria.hp = "mucho"        # TypeError
```

**Salida esperada.**
```text
Inicio: Aria (80/80 hp, en pie)
Daño aplicado: 25
Estado: Aria (55/80 hp, en pie)
Curación aplicada: 25
Estado: Aria (80/80 hp, en pie)

Error de rango: El hp debe estar entre 0 y 80.
Error de daño: El daño no puede ser negativo.
Error de tipo: El hp debe ser un número entero.

str: Aria (80/80 hp, en pie)
repr: Personaje(nombre='Aria', hp=80, hp_max=80)
```

**Criterios de evaluación.**
- [ ] La clase no expone `hp` como atributo público escribible sin validación.
- [ ] El setter usa `self._hp = valor` y no provoca recursión.
- [ ] Las operaciones devuelven el cambio real, no el valor solicitado.
- [ ] Los tres errores se capturan y se informan con mensajes claros.
- [ ] `__str__` y `__repr__` devuelven texto y se diferencian.
- [ ] El script se ejecuta completo con `python3`.

---

## Nivel 2 — Intermedio: Cuenta bancaria con retiros y transferencias

**Enunciado.**
Implementa una clase `CuentaBancaria` con saldo protegido, historial de movimientos y operaciones de depósito, retiro y transferencia. El saldo nunca puede quedar negativo. Cada operación válida debe registrarse; cada operación inválida debe lanzar `ValueError` o `TypeError` sin alterar el estado.

**Requisitos.**
- `__init__(self, titular: str, saldo_inicial: float = 0.0)` valida el nombre y el saldo. Rechaza saldo negativo y valores no finitos.
- `depositar(monto)` y `retirar(monto)` validan `monto > 0` y redondean a dos decimales con `round`.
- `retirar` lanza `ValueError` si el monto supera el saldo; `transferir(monto, destino)` reutiliza `retirar` y `depositar`, y rechaza transferir a la misma cuenta.
- `saldo` es una propiedad de solo lectura, sin setter.
- `historial` devuelve una tupla con los movimientos. Nadie debe poder hacer `cuenta.historial.append(...)`.
- Añade `desde_registro(linea)` como `@classmethod` para el formato `"Titular;saldo"` y `formatear_monto(monto)` como `@staticmethod`.
- El demo debe incluir al menos dos errores capturados y mostrar el historial final de ambas cuentas.

**Entrada esperada.**
```python
ana = CuentaBancaria("Ana Torres", 500.0)
luis = CuentaBancaria.desde_registro("Luis Prado; 50")
ana.depositar(250.75)
ana.retirar(120.25)
ana.transferir(100.0, luis)
ana.retirar(10_000)     # ValueError
ana.transferir(5, ana)  # ValueError
```

**Salida esperada.**
```text
Cuenta de Ana Torres: $500.00
Depósito: +$250.75 | saldo $750.75
Retiro: -$120.25 | saldo $630.50
Transferencia a Luis Prado: -$100.00
Saldo de Ana: $530.50
Saldo de Luis: $150.00

Error: Saldo insuficiente: intentas retirar $10,000.00 y tienes $530.50.
Error: No puedes transferirte dinero a ti mismo.

Historial de Ana Torres
  Apertura: +$500.00 | saldo $500.00
  Depósito: +$250.75 | saldo $750.75
  Retiro: -$120.25 | saldo $630.50
  Transferencia a Luis Prado: -$100.00 | saldo $530.50
Historial de Luis Prado
  Apertura: +$50.00 | saldo $50.00
  Transferencia de Ana Torres: +$100.00 | saldo $150.00

Transferencia recibida: +$100.00
Cuentas creadas: 2
```

**Criterios de evaluación.**
- [ ] El saldo solo cambia mediante operaciones validadas.
- [ ] Una operación fallida deja el saldo y el historial exactamente igual.
- [ ] `transferir` no duplica lógica de validación: reutiliza los métodos existentes.
- [ ] El historial es inmutable desde fuera.
- [ ] La fábrica y el formateador usan `@classmethod` y `@staticmethod` correctamente.
- [ ] Los montos se muestran con dos decimales y separador de miles.

---

## Nivel 3 — Reto: Combate con validaciones y pociones

**Enunciado.**
Construye un combate por turnos entre dos personajes. Cada personaje tiene vida validada, ataque, defensa y un número limitado de pociones. El combate debe rechazar acciones imposibles: atacar estando derrotado, atacar a un rival ya derrotado, curarse sin pociones o curarse estando al máximo. Al final, muestra el ganador y un resumen del combate.

**Requisitos.**
- Clase `Personaje` con `_hp`, propiedad `hp` validada, propiedad `vivo`, `atacar`, `recibir_danio`, `curar` y `usar_pocion`.
- `atacar(objetivo)` lanza `ValueError` si el atacante o el objetivo están derrotados y devuelve el daño aplicado.
- `usar_pocion()` consume una poción y cura 25 hp sin superar `hp_max`; si no quedan, lanza `ValueError`.
- Fábrica `desde_ficha(ficha)` con formato `"Nombre,hp_max,ataque,defensa,pociones"` y `@classmethod`. Valida que tenga cinco campos.
- `calcular_danio(ataque, defensa)` como `@staticmethod`, con un mínimo de 1.
- Atributo de clase `total_combates` que se incrementa al iniciar un combate; método de clase `registrar_combate()` si lo necesitas.
- El combate debe usar un bucle `while` con límite de rondas y detenerse cuando alguien llega a 0 hp.
- Define `__str__` y `__repr__`, y captura al menos tres errores al final del demo.

**Entrada esperada.**
```python
aria = Personaje("Aria", hp_max=100, ataque=20, defensa=5, pociones=2)
brom = Personaje.desde_ficha("Brom, 90, 18, 8, 1")

# Aria ataca primero en cada ronda; en la ronda 3 usa una poción.
# El combate termina cuando Brom llega a 0 hp.
```

**Salida esperada (resumida).**
```text
Combate 1: Aria (100/100 hp, 2 pociones) vs. Brom (90/90 hp, 1 poción)

Ronda 1: Aria causa 12. Brom queda en 78/90.
Ronda 1: Brom causa 13. Aria queda en 87/100.
Ronda 2: Aria causa 12. Brom queda en 66/90.
Ronda 2: Brom causa 13. Aria queda en 74/100.
Ronda 3: Aria causa 12. Brom queda en 54/90.
Ronda 3: Brom causa 13. Aria queda en 61/100.
Ronda 3: Aria usa una poción y recupera 25 hp. Aria queda en 86/100.
...
Ronda 8: Aria causa 12. Brom queda en 0/90.

Ganadora: Aria (34/100 hp, 1 poción)

Error: Brom está derrotado y no puede atacar.
Error: Aria no tiene pociones.
Error: La ficha debe tener 5 campos.
```

**Criterios de evaluación.**
- [ ] El hp nunca sale de `[0, hp_max]`, ni siquiera al curar o recibir daño excesivo.
- [ ] `usar_pocion` descuenta la poción solo cuando la curación es válida.
- [ ] Atacar a un derrotado y atacar estando derrotado lanzan `ValueError`.
- [ ] La fábrica valida el número de campos y convierte los valores numéricos.
- [ ] El bucle termina por victoria o por límite de rondas, sin bucles infinitos.
- [ ] El resumen final muestra ganador, vida restante y pociones.
- [ ] El script corre completo con `python3` y los errores se capturan sin ocultar el estado.
