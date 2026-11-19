# Ejercicios — Semana 09

## Nivel 1 — Básico: Contrato de habilidad

**Enunciado.** Crea `habilidades_combate.py` con una clase abstracta `Habilidad` y dos habilidades concretas: `BolaDeFuego` y `Curacion`. La base declara el contrato; cada habilidad decide qué hace al ejecutarse.

**Requisitos.**
- `Habilidad(ABC)` tiene `nombre`, `costo_mana` y el método abstracto `ejecutar(self) -> str`.
- `BolaDeFuego` devuelve un texto con el daño causado y gasta maná.
- `Curacion` devuelve un texto con la vida recuperada y gasta maná.
- Ambas subclases llaman a `super().__init__()`.
- El script intenta crear `Habilidad("Genérica", 0)` dentro de `try/except TypeError` e imprime el mensaje.
- Recorre una `list[Habilidad]` y ejecuta cada una sin preguntar por su clase.
- Valida que `costo_mana >= 0` en el constructor de la base y lanza `ValueError` si no se cumple.

**Entrada esperada.**
Ninguna. Datos de ejemplo: una bola de fuego y una curación.

**Salida esperada.**
```text
No se puede crear una Habilidad genérica:
  Can't instantiate abstract class Habilidad without an implementation for abstract method 'ejecutar'

Bola de fuego: 18 de daño (maná restante: 10)
Curación: 25 PV recuperados (maná restante: 15)
```

**Criterios de evaluación.**
- [ ] `Habilidad` hereda de `ABC` y `ejecutar()` está decorado con `@abstractmethod`.
- [ ] Las dos subclases implementan `ejecutar()`.
- [ ] La instanciación de la base lanza `TypeError` y se captura.
- [ ] La validación de `costo_mana` lanza `ValueError`.
- [ ] El bucle usa la clase base como tipo de la lista.

---

## Nivel 2 — Intermedio: Protocol de curación

**Enunciado.** Crea `curacion.py` con un `Protocol` llamado `Curable` y una función `curar_equipo(objetivos: list[Curable], cantidad: int) -> int`. Debes poder curar objetos de clases que no comparten una base común.

**Requisitos.**
- `Curable` declara `nombre: str`, `vida: int`, `vida_maxima: int` y `curar(self, cantidad: int) -> int`.
- Marca el protocolo con `@runtime_checkable`.
- Implementa dos clases independientes: `Caballero` y `Lobo`. Ninguna hereda de `Curable`.
- `curar()` devuelve la cantidad realmente recuperada, sin superar `vida_maxima`.
- `curar_equipo()` recorre la lista y acumula el total curado.
- Agrega una clase `Roca` sin `curar()` y demuestra con `isinstance()` que no cumple el protocolo.
- La función debe rechazar objetos no curables sin lanzar una excepción no controlada; imprime un aviso y continúa.
- Valida que `cantidad > 0`; si no, lanza `ValueError`.

**Entrada esperada.**
Ninguna. Datos: un caballero con 40/120 PV, un lobo con 10/30 PV y una roca.

**Salida esperada.**
```text
Caballero recupera 25 PV (65/120)
Lobo recupera 20 PV (30/30)
Total curado: 45 PV

¿Roca es Curable? False
Roca no cumple el contrato de curación
```

**Criterios de evaluación.**
- [ ] `Curable` es un `Protocol` y no una clase base heredada.
- [ ] `runtime_checkable` permite usar `isinstance()`.
- [ ] Las dos clases comparten forma, no padre.
- [ ] La curación respeta el máximo de vida.
- [ ] La función maneja el objeto inválido sin romper el programa.
- [ ] Se valida la cantidad con `ValueError`.

---

## Nivel 3 — Reto: Jerarquía de armas

**Enunciado.** Diseña `armas.py` con una clase abstracta `Arma` y tres armas concretas: `Espada`, `Arco` y `Baston`. La base debe fijar un método plantilla `describir()` que use los pasos abstractos de cada arma.

**Requisitos.**
- `Arma(ABC)` tiene `nombre: str`, `precio: int` y dos métodos abstractos: `dano(self) -> int` y `tipo_dano(self) -> str`.
- `describir(self) -> str` es concreto y devuelve, en este orden: nombre, tipo de daño, daño y precio.
- `Espada` suma fuerza al daño base; `Arco` dispara dos flechas si tiene munición; `Baston` gasta maná para lanzar un hechizo.
- Cada subclase implementa `dano()` y `tipo_dano()` y llama a `super().__init__()`.
- Valida en la base que `precio > 0` y que `nombre` no esté vacío; lanza `ValueError` con un mensaje claro.
- Crea una `list[Arma]` y recorre con `describir()` sin preguntar por la clase.
- Intenta crear `Arma("Genérica", 10)` y captura el `TypeError`.
- Agrega una subclase `ArmaRota` que no implemente `tipo_dano()` y demuestra que tampoco se instancia.
- Comenta en 3–5 líneas por qué `describir()` no es abstracto y qué ventaja tiene el método plantilla.

**Entrada esperada.**
Ninguna. Datos: espada corta, arco élfico, bastón de hielo.

**Salida esperada.**
```text
Espada corta | físico | 16 de daño | 120 monedas
Arco élfico | perforante | 18 de daño | 200 monedas
Bastón de hielo | mágico | 21 de daño | 180 monedas

Arma genérica: no se puede instanciar
ArmaRota: falta implementar tipo_dano()
```

**Criterios de evaluación.**
- [ ] `Arma` no se puede instanciar.
- [ ] `describir()` está en la base y no se sobrescribe en las hijas.
- [ ] Los dos métodos abstractos se implementan en las tres armas.
- [ ] Las validaciones cubren precio y nombre con mensajes claros.
- [ ] `ArmaRota` demuestra el `TypeError` por contrato incompleto.
- [ ] El comentario final explica la diferencia entre método concreto y abstracto.
- [ ] El script ejecuta completo con `python3 armas.py`.
