# P3 · Proyecto integrador: arcade con interfaz gráfica

**Unidad 3 — Interfaces gráficas e integración** · Semana 15 · **45% de la nota final** · Equipos de 2 a 3 personas

---

## Contexto

El arcade de consola necesita dar el salto al escritorio. La dirección quiere una aplicación con **interfaz gráfica** para administrar personajes, ítems y partidas, y para jugar un combate por turnos sin escribir comandos. El sistema debe conservar la información entre ejecuciones y mantener la lógica de negocio separada de la interfaz.

Tu equipo debe entregar una aplicación de escritorio funcional construida con **Tkinter + ttk**, aplicando todo lo aprendido en el curso: clases, encapsulamiento, relaciones, herencia, polimorfismo, eventos y organización por capas.

> También se acepta una temática de **banca** (clientes, cuentas y transacciones) si el equipo prefiere un dominio administrativo. Los requisitos técnicos son exactamente los mismos.

---

## Objetivo

Construir una aplicación de escritorio que permita **crear, consultar, actualizar y eliminar** al menos dos entidades relacionadas, ejecutar una acción propia del dominio (combate, simulación o transacción) y **persistir** los datos, con una interfaz clara, validada y conectada a la lógica de negocio.

---

## Opción A — Videojuego (recomendada)

Entidades mínimas:

- **Personaje**: nombre, clase, nivel, hp, hp_max, ataque, defensa.
- **Ítem**: nombre, tipo (arma, poción, armadura), poder, precio, stock.
- **Inventario** o **Partida**: relación entre personajes e ítems, o registro de combates.

Funcionalidades:

1. **Personajes**: listar, crear, editar, eliminar y ver detalle.
2. **Ítems**: listar, crear, editar, eliminar y asignar a un personaje.
3. **Combate**: elegir dos personajes y simular un duelo por turnos con registro visual.
4. **Persistencia**: guardar y cargar personajes, ítems e historial en JSON.
5. **Búsqueda/filtro** por nombre o clase (deseable).

## Opción B — Banca

Entidades mínimas:

- **Cliente**: documento, nombre, correo, teléfono.
- **Cuenta**: número, tipo (ahorro/corriente), saldo, cliente asociado.
- **Transacción**: tipo (depósito/retiro), monto, fecha, cuenta.

Funcionalidades:

1. **Clientes**: CRUD completo.
2. **Cuentas**: CRUD, asociadas a un cliente.
3. **Transacciones**: depósitos y retiros con validación de saldo, historial por cuenta.
4. **Persistencia** en JSON.
5. **Búsqueda/filtro** por documento o número de cuenta (deseable).

---

## Requisitos funcionales

1. Ventana principal con navegación entre al menos **tres vistas**: listado, formulario y acción de dominio (combate o transacciones).
2. **CRUD completo** de las dos entidades principales.
3. **Validación visual**: mensajes de error junto al campo o en un área de estado; nunca un `print` como única respuesta.
4. **Confirmación** antes de eliminar.
5. **Persistencia**: los datos se guardan en un archivo JSON y se recuperan al iniciar.
6. **Acción de dominio** integrada: combate por turnos o transacción bancaria.
7. **Manejo de errores**: archivo corrupto, campos vacíos, valores no numéricos, entidades inexistentes.
8. La aplicación no debe cerrarse ante un error del usuario.

---

## Requisitos técnicos

### CE3.1 — Interfaz gráfica y organización (50%)

- Usa **Tkinter + ttk** (sin PyQt, CustomTkinter ni dependencias externas).
- Organiza la interfaz con **Frames**, `pack`, `grid` o `place` de forma coherente.
- Usa al menos **6 widgets distintos**: `Label`, `Entry`, `Button`, `Combobox`, `Treeview`, `Notebook`, `Frame`, `LabelFrame` o `Text`.
- Aplica un estilo consistente con `ttk.Style` (colores, fuentes, padding).
- La ventana debe ser usable en 1024×768 y adaptarse al redimensionar.
- Separa la interfaz de la lógica: las vistas no deben contener reglas de negocio.
- Incluye un **prototipo/wireframe** en el README y explica cómo se corresponde con la implementación.

### CE3.2 — Eventos e integración con la lógica OO (50%)

- Conecta botones con `command` y al menos un evento con `bind` (teclado, selección de tabla, cierre de ventana).
- Los callbacks deben delegar en **servicios** o clases de dominio, no implementar la lógica completa.
- Modelo por capas obligatorio:

```text
proyecto/
├── main.py
├── modelos/
│   ├── personaje.py
│   └── item.py
├── datos/
│   └── repositorio_json.py
├── servicios/
│   └── servicio_partida.py
└── vistas/
    ├── ventana_principal.py
    ├── vista_personajes.py
    ├── vista_items.py
    └── vista_combate.py
```

- Usa clases con encapsulamiento y validaciones (reutiliza lo de la Unidad 1).
- Usa herencia/abstractas/polimorfismo donde aporte valor (por ejemplo, tipos de ítem o de personaje).
- La interfaz se actualiza después de cada operación (tabla, etiquetas, mensajes).
- Implementa un **registro de actividad** visible (log de combate o de transacciones).
- Guarda y carga con `json`; maneja `FileNotFoundError` y `json.JSONDecodeError`.

> **Prohibido:** lógica de negocio dentro de los `command`, variables globales para el estado, `print()` como interfaz de usuario y acceso directo a los atributos privados del modelo.

---

## Entregables

| Entregable | Descripción |
|---|---|
| Código fuente | Proyecto completo por capas, ejecutable con `python3 main.py` |
| `README.md` | Descripción, capturas, wireframe, arquitectura, instrucciones y decisiones |
| Video demo | 4–6 minutos: recorrido completo de la aplicación |
| Datos de ejemplo | `datos.json` con al menos 5 personajes/ítems o clientes/cuentas |
| Sustentación | Cada integrante explica una capa distinta y responde preguntas |

---

## Flujo mínimo esperado (opción videojuego)

```text
[Vista Personajes]
  → Crear personaje (formulario validado)
  → Guardar
  → Aparece en la tabla
  → Editar nivel
  → Eliminar con confirmación

[Vista Ítems]
  → Crear ítem
  → Asignar a personaje
  → Ver inventario

[Vista Combate]
  → Elegir personaje del jugador y de la máquina
  → Botón Atacar
  → Log de turnos y HP actualizado
  → Ganador
  → Guardar historial

[Al cerrar]
  → Persistencia en JSON
[Al abrir]
  → Carga automática
```

---

## Rúbrica de evaluación

**P3 = CE3.1 (50%) + CE3.2 (50%)**

### CE3.1 — Interfaz gráfica y organización (50%)

| Nivel | Descriptor |
|---|---|
| Excelente (5.0) | Construye una interfaz funcional, organizada, coherente y correctamente estructurada mediante clases y componentes visuales. |
| Sobresaliente (4.6–4.9) | Construye una interfaz funcional y bien organizada, con detalles menores por mejorar. |
| Bueno (4.0–4.5) | Desarrolla una interfaz funcional que cumple los principales requisitos de organización y distribución. |
| Aceptable (3.0–3.9) | Desarrolla una interfaz parcialmente funcional, con dificultades de organización o distribución. |
| No aceptable (1.0–2.9) | La interfaz no es funcional o no cumple los requerimientos mínimos. |

### CE3.2 — Eventos e integración (50%)

| Nivel | Descriptor |
|---|---|
| Excelente (5.0) | Integra correctamente eventos, interfaz y lógica de negocio, manteniendo una estructura orientada a objetos clara y funcional. |
| Sobresaliente (4.6–4.9) | Integra adecuadamente los componentes con errores mínimos que no afectan el funcionamiento general. |
| Bueno (4.0–4.5) | Logra una integración funcional entre interfaz, eventos y lógica de negocio. |
| Aceptable (3.0–3.9) | Integra parcialmente los elementos, con fallos de funcionamiento o estructura. |
| No aceptable (1.0–2.9) | No logra integrar correctamente interfaz, eventos y lógica orientada a objetos. |

---

## Checklist de autoevaluación

- [ ] Ejecuta con `python3 main.py` sin errores.
- [ ] Hay al menos 3 vistas navegables.
- [ ] CRUD completo de dos entidades relacionadas.
- [ ] Las vistas no contienen reglas de negocio.
- [ ] La lógica está en modelos y servicios.
- [ ] Se usa `ttk` y un estilo consistente.
- [ ] Hay validación visual con mensajes claros.
- [ ] Se confirma antes de eliminar.
- [ ] Los datos persisten en JSON y se cargan al iniciar.
- [ ] Un JSON corrupto no cierra la aplicación.
- [ ] Hay log visible de la acción de dominio.
- [ ] El README incluye wireframe, arquitectura y capturas.
- [ ] El video muestra el flujo completo.
- [ ] Todos los integrantes pueden explicar cualquier capa.

---

## Preguntas de sustentación

1. ¿Dónde vive la regla “el HP no puede ser negativo” y por qué no está en el botón?
2. ¿Cómo se comunican la vista y el servicio? ¿Qué pasa si cambias Tkinter por otra librería?
3. ¿Qué clase se encarga de guardar en JSON? ¿Por qué no lo hace la vista?
4. ¿Qué evento usaste con `bind` y en qué se diferencia de `command`?
5. ¿Qué pasa si el archivo JSON no existe o está corrupto?
6. ¿Cómo agregarías una nueva entidad sin romper lo existente?
7. ¿Qué parte del proyecto todavía tiene demasiadas responsabilidades?

---

## Política de entrega

- Entrega en la fecha indicada; se revisa avance y versión final.
- Un proyecto que no ejecuta obtiene como máximo **3.0**.
- Trabajo copiado entre equipos: **0 automático**.
- La sustentación es obligatoria. Todos los integrantes deben poder explicar cualquier parte del código.
