# Dudas frecuentes — Semana 07

## ¿Agregación y composición no son lo mismo?
No. Ambas son relaciones todo-parte, pero cambian el ciclo de vida. En la agregación la parte existe por su cuenta y sobrevive al todo; en la composición la parte la crea el todo y muere con él. El rombo UML también cambia: hueco para agregación, relleno para composición.

## ¿Cómo decido cuál usar?
Pregunta qué debe pasar al borrar el todo. Si la parte debe desaparecer, composición. Si debe seguir existiendo o compartirse, agregación. También ayuda preguntar si la parte tiene identidad propia fuera del contenedor: una poción suelta no, un personaje sí.

## Si Python usa referencias para todo, ¿la composición existe de verdad?
Existe como **contrato de diseño**, no como restricción del lenguaje. Se implementa con tres decisiones: el todo crea sus partes, no acepta partes externas y no filtra referencias internas. El lenguaje no te obliga, pero el modelo y las validaciones sí pueden hacerlo.

## ¿Por qué mi ítem sobrevive si borré el inventario?
Porque alguien más lo referencia. Puede ser una variable (`item = inventario.obtener(...)`), una lista externa o una estructura de depuración. La composición se rompe en cuanto el objeto sale del control del dueño. Revisa quién guarda la referencia y elimínala.

## ¿Puedo usar `__del__` para cerrar recursos o actualizar contadores?
No es recomendable para reglas de negocio. `__del__` puede ejecutarse tarde, en un orden inesperado o no ejecutarse durante el cierre del intérprete. Para demostrar ciclos de vida usa `weakref.finalize`; para cerrar recursos, un método explícito como `cerrar()` o un context manager.

## ¿Dónde va el rombo en el diagrama UML?
Siempre en el extremo del **todo**, junto a la clase contenedora. Relleno si es composición, hueco si es agregación. Si lo pones del lado de la parte, el diagrama está afirmando lo contrario.

## ¿Una clase puede tener composición y agregación a la vez?
Sí, y es común. Una `Mochila` puede crear pociones (composición) y recibir una espada legendaria que existe en el mundo (agregación). Lo importante es documentar cada relación y no mezclar las reglas: la poción muere con la mochila, la espada no.

## ¿Cómo pruebo que el ownership funciona?
Elimina el contenedor y verifica qué queda vivo. También intenta operaciones indebidas: agregar la misma parte a dos contenedores, consumir dos veces o usar una parte después de borrar el todo. Si el código lo impide o lo hace explícito, el contrato está bien definido.
