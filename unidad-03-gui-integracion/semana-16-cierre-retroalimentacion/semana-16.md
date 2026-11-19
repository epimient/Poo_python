# Semana 16 — Retroalimentación y cierre

> Un proyecto termina cuando otra persona puede entenderlo, ejecutarlo y explicarlo sin ti.

## Objetivos de aprendizaje

- Aplicar una checklist de calidad a tu proyecto y al de un compañero.
- Dar y recibir code review con comentarios accionables.
- Sustentar un proyecto sin leer el código línea por línea.
- Publicar un portafolio legible en GitHub con README y demo.
- Autoevaluarte con la rúbrica usando evidencia.
- Elegir un siguiente paso con una ruta clara.

## ¿Por qué importa?

Imagina dos entregas. La primera funciona, pero su README dice «proyecto final» y nadie sabe qué hace la clase `Gestor`. La segunda tiene una pantalla menos, pero nombres honestos, errores claros y un README con captura y tres pasos para ejecutarla. En una feria consigue más preguntas; en una entrevista, también.

El code review es práctica diaria en cualquier equipo: no es un examen, es la forma en que circula el conocimiento y se detectan errores antes de producción. En banca, un `print` en una transferencia puede filtrar datos a los logs. En un videojuego, un método de 200 líneas que calcula daño y dibuja la barra de vida impide balancear el combate.

No aprendes sintaxis nueva: aprendes a mirar tu proyecto con los ojos de quien lo ejecutará, revisará y quizá te contrate.

## Concepto central

### Code review entre pares

Tres reglas para revisar código:

1. **Revisa el código, no a la persona.** «Este método mezcla validación y escritura» dice qué cambiar; «esto está mal» no.
2. **Pregunta antes de afirmar.** «¿Qué pasa si la lista llega vacía?» abre la conversación; «te falta validar» la cierra.
3. **Prioriza.** Primero lo que afecta el comportamiento o la comprensión; después el estilo.

Un buen comentario incluye el dónde, el porqué y una salida:

| Comentario que no ayuda | Comentario que abre conversación |
|---|---|
| «Mal.» | «`procesar_todo` hace tres cosas; ¿lo dividimos en `calcular_total` y `resumir`?» |
| «Falta validar.» | «Si `precio` llega negativo, el total baja. ¿Agregamos una validación?» |
| «Usa nombres claros.» | «`x` parece ser la cantidad de pociones; ¿la renombramos?» |

Revisa primero que el proyecto se ejecute, después el diseño, luego los casos límite y al final el estilo. Al revés, discutirás sangrías mientras la vista escribe en la base de datos.

:::info
El revisor no arregla el código del otro: señala, propone y deja decidir. Si corriges tú, el autor no aprende y el historial miente.
:::

### Checklist de calidad

Es el corazón de la semana: úsala antes de entregar y antes de revisar a alguien más.

| Dimensión | Pregunta de control | Señal de alerta |
|---|---|---|
| Nombres | ¿Se entiende qué guarda o qué hace sin leer el cuerpo? | `d`, `x2`, `Gestor`, `hacer_cosas` |
| Encapsulamiento | ¿Los datos internos se modifican solo por métodos públicos? | `self.saldo` público y editado desde fuera |
| Responsabilidad única | ¿Cada clase tiene un motivo para cambiar? | Una clase que valida, guarda y dibuja |
| Validaciones | ¿Se rechazan datos imposibles antes de usarlos? | Precio negativo, nombre vacío, cantidad cero |
| Separación de capas | ¿La interfaz no contiene reglas de negocio? | Tkinter calculando impuestos |
| Manejo de errores | ¿Los fallos se capturan y se explican? | `except: pass` o un traceback crudo |
| README | ¿Otra persona puede ejecutar el proyecto en cinco minutos? | Sin requisitos, sin captura, sin comandos |

Una checklist no reemplaza el criterio: si una casilla no se puede marcar con evidencia, no está resuelta.

### Cómo presentar un proyecto

La sustentación cuenta la historia de un problema y tus decisiones. Ocho minutos alcanzan:

1. **Problema (1 min).** Qué resuelve y para quién; un ejemplo concreto vale más que una lista de funciones.
2. **Demo (3 min).** El flujo principal funcionando. Ten un plan B grabado por si falla la red.
3. **Arquitectura (1,5 min).** Dos o tres clases clave y cómo se relacionan; un diagrama simple.
4. **Decisiones (1,5 min).** Por qué separaste la lógica de la interfaz y qué validación evita qué error.
5. **Aprendizajes y siguiente paso (1 min).** Qué harías distinto con una semana más.

:::warning
Si tu sustentación consiste en leer el código línea por línea, el jurado no puede evaluar si entiendes el diseño. Explica el porqué; el cómo ya está en el repositorio.
:::

### Portafolio en GitHub

Tu portafolio es la colección de proyectos que puedes defender: tres terminados valen más que quince a medias.

- **README primero.** Qué es, captura, requisitos y cómo ejecutar.
- **Historial honesto.** Commits pequeños en imperativo: `agrega validación de saldo`, no `cambios`.
- **Un repositorio por proyecto.** No mezcles el proyecto final con apuntes de clase.
- **Sin secretos.** Nunca subas contraseñas, tokens ni datos reales.
- **Fija en tu perfil** tus dos o tres mejores proyectos.

### Autoevaluación con la rúbrica

Antes de conocer la nota oficial, ponte una:

| Criterio | Peso | Evidencia que debes poder mostrar |
|---|---|---|
| Funcionalidad | 30 % | El flujo principal corre de principio a fin |
| POO y diseño | 25 % | Clases con responsabilidad clara y datos encapsulados |
| Validaciones y errores | 15 % | Casos límite probados y mensajes comprensibles |
| Claridad y documentación | 15 % | Nombres, docstrings y README ejecutable |
| Sustentación | 15 % | Explicas decisiones, no solo pantallas |

Si te pones 5, escribe qué evidencia lo sostiene; si te pones 3, qué falta. La autoevaluación detecta huecos, no negocia la nota.

### Siguientes pasos

Estas rutas parten de lo que ya sabes:

| Ruta | Qué practicas | Primer paso concreto |
|---|---|---|
| Videojuegos con Pygame | Bucle de juego, sprites, colisiones | Mueve un personaje con el teclado y dibuja su inventario en pantalla |
| Desarrollo web | Rutas, formularios, sesiones, APIs | Publica una página que consuma datos de tu proyecto |
| Datos y automatización | Lectura de archivos, reportes, gráficas | Convierte un CSV de ventas en un resumen por categoría |
| Diseño de videojuegos | Prototipos, balance, experiencia | Documenta el sistema de combate de tu proyecto y ajústalo con pruebas |

No aprendas las cuatro: elige una y termina algo pequeño en dos semanas. Un proyecto terminado enseña más que cuatro cursos empezados.

## Código paso a paso

El ejemplo es un revisor orientado a objetos que usa `ast` para reportar cinco señales: clase sin docstring, atributos públicos, método largo, `print` en la lógica y falta de type hints.

Primero, un objeto que representa un hallazgo y valida su severidad:

```python
class Hallazgo:
    """Un problema concreto detectado en una línea del código."""

    __slots__ = ("regla", "linea", "detalle", "severidad")

    def __init__(self, regla: str, linea: int, detalle: str,
                 severidad: str = "media") -> None:
        if severidad not in SEVERIDADES:
            raise ValueError(f"Severidad no válida: {severidad}")
        self.regla = regla
        self.linea = linea
        self.detalle = detalle
        self.severidad = severidad
```

La clase base `Regla` define el contrato: cada regla hereda, sobrescribe `revisar` y usa `_crear`. Una regla real busca `print` dentro de funciones que no sean de presentación:

```python
class PrintEnLogica(Regla):
    nombre = "print en lógica"
    severidad = "alta"
    EXENTOS = {"__str__", "mostrar", "main"}

    def revisar(self, arbol: ast.AST) -> list[Hallazgo]:
        hallazgos = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.FunctionDef) and nodo.name not in self.EXENTOS:
                for interno in ast.walk(nodo):
                    if isinstance(interno, ast.Call) and getattr(interno.func, "id", "") == "print":
                        hallazgos.append(self._crear(interno, f"print en '{nodo.name}'"))
        return hallazgos
```

El `Revisor` guarda las reglas y convierte el texto en árbol; el `Informe` ordena, deduplica y decide el veredicto. Ejecuta el archivo para ver los dos fragmentos.

## Diagrama / modelo

```text
código fuente
     │
     ▼
 ast.parse() ──► árbol sintáctico
     │
     ▼
 Revisor ──► [DocstringDeClase, AtributosPublicos, MetodoLargo,
              PrintEnLogica, FaltaTypeHints]
     │
     ▼
 lista de Hallazgo (regla, línea, detalle, severidad)
     │
     ▼
 Informe ──► ordena, cuenta, imprime veredicto
```

Cada regla conoce una sola señal: para detectar `except: pass`, agregas una clase y la registras sin tocar las demás. Eso es responsabilidad única aplicada a una herramienta real.

## Errores comunes

- **Revisar solo el estilo** antes que las validaciones ausentes.
- **Reescribir el código ajeno:** el autor no aprende y el historial miente.
- **Sustentar leyendo código:** el jurado evalúa el diseño, no tu velocidad de lectura.
- **Un README que no permite ejecutar:** sin comandos ni datos de ejemplo, el proyecto queda a medias.
- **Autoevaluarse sin evidencia:** «creo que merezco 5» no es un argumento.

:::error
Nunca subas a GitHub contraseñas, tokens ni bases con datos reales. Un repositorio público conserva el historial: borrar el archivo no borra el commit.
:::

## Buenas prácticas

- Revisa tu propio proyecto en voz alta antes de que lo haga otro: explicar revela huecos.
- Deja comentarios con una propuesta concreta, no solo con una queja.
- Incluye en el README una sección «Decisiones»: qué cambiaste y por qué.
- Graba una demo corta: es tu respaldo y material de portafolio.
- Ensaya la sustentación con cronómetro y sin abrir el editor.

:::reto
Intercambia tu proyecto con un compañero. Cada uno revisa el del otro con la checklist, escribe cinco comentarios accionables y se los devuelve. No corrijan el código ajeno: solo señalen y propongan.
:::

## Checklist de la semana

- [ ] Mi proyecto se ejecuta desde cero siguiendo mi propio README.
- [ ] Mis clases tienen docstring y nombres comprensibles.
- [ ] Los atributos internos son protegidos y se acceden por métodos o propiedades.
- [ ] Cada clase tiene una responsabilidad que puedo explicar en una frase.
- [ ] Las validaciones rechazan datos imposibles antes de guardarlos.
- [ ] La interfaz no contiene reglas de negocio ni acceso a datos.
- [ ] Los errores previsibles tienen mensajes claros; no hay `except: pass`.
- [ ] Revisé el proyecto de un compañero y recibí su revisión del mío.
- [ ] Mi portafolio tiene tres repositorios terminados y con README.

## Resumen

Esta semana convertiste el código en algo revisable, presentable y heredable. Aprendiste a dar retroalimentación útil, a usar una checklist con evidencia, a sustentar decisiones y a publicar un portafolio honesto. `revision_final.py` mostró que la POO también construye herramientas: una regla, una clase; un hallazgo, un objeto.

El curso se cierra; tu criterio apenas empieza. La diferencia entre aprobar y programar no es recordar sintaxis, sino revisar, explicar y reintentar con mejores preguntas.

## Siguiente paso

Elige una ruta y define un proyecto pequeño para las próximas dos semanas. Escríbelo en tu README como «Próximos pasos» con tres tareas concretas. Luego pide a alguien que no haya visto el curso que lo ejecute sin ayuda: lo que no pueda hacer es lo que falta documentar.
