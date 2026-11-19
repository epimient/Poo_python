# Ejemplo guiado — Semana 03

## Qué construye

`personaje.py` define la clase `Personaje` con tres atributos de instancia (`nombre`, `hp`, `nivel`) y dos atributos de clase (`MAX_HP` y `total_personajes`). El programa crea un equipo de tres personajes, muestra su estado con una barra de vida en texto, compara identidad y tipo, imprime el `__dict__` de cada objeto y demuestra qué pasa al asignar un atributo sobre una instancia.

## Cómo ejecutarlo

```bash
cd ejemplo-guiado
python3 personaje.py
```

No pide datos: usa un modo demo con valores fijos, así que puedes ejecutarlo tantas veces como quieras.

## Salida esperada

```text
=== Semana 03: clases, objetos y atributos ===
Personajes creados al inicio: 0

Equipo Alba
-----------
Aria     Nv.3  [########--] 80/100
Brom     Nv.2  [##########] 100/100
Cyd      Nv.5  [####------] 45/100
Nivel combinado: 10 | hp total: 225

Identidad y tipo
id(aria) = 140234...
type(aria) = Personaje
isinstance(aria, Personaje) = True
aria is brom -> False

Atributos por objeto (__dict__)
Aria: {'nombre': 'Aria', 'hp': 80, 'nivel': 3}
Brom: {'nombre': 'Brom', 'hp': 100, 'nivel': 2}
Cyd: {'nombre': 'Cyd', 'hp': 45, 'nivel': 5}

Atributos de clase
Personaje.MAX_HP = 100
Personaje.total_personajes = 3
'MAX_HP' en aria.__dict__? False

Cambiar el hp de un objeto no afecta a los demás
Brom: {'nombre': 'Brom', 'hp': 95, 'nivel': 2}
Aria: {'nombre': 'Aria', 'hp': 80, 'nivel': 3}

Cuidado al asignar sobre una instancia
cyd.MAX_HP = 120  -> atributo propio
Personaje.MAX_HP = 100  -> intacto
'MAX_HP' en cyd.__dict__? True

Fin de la demo. Personajes creados: 3
```

El valor de `id(aria)` cambia en cada ejecución; es normal.

## Puntos clave

1. **La clase es el molde.** `Personaje` se define una vez; `aria`, `brom` y `cyd` son tres objetos independientes creados a partir de ella.
2. **`self` guarda por objeto.** Cada llamada a `__init__` escribe en el `__dict__` del objeto que se está creando. Modificar `brom.hp` no toca `aria.hp`.
3. **Los atributos de clase se comparten.** `MAX_HP` y `total_personajes` viven en la clase; el contador se incrementa con `Personaje.total_personajes`, no con `self`.
4. **`__dict__` solo muestra lo propio.** `MAX_HP` no aparece en el diccionario de la instancia porque se busca en la clase.
5. **Asignar sobre la instancia crea un atributo nuevo.** `cyd.MAX_HP = 120` no cambia la constante global: crea una sombra local para ese objeto. Es una fuente habitual de confusión.

## Para experimentar

- Añade un cuarto personaje y comprueba cómo cambia el contador.
- Cambia `hp=45` por `hp=0` y observa que la clase no valida nada todavía. En la Semana 04 añadirás esa protección.
- Crea dos objetos con los mismos datos y verifica con `is` que siguen siendo distintos.
