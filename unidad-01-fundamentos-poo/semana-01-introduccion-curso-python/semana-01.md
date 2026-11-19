# Semana 01 — Introducción al curso y a Python

> Antes de escribir clases necesitas un lugar donde escribirlas: Python instalado, un editor configurado y un repositorio que guarde tu historia.

## Objetivos de aprendizaje

- Explicar con tus palabras qué es la programación orientada a objetos y diferenciar **objeto** de **clase**.
- Instalar y verificar Python 3.12 en Linux, Windows o macOS.
- Configurar Visual Studio Code y un entorno virtual (`venv`) para cada proyecto.
- Crear un repositorio en Git, publicarlo en GitHub y registrar cambios con commits claros.
- Identificar objetos en Python y escribir tu primera clase con atributos y métodos.
- Entregar actividades por el EVA/LMS y ejecutar tus scripts desde la terminal.

## ¿Por qué importa?

Un curso de programación no empieza con sintaxis: empieza con un entorno que no te haga perder tiempo. Si cada ejercicio depende de instalar algo distinto o de activar mal el entorno, vas a culpar al lenguaje de problemas de taller. Esta semana montas el taller y lo pruebas con un programa pequeño.

La POO responde a una pregunta de diseño. Imagina un RPG con héroes, enemigos, armas y tienda. Si todo vive en variables sueltas, cambiar el combate obliga a revisar diez archivos. Si cada personaje sabe su nombre, su vida y cómo atacar, el programa se parece al problema real. Esa es la promesa de la orientación a objetos: **modelar el software con piezas que tienen datos y comportamiento propio**.

Python es el lenguaje del curso y su modelo de objetos es directo: un entero, un texto y una lista ya son objetos. No necesitas una sintaxis nueva para descubrir qué es un objeto.

:::info
La mediación del curso es **Python 3.12 + Visual Studio Code + EVA/LMS + Git + repositorio de código**. Todo es gratuito y funciona en Linux, Windows y macOS.
:::

## Concepto central

### Objeto y clase

Un **objeto** tiene **estado** (datos) y **comportamiento** (acciones). Una **clase** es el molde que describe cómo serán los objetos de ese tipo.

La clase `Nave` describe nombre, escudo y potencia; cada nave concreta —la tuya, la del jefe— es un objeto creado a partir de ese molde.

| Concepto | En el videojuego | En Python |
|---|---|---|
| Clase | El plano de una nave | `class Nave:` |
| Objeto | Tu nave llamada *Halcon* | `mi_nave = Nave(...)` |
| Atributo | Escudo actual: 80 | `self.escudo` |
| Método | Disparar | `def disparar(self):` |
| Estado | Escudo 80, potencia 12 | Valores guardados en el objeto |

La clase existe una vez en el código; los objetos pueden ser muchos y cada uno tiene sus propios valores. Dos personajes comparten la definición de `atacar`, pero no comparten la vida.

### Por qué Python

Python es interpretado: escribes un `.py` y lo ejecutas, sin compilación manual. Su indentación obliga a escribir código legible y su biblioteca estándar cubre todo el curso, incluida Tkinter para la unidad gráfica. Además, deja ver el concepto sin la ceremonia de otros lenguajes; si más adelante cambias de herramienta, las ideas de clase, objeto, herencia y polimorfismo viajan contigo.

### Todo en Python es un objeto

Abre una terminal y prueba:

```python
>>> nombre = "Kaede"
>>> type(nombre)
<class 'str'>
>>> nombre.upper()
'KAEDE'
>>> type(42)
<class 'int'>
```

`nombre` es una instancia de `str` y `upper()` es un método de esa clase. Cuando escribes `nombre.upper()` envías un mensaje a un objeto, el mismo gesto que usarás con `kaede.atacar(enemigo)`.

### El entorno de trabajo

Necesitas cuatro piezas: **Python 3.12**, **VS Code** con la extensión de Python, un **repositorio Git** con copia en GitHub y una carpeta de proyecto con **entorno virtual**.

```bash
# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install python3 python3-venv python3-pip

# macOS con Homebrew
brew install python@3.12

# Windows: descarga Python 3.12 desde python.org
# y marca "Add python.exe to PATH" durante la instalación
```

Verifica siempre la versión:

```bash
python3 --version
# Python 3.12.x

# En Windows también puede ser:
py -3.12 --version
```

Si devuelve otra versión, revisa qué intérprete estás llamando; en Windows, `py -3.12` es más explícito.

### Visual Studio Code

Instala VS Code y la extensión **Python** de Microsoft. Elige el intérprete con `Ctrl+Shift+P` → *Python: Select Interpreter* → el `python` de tu entorno virtual. Esa selección permite ver errores, autocompletado y ejecución integrada.

### Entorno virtual

Un entorno virtual es una carpeta con su propio intérprete y paquetes. Evita que un proyecto rompa otro y permite reproducir el entorno en otro computador.

```bash
# Desde la carpeta del proyecto
python3 -m venv .venv

# Activar en Linux y macOS
source .venv/bin/activate

# Activar en Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Comprobar que estás dentro
which python        # Linux/macOS
where python        # Windows
python --version
```

El prompt muestra `(.venv)` cuando está activo. Para salir: `deactivate`. La carpeta `.venv/` nunca se sube a Git; se agrega a `.gitignore`.

### Git y GitHub

Git guarda versiones en tu computadora; GitHub aloja una copia remota y te permite entregar evidencias y mostrar tu portafolio.

```bash
# Configuración inicial (una sola vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"

# Crear el repositorio local
mkdir poo-personajes
cd poo-personajes
git init

# Primer archivo
printf '.venv/\n__pycache__/\n' > .gitignore
git add .
git commit -m "Configura repositorio inicial del curso"

# Publicar en GitHub (crea antes el repositorio vacío en la web)
git branch -M main
git remote add origin https://github.com/TU-USUARIO/poo-personajes.git
git push -u origin main
```

Un buen commit completa «este cambio…»: *agrega clase Personaje*, *corrige validación de hp*. Evita *cambios* o *final final*.

:::warning
No subas contraseñas, tokens, `.venv/` ni `__pycache__/`. Si ya los subiste, no basta con borrarlos en el siguiente commit: quedan en el historial. Avísale a tu docente y corrige el repositorio.
:::

## Código paso a paso

Vamos a construir `personaje.py`. El objetivo no es un sistema de combate completo, sino ver el ciclo mínimo de la POO: definir una clase, crear objetos, llamar métodos y observar cómo cambia el estado.

### Paso 1 — Definir la clase

```python
class Personaje:
    """Un personaje jugable con nombre, vida y poder de ataque."""

    def __init__(self, nombre: str, hp: int, ataque: int) -> None:
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque
```

`class` crea el molde. `__init__` es el constructor: se ejecuta automáticamente al crear un objeto. `self` es la referencia al objeto que se está construyendo; por eso `self.nombre` guarda un dato distinto en cada personaje.

### Paso 2 — Agregar comportamiento

```python
    def presentarse(self) -> str:
        return f"Soy {self.nombre} y tengo {self.hp} HP."

    def atacar(self, objetivo: "Personaje") -> None:
        dano = self.ataque
        objetivo.hp = max(0, objetivo.hp - dano)
        print(f"{self.nombre} ataca a {objetivo.nombre} y causa {dano} de daño.")
        print(f"{objetivo.nombre} queda con {objetivo.hp} HP.")

    def esta_vivo(self) -> bool:
        return self.hp > 0
```

Un método es una función que pertenece a la clase. `atacar` recibe otro objeto y modifica su estado. `max(0, ...)` evita que la vida quede negativa, una validación pequeña que ya es una regla del dominio.

### Paso 3 — Crear y usar objetos

```python
kaede = Personaje("Kaede", 120, 18)
rook = Personaje("Rook", 90, 24)
nima = Personaje("Nima", 100, 14)

for personaje in (kaede, rook, nima):
    print(personaje.presentarse())

kaede.atacar(rook)
rook.atacar(kaede)
```

Cada llamada a `Personaje(...)` crea un objeto independiente. `kaede.hp` y `rook.hp` son atributos distintos aunque compartan el mismo nombre en el código.

### Paso 4 — Ejecutar

```bash
cd ejemplo-guiado
python3 personaje.py
```

La salida muestra las presentaciones y luego el intercambio de ataques. Si ves los nombres y la vida actualizada, el entorno y el código funcionan.

## Diagrama / modelo (si aplica)

```text
        CLASE Personaje
        ─────────────────────────────
        nombre : str
        hp     : int
        ataque : int
        ─────────────────────────────
        presentarse() -> str
        atacar(objetivo) -> None
        esta_vivo() -> bool
                 ▲
                 │ crea instancias
     ┌───────────┼───────────┐
     │           │           │
  kaede       rook        nima
  hp=120      hp=90       hp=100
  ataque=18   ataque=24   ataque=14
```

La clase aparece una vez; los objetos, tres. Cada objeto tiene su propia copia de los atributos de instancia.

## Errores comunes

| Error | Qué significa | Cómo corregirlo |
|---|---|---|
| `python: command not found` | Python no está en el PATH | Prueba `python3 --version` o `py -3.12 --version` |
| `IndentationError` | Indentación inconsistente | Usa 4 espacios, nunca tabuladores |
| `NameError` | Clase usada antes de definirla | Define antes del bloque demo |
| `TypeError: Personaje() takes no arguments` | Falta `__init__` o no coincide la firma | Revisa el constructor y sus argumentos |
| `AttributeError` | Atributo mal escrito o ausente | Decláralo en `__init__` |
| El script no hace nada | Falta el bloque de ejecución | Agrega `if __name__ == "__main__":` |

Otro tropiezo: activar el entorno en una terminal y ejecutar en otra. El prompt `(.venv)` debe aparecer donde lanzas `python3`.

:::error
No uses `pip install` todavía. Todos los ejemplos funcionan con la biblioteca estándar.
:::

## Buenas prácticas

- **snake_case** para variables y funciones; **PascalCase** para clases.
- **Una clase, una responsabilidad.** `Personaje` no abre ventanas ni guarda archivos.
- **Docstring breve** en cada clase pública.
- **Todos los atributos en `__init__`** si el objeto siempre debe tenerlos.
- **Valida en el borde**: si `hp` no puede ser negativo, protégelo donde cambia.
- **Commits pequeños y frecuentes**, con mensajes en imperativo.
- **Ejecuta y documenta antes de entregar**: comando y carpeta en el README.

## Checklist de la semana

- [ ] Python 3.12 responde en la terminal.
- [ ] VS Code con la extensión de Python y el intérprete seleccionado.
- [ ] Entorno virtual activo y excluido en `.gitignore`.
- [ ] Repositorio local con un commit y remoto en GitHub.
- [ ] `personaje.py` ejecuta sin errores.
- [ ] Explico clase y objeto con un ejemplo propio.
- [ ] Entregué el enlace en el EVA/LMS.

## Resumen

Esta semana montaste el taller y escribiste tu primer molde. Una **clase** define atributos y métodos; un **objeto** es una instancia con estado propio. Python hace visible la idea porque todo valor es un objeto. `__init__` construye, `self` identifica y los métodos modifican el objeto que los recibe.

También dejaste listo el flujo que usarás hasta el final: Python 3.12, VS Code, `venv`, Git y GitHub. Un proyecto ordenado se puede ejecutar, revisar y recuperar.

## Siguiente paso

La próxima semana compararás formas de pensar el software. Resolverás el mismo combate con funciones y con clases, verás qué gana y qué pierde cada enfoque, y aprenderás a dibujar un UML antes de escribir código. Llega con tu repositorio funcionando: el ejercicio de refactorización parte de un script procedural que tú mismo vas a mejorar.
