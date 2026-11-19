# Ejemplo guiado — Revisor de código con POO

## Qué construye

`revision_final.py` es un revisor de código orientado a objetos. Analiza un fragmento de Python, lo convierte en árbol sintáctico con `ast` y aplica cinco reglas:

| Regla | Qué detecta | Severidad |
|---|---|---|
| `DocstringDeClase` | Clases sin docstring | media |
| `AtributosPublicos` | Atributos `self.x` que deberían ser `self._x` | alta |
| `MetodoLargo` | Métodos de más de 12 líneas | media |
| `PrintEnLogica` | `print()` dentro de métodos que no son de presentación | alta |
| `FaltaTypeHints` | Parámetros o retornos sin anotación | baja |

El programa incluye dos fragmentos: uno con problemas deliberados y otro corregido. Así se ven los dos veredictos posibles.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 revision_final.py
```

No requiere dependencias externas ni datos de entrada.

## Salida esperada

```text
================================================================
                 INFORME DE REVISIÓN DE CÓDIGO
================================================================
 Fuente          : fragmento con problemas · inventario.py
 Reglas aplicadas: 5
 Hallazgos       : 10
----------------------------------------------------------------
 L  1  [MEDIA ] Docstring de clase: la clase 'Inventario' no tiene docstring
 L  2  [BAJA  ] Type hints: '__init__' sin anotación en: duenio
 L  2  [BAJA  ] Type hints: '__init__' sin tipo de retorno
 L  3  [ALTA  ] Encapsulamiento: atributo público 'self.duenio' en 'Inventario'
 L  4  [ALTA  ] Encapsulamiento: atributo público 'self.objetos' en 'Inventario'
 L  6  [BAJA  ] Type hints: 'agregar' sin anotación en: objeto
 L  6  [BAJA  ] Type hints: 'agregar' sin tipo de retorno
 L  7  [ALTA  ] print en lógica: 'print' dentro de 'agregar'
 L 10  [MEDIA ] Método largo: 'procesar_todo' ocupa 18 líneas (límite 12)
 L 10  [BAJA  ] Type hints: 'procesar_todo' sin tipo de retorno
----------------------------------------------------------------
 Alta: 3   Media: 2   Baja: 5
 Veredicto: Requiere ajustes antes de entregar
================================================================
```

El segundo informe, sobre el fragmento corregido, termina con `Sin hallazgos: listo para revisión de pares`.

## Puntos clave

1. **Un hallazgo es un objeto.** `Hallazgo` guarda regla, línea, detalle y severidad; valida la severidad en el constructor para que un dato inválido no llegue al informe.
2. **Una regla, una responsabilidad.** Cada clase hereda de `Regla` y sobrescribe `revisar`. Agregar una detección nueva no obliga a tocar las existentes.
3. **El revisor no imprime mientras analiza.** `Revisor` devuelve un `Informe`; solo `Informe.mostrar()` escribe en consola. Separar cálculo y presentación es la misma idea que separar lógica e interfaz en Tkinter.
4. **El informe ordena y deduplica.** Los hallazgos se ordenan por línea y severidad, y se eliminan duplicados antes de contar. Un informe legible es parte del resultado, no un extra.
5. **`ast` sin complejidad.** No hay análisis semántico: se recorren nodos, se cuentan líneas y se buscan llamadas. Es suficiente para una primera señal y deja claro dónde estaría el límite de la herramienta.
