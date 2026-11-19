# Dudas frecuentes — Semana 16

## ¿Code review es lo mismo que alguien me corrija el código?

No. Corregir es modificar; revisar es señalar y proponer. El revisor deja comentarios con línea, problema y una salida posible, y el autor decide e implementa. Si el revisor hace commit de sus cambios, el autor no aprende y el historial atribuye el trabajo a quien no lo hizo.

## ¿Cuántos comentarios debo dejar en una revisión?

Los suficientes para que el proyecto mejore, no todos los posibles. Empieza por lo que afecta el comportamiento: validaciones ausentes, datos públicos, errores silenciados. Después el diseño y al final el estilo. Cinco comentarios bien argumentados valen más que treinta correcciones de espacios.

## ¿Qué hago si no estoy de acuerdo con un comentario?

Pregunta antes de defender. «¿En qué caso falla mi versión?» suele aclarar si el comentario tiene razón. Si no la tiene, explica tu decisión con una prueba o un ejemplo y deja constancia en el hilo. El desacuerdo técnico es sano; ignorar el comentario sin responder, no.

## ¿Cómo sustento si la demo falla o me pongo nervioso?

Ten un plan B: una grabación de dos o tres minutos y datos de ejemplo cargados. Si algo falla en vivo, dilo y pasa al respaldo; el jurado evalúa tu comprensión, no la estabilidad de la red. Ensaya al menos dos veces con cronómetro y sin editor abierto.

## ¿Qué debe llevar el README como mínimo?

```md
# Nombre del proyecto

Qué resuelve y para quién.

## Cómo ejecutar
python3 main.py

## Requisitos
Python 3.12 o superior. Sin dependencias externas.

## Decisiones
Por qué separé la lógica de la interfaz y cómo valido los datos.

## Próximos pasos
Tres tareas concretas.
```

Si otra persona puede ejecutarlo con esas instrucciones, el README cumple.

## ¿Sirve subir proyectos académicos a GitHub?

Sí, si están terminados y documentados. Un proyecto de curso con README claro, historial de commits y demo funciona como evidencia de que sabes construir y explicar. Lo que no ayuda es un repositorio con el enunciado copiado y sin código propio.

## ¿Cómo me autoevalúo sin ser injusto?

Puntúa con evidencia, no con intención. Para cada criterio escribe qué se puede verificar: «el flujo de reserva corre de inicio a fin», «el saldo no se puede editar desde fuera», «probé cantidad cero y muestra mensaje». Si no encuentras evidencia, la nota es la que corresponde a lo que falta, no a lo que planeabas hacer.

## ¿Qué ruta elijo después del curso?

La que te permita terminar algo pequeño en dos semanas. Si dudas, elige Pygame para reforzar bucles y estados, desarrollo web para practicar interfaces y datos, o análisis de datos para trabajar con archivos reales. No empieces las tres: termina una y úsala como base del siguiente proyecto.
