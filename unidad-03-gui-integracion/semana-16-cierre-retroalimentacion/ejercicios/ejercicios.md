# Ejercicios — Semana 16

## Nivel 1 — Básico: Revisión de una clase

**Enunciado.** Recibes la siguiente clase de un compañero. Aplica la checklist de calidad y entrega una revisión escrita con al menos cinco hallazgos, cada uno con línea, problema y propuesta.

```python
class Personaje:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def recibir_danio(self, cantidad):
        print("Recibiendo daño:", cantidad)
        self.vida = self.vida - cantidad
        if self.vida < 0:
            self.vida = 0

    def atacar(self, enemigo):
        enemigo.vida = enemigo.vida - self.ataque
        print(self.nombre, "atacó a", enemigo.nombre)
        return enemigo.vida
```

**Requisitos.**
- Numera cada hallazgo con la línea exacta y clasifícalo (alta, media o baja).
- Propón un cambio concreto para cada hallazgo, sin reescribir toda la clase.
- Señala al menos un caso límite que la clase no maneja.

**Entrada esperada.**
El código anterior y la checklist de siete dimensiones vista en la semana.

**Salida esperada.**
Un archivo `revision-companero.md` con una tabla de hallazgos y un párrafo final de veredicto: ¿se puede entregar así o requiere ajustes?

**Criterios de evaluación.**
- [ ] Cada hallazgo indica línea, problema y propuesta.
- [ ] Se detectan atributos públicos y `print` dentro de la lógica.
- [ ] Se menciona al menos una validación ausente (vida negativa, ataque negativo o enemigo sin vida).
- [ ] El veredicto se sostiene con los hallazgos, no con una opinión general.

---

## Nivel 2 — Intermedio: Sustentación de ocho minutos

**Enunciado.** Prepara la sustentación de tu proyecto final con la estructura de la semana: problema, demo, arquitectura, decisiones y aprendizajes. Entrega el guion y preséntalo ante dos compañeros con cronómetro.

**Requisitos.**
- Escribe un guion de máximo 900 palabras con tiempos por bloque (1, 3, 1,5, 1,5 y 1 minuto).
- Incluye un diagrama de dos o tres clases y explica una decisión de encapsulamiento y una de separación de capas.
- Prepara una demo de tres minutos que funcione sin conexión y un plan B grabado.
- Anticipa tres preguntas del jurado y escribe su respuesta.

**Entrada esperada.**
Tu proyecto final ejecutable y el README del repositorio.

**Salida esperada.**
`guion-sustentacion.md` con tiempos, enlaces a la demo y las tres preguntas anticipadas. La presentación real dura entre 7 y 9 minutos.

**Criterios de evaluación.**
- [ ] El guion sigue los cinco bloques y respeta los tiempos.
- [ ] Se explica el porqué de al menos dos decisiones técnicas.
- [ ] La demo cubre el flujo principal sin leer código.
- [ ] Las respuestas a las preguntas anticipadas son concretas y breves.

---

## Nivel 3 — Reto: Plan de portafolio y README profesional

**Enunciado.** Convierte tu trabajo del curso en un portafolio defendible. Elige tres proyectos (por ejemplo, el creador de personajes, el arcade y la aplicación con Tkinter), escribe el README de cada uno y un plan de dos semanas para el siguiente proyecto.

**Requisitos.**
- Cada README debe incluir: qué es, captura o demo, requisitos, cómo ejecutar, decisiones y próximos pasos.
- El plan debe tener tres tareas concretas con fecha y una ruta de estudio elegida (Pygame, desarrollo web, datos o diseño de videojuegos).
- Incluye una tabla de autoevaluación con los cinco criterios de la rúbrica y una evidencia por criterio.
- Revisa los tres repositorios: sin contraseñas, sin bases con datos reales y con commits en imperativo.

**Entrada esperada.**
Tus repositorios del curso, tu README actual y la rúbrica de autoevaluación.

**Salida esperada.**
Tres README actualizados, un archivo `plan-portafolio.md` y una captura del perfil de GitHub con los proyectos fijados.

**Criterios de evaluación.**
- [ ] Los tres README permiten ejecutar el proyecto sin ayuda externa.
- [ ] El plan tiene tres tareas con fecha y una ruta justificada.
- [ ] La autoevaluación cita una evidencia verificable por criterio.
- [ ] No hay secretos ni datos reales en el historial de los repositorios.
- [ ] Los commits recientes describen el cambio en imperativo.
