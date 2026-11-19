# Semana 02 — Metodologías y paradigmas

> Programar es elegir una forma de pensar el problema; la POO es una de ellas, no la única.

## Objetivos de aprendizaje

- Distinguir los paradigmas **procedural**, **funcional** y **orientado a objetos**.
- Resolver el mismo problema con funciones y con clases.
- Leer y dibujar un UML básico con clases y relaciones.
- Describir el ciclo de desarrollo y las metodologías ágiles.
- Usar Git a diario: ramas, commits e issues.
- Explicar la evaluación por proyectos P1, P2 y P3.

## ¿Por qué importa?

Dos equipos reciben el mismo enunciado —«un combate por turnos»— y producen programas muy distintos. Uno llena una función de cien líneas con condicionales; el otro reparte responsabilidades entre personajes, armas y una arena. La diferencia se nota el lunes, cuando hay que agregar un enemigo nuevo o corregir un daño mal calculado.

Un **paradigma** es una manera de organizar el pensamiento y el código. No es una religión ni una marca de lenguaje. Python permite escribir procedural, funcional y orientado a objetos en el mismo archivo. Saber elegir te evita dos extremos: convertir todo en clases innecesarias o dejar crecer un script que nadie quiere tocar.

La metodología responde a otra pregunta: cómo se construye en equipo y cómo se sabe si va bien. Todo proyecto tiene alcance, fechas, revisión y ajuste; esta semana conecta esas ideas con Git, GitHub y el EVA/LMS.

## Concepto central

### Imperativo, procedural y funcional

El **imperativo** describe el programa como una secuencia de instrucciones que cambian el estado; el **procedural** lo organiza en funciones. Es directo, pero el estado se dispersa cuando la vida, el turno y el inventario viven en variables que muchas funciones modifican.

```python
def calcular_dano(ataque: int, defensa: int) -> int:
    return max(1, ataque - defensa)
```

El **funcional** transforma datos sin mutar los originales. En Python no es puro, pero sus funciones pequeñas y sin efectos secundarios sirven para filtrar inventarios o calcular totales.

```python
enemigos = [("Slime", 30), ("Gólem", 120), ("Murciélago", 45)]
fuertes = [nombre for nombre, hp in enemigos if hp >= 50]
```

### Orientado a objetos

Agrupa estado y comportamiento en objetos y define contratos con clases. No preguntas «¿qué funciones necesito?» sino «¿qué entidades existen y qué saben hacer?».

```python
class Personaje:
    def __init__(self, nombre: str, hp: int, ataque: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque

    def atacar(self, objetivo: "Personaje") -> None:
        objetivo.hp = max(0, objetivo.hp - self.ataque)
```

La ventaja es la **cohesión**: las reglas del personaje viven con sus datos. Si cambia la fórmula de daño, hay un solo lugar donde mirar.

### El mismo problema, dos formas

| Aspecto | Procedural | Orientado a objetos |
|---|---|---|
| Unidad principal | Función | Objeto y clase |
| Datos | Diccionarios y variables sueltas | Atributos del objeto |
| Comportamiento | Funciones que reciben datos | Métodos del objeto |
| Cambio típico | Más `if` en varios lugares | Nuevo método o subclase |
| Validación | Repetida en cada función | Concentrada en el constructor |
| Riesgo | Estado global difícil de rastrear | Jerarquías innecesarias |

No hay ganador universal: un cálculo de IVA no necesita una clase, pero un RPG con héroes e ítems sí se beneficia. La pregunta es: **¿hay entidades con estado y reglas propias?**

### UML básico

**UML** es una notación para describir sistemas antes de programarlos. Para este curso basta el **diagrama de clases**, donde cada caja tiene tres compartimentos:

```text
┌─────────────────────────────┐
│          Personaje          │
├─────────────────────────────┤
│ - nombre: str               │
│ - hp: int                   │
│ - ataque: int               │
├─────────────────────────────┤
│ + presentarse(): str        │
│ + atacar(objetivo): None    │
│ + esta_vivo(): bool         │
└─────────────────────────────┘
```

- `+` público, `-` privado y `#` protegido.
- Atributos como `nombre: tipo`; métodos como `nombre(parámetros): retorno`.
- **Asociación:** línea simple entre clases que colaboran.
- **Herencia:** flecha con triángulo hueco hacia la clase base.
- **Composición:** rombo relleno en el extremo del todo; la parte no existe sin él.

Un buen diagrama cabe en una página y responde qué clases hay, qué guardan, quién conoce a quién y qué operaciones son públicas.

### Ciclo y metodologías

Un proyecto pasa por análisis, diseño, implementación, pruebas, despliegue y mantenimiento. El modelo en **cascada** avanza fase por fase y asume requisitos estables; en la práctica cambian. Por eso se usan **metodologías iterativas**: construir una versión pequeña, revisarla y mejorar.

Las prácticas **ágiles** priorizan entregas cortas, un *backlog* ordenado, revisión con quien usa el software y ajuste con evidencia. **Scrum** trabaja en *sprints*; **Kanban** visualiza el flujo en columnas. Para el curso, un tablero simple y una reunión semanal bastan.

### Git como herramienta de trabajo

Git permite experimentar sin miedo, volver a una versión que funcionaba y trabajar en paralelo.

```bash
git switch -c feature/menu-combate
git add menu.py
git commit -m "Agrega menú de selección de personaje"
git switch main
git merge feature/menu-combate
```

Una rama por funcionalidad, commits pequeños en imperativo, `git status` antes de confirmar y nunca versionar `.venv/`, `__pycache__/` ni datos personales.

### Cómo se evalúa el curso

La evaluación es **100 % por proyectos**, sin exámenes escritos:

| Proyecto | Semana | Modalidad | Peso | Producto |
|---|---|---|---|---|
| P1 | 5 | Individual | 25 % | Creador de personajes RPG por consola |
| P2 | 11 | Equipos de 2–3 | 30 % | Arcade de combate por turnos |
| P3 | 15 | Equipos de 2–3 | 45 % | Arcade con interfaz gráfica |

Cada proyecto tiene dos criterios que pesan 50/50. Se evalúa ejecución, validaciones, historial y sustentación individual. Un proyecto que no ejecuta obtiene máximo 3.0; una copia, 0.

:::warning
No dejes el proyecto para el último fin de semana. La clase `Personaje` de hoy será la base del P1, y el combate de esta semana reaparecerá en el P2.
:::

## Código paso a paso

El ejemplo `paradigmas.py` resuelve el mismo combate de dos maneras. Primero con funciones y diccionarios; después con una clase. La salida debe ser equivalente, para que compares la estructura y no el resultado.

### Versión procedural

```python
def crear_personaje(nombre: str, hp: int, ataque: int) -> dict[str, object]:
    return {"nombre": nombre, "hp": hp, "ataque": ataque}


def atacar(atacante: dict[str, object], objetivo: dict[str, object]) -> None:
    dano = int(atacante["ataque"])
    objetivo["hp"] = max(0, int(objetivo["hp"]) - dano)
    print(f"{atacante['nombre']} ataca a {objetivo['nombre']} y causa {dano} de daño.")
```

Los datos viajan como diccionarios. Cualquier función puede cambiar cualquier clave; el tipado se vuelve difuso y las reglas quedan repartidas.

### Versión orientada a objetos

```python
class Personaje:
    def __init__(self, nombre: str, hp: int, ataque: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque

    def atacar(self, objetivo: "Personaje") -> None:
        dano = self.ataque
        objetivo.hp = max(0, objetivo.hp - dano)
        print(f"{self.nombre} ataca a {objetivo.nombre} y causa {dano} de daño.")
```

Ahora el ataque pertenece al personaje y la vida del objetivo es un atributo con nombre. La llamada `kaede.atacar(rook)` se lee como la regla del juego.

### Ejecutar y comparar

```bash
cd ejemplo-guiado
python3 paradigmas.py
```

El script imprime dos bloques, `PROCEDURAL` y `POO`, y ambos terminan con el mismo estado. La diferencia está en dónde vive la responsabilidad.

## Diagrama / modelo (si aplica)

```text
                 ┌──────────────────────────┐
                 │        Personaje         │
                 ├──────────────────────────┤
                 │ - nombre: str            │
                 │ - hp: int                │
                 │ - ataque: int            │
                 ├──────────────────────────┤
                 │ + atacar(objetivo): None │
                 │ + presentarse(): str     │
                 │ + esta_vivo(): bool      │
                 └────────────┬─────────────┘
                              │
                              │ asociación
                              ▼
                 ┌──────────────────────────┐
                 │         Equipo           │
                 ├──────────────────────────┤
                 │ - nombre: str            │
                 │ - miembros: list         │
                 ├──────────────────────────┤
                 │ + agregar(p): None       │
                 │ + vivos(): list          │
                 └──────────────────────────┘
```

En el diagrama, `Equipo` conoce a varios `Personaje`. La asociación no implica propiedad: si un personaje sale del equipo, el objeto puede seguir existiendo. Esa distinción importará al estudiar composición.

## Errores comunes

| Error | Qué revela | Cómo corregirlo |
|---|---|---|
| Crear una clase para cada cosa, incluso para sumar dos números | Abstracción innecesaria | Usa funciones si no hay estado ni reglas propias |
| Usar diccionarios para todo y llamarlo POO | Datos sin comportamiento | Pregunta qué operaciones pertenecen a la entidad |
| UML con cada método privado y cada variable temporal | Exceso de detalle | Modela solo lo necesario para comunicar |
| `git add .` sin revisar | Se suben archivos temporales o secretos | Revisa `git status` y usa `.gitignore` |
| Trabajar semanas sin commit y subir todo al final | No hay historial ni respaldo | Commits pequeños por avance |
| Copiar una solución de otro equipo | Riesgo académico y nulo aprendizaje | Sustenta tu código; la copia vale 0 |

:::error
No compares paradigmas contando líneas. Compara cohesión, legibilidad y facilidad para cambiar una regla.
:::

## Buenas prácticas

- **Modela antes de codificar.** Cinco minutos de UML ahorran una hora de refactorización.
- **Empieza por el caso más simple.** Un combate de dos personajes antes de una arena.
- **Nombra con el dominio.** `atacar`, `curar`, `equipo`; evita `dato1` o `procesar`.
- **Una responsabilidad por clase.** `Personaje` no imprime menús ni guarda archivos.
- **Prueba la salida esperada**, no solo que el programa «corra».
- **Documenta las decisiones** en el README, no en un comentario por línea.
- **Trabaja en ramas pequeñas** y vuelve a `main` solo cuando el código ejecute.

## Checklist de la semana

- [ ] Defino paradigma y nombro tres con un ejemplo.
- [ ] Expliqué una diferencia concreta entre procedural y POO.
- [ ] Ejecuté `paradigmas.py` y comparé las dos salidas.
- [ ] Dibujé un UML con al menos dos clases y una relación.
- [ ] Identifico las fases del ciclo y una práctica ágil.
- [ ] Usé una rama y un commit con mensaje claro.
- [ ] Entiendo los pesos y requisitos de P1, P2 y P3.

## Resumen

Un paradigma organiza el código; una metodología organiza el trabajo. El procedural piensa en funciones y pasos; el funcional, en transformaciones sin estado mutable; la POO, en entidades con datos y comportamiento. Python permite mezclarlos y la elección depende de la forma del problema.

UML da un lenguaje para discutir el diseño antes de codificar. El ciclo de desarrollo y las prácticas ágiles recuerdan que el software se construye por incrementos y se corrige con evidencia. Git registra el proceso y lo hace recuperable.

La evaluación refleja esa filosofía: tres proyectos con pesos 25/30/45, individuales y en equipo, con sustentación.

## Siguiente paso

La próxima semana entrarás en la sintaxis de la POO: clases, objetos, atributos de instancia y de clase, y `__init__` con criterio. Trae un diagrama sencillo de tu personaje y el repositorio limpio.
