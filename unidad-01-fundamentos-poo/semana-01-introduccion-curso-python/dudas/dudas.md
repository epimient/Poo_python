# Dudas frecuentes — Semana 01

## ¿Cuál es la diferencia entre `python` y `python3`?

En Linux y macOS, `python` puede no existir o apuntar a una versión antigua. `python3` es el comando seguro para llamar a Python 3. En Windows, el instalador de python.org suele crear `python` y el lanzador `py`. Para fijar la versión exacta usa `py -3.12`.

```bash
python3 --version
# Python 3.12.x
```

Si `python3 --version` no devuelve 3.12, revisa qué intérprete tienes instalado antes de seguir con el curso.

## ¿Por qué aparece `(.venv)` en la terminal?

Ese prefijo indica que el entorno virtual está activo. Significa que `python` y `pip` apuntan a la copia del proyecto, no a la instalación global del sistema. Para desactivarlo:

```bash
deactivate
```

Si abres una terminal nueva, el entorno no queda activo automáticamente: debes volver a activarlo desde la carpeta del proyecto.

## Creé el entorno virtual pero `python` sigue usando el del sistema. ¿Qué hago?

Comprueba la ruta del intérprete:

```bash
which python    # Linux/macOS
where python    # Windows
```

Debe mostrar una ruta dentro de `.venv`. Si no es así, activa el entorno de nuevo y verifica que estás en la carpeta correcta. En VS Code, selecciona el intérprete con `Ctrl+Shift+P` → *Python: Select Interpreter*.

## ¿Por qué crear una clase si puedo usar un diccionario?

Puedes. De hecho, en la Semana 02 verás un combate resuelto con diccionarios y funciones. La diferencia aparece cuando el programa crece: una clase agrupa datos y comportamiento, permite validar en un solo lugar y deja claro qué operaciones tienen sentido para ese tipo de objeto. Un diccionario acepta cualquier clave nueva sin avisar; una clase bien diseñada protege sus reglas.

```python
# Con diccionario, nada impide un hp negativo
personaje = {"nombre": "Kaede", "hp": -10}

# Con una clase puedes validar en el constructor
class Personaje:
    def __init__(self, nombre: str, hp: int) -> None:
        if hp <= 0:
            raise ValueError("El hp debe ser mayor que cero")
        self.nombre = nombre
        self.hp = hp
```

## ¿Qué es exactamente `self`?

`self` es el objeto que recibe la llamada. Cuando escribes `kaede.atacar(rook)`, Python pasa `kaede` como primer argumento y `rook` como segundo. Por eso la definición es `def atacar(self, objetivo):`. No es una palabra reservada del lenguaje, pero es la convención que todo el mundo espera; no la cambies.

## Me sale `IndentationError`. ¿Qué reviso?

Python usa la indentación para delimitar bloques. Revisa que:

- Todas las líneas de un mismo bloque tengan la misma cantidad de espacios.
- No mezcles tabuladores y espacios en el mismo archivo.
- Después de `class`, `def`, `if`, `for` y `while` haya dos puntos y una línea indentada.

En VS Code, activa *Render Whitespace* y configura tabulaciones de 4 espacios. El error suele estar en la línea anterior a la que reporta el intérprete.

## ¿Debo subir la carpeta `.venv` a GitHub?

No. El entorno virtual contiene binarios y rutas absolutas de tu computadora; no es portable y ocupa mucho espacio. Crea un `.gitignore` con:

```text
.venv/
__pycache__/
*.pyc
```

Cualquier compañero puede reconstruir el entorno con `python3 -m venv .venv` y volver a instalar las dependencias. En este curso casi no habrá dependencias externas, así que el repositorio será pequeño.

## ¿Cómo entrego la actividad en el EVA/LMS?

Sube el enlace de tu repositorio de GitHub y, si el docente lo pide, un archivo comprimido sin `.venv/` ni `__pycache__/`. Antes de entregar:

1. Ejecuta `python3 personaje.py` y confirma que no hay errores.
2. Revisa que el repositorio tenga un README con las instrucciones de ejecución.
3. Haz `git status` y `git log --oneline` para confirmar que tus cambios están registrados.
4. Comprueba que el enlace abre sin iniciar sesión (repositorio público) o que el docente tiene acceso.

Si el enlace no abre o el script no corre, la entrega se considera incompleta aunque el código esté en tu computadora.
