/* ============================================================
   Datos del curso — Programación Orientada a Objetos con Python
   Constantes solamente. La lógica vive en landing.js.
   ============================================================ */

const COURSE = {
  title: 'Programación Orientada a Objetos',
  language: 'Python',
  weeks: 16,
  units: 3,
  projects: 3,
  start: 'Semana 1',
  end: 'Semana 16',
  description: 'Curso práctico de 16 semanas: construye videojuegos, simuladores y aplicaciones de escritorio mientras aprendes POO, herencia, polimorfismo e interfaces gráficas con Python.',
  stack: [
    'Python 3.12',
    'Visual Studio Code',
    'Tkinter + ttk',
    'Git + GitHub',
    'EVA / LMS',
    'JSON / SQLite opcional'
  ]
};

const UNITS = [
  {
    id: 'u1',
    num: 1,
    title: 'Fundamentos de POO en Python',
    short: 'Fundamentos',
    color: 'cyan',
    weeksLabel: 'Semanas 1–5',
    desc: 'Del primer objeto a una clase completamente encapsulada. Clases, atributos, métodos, constructores, propiedades y validaciones.',
    result: 'RA1 · Construye clases y objetos con atributos, métodos, constructores y encapsulamiento.',
    tags: ['Clases', 'Objetos', 'Atributos', 'Constructores', 'Encapsulamiento'],
    weeks: [
      {
        num: 1,
        dir: 'unidad-01-fundamentos-poo/semana-01-introduccion-curso-python',
        doc: 'semana-01.md',
        title: 'Introducción al curso y a Python',
        desc: 'Entorno de trabajo, qué es la POO, Git y primer objeto.',
        tags: ['Python', 'VS Code', 'venv', 'Git', 'Objetos']
      },
      {
        num: 2,
        dir: 'unidad-01-fundamentos-poo/semana-02-metodologias-paradigmas',
        doc: 'semana-02.md',
        title: 'Metodologías y paradigmas',
        desc: 'Paradigmas de programación, POO vs procedural, UML y ciclo de desarrollo.',
        tags: ['Paradigmas', 'POO', 'UML', 'Metodología']
      },
      {
        num: 3,
        dir: 'unidad-01-fundamentos-poo/semana-03-clases-objetos-atributos',
        doc: 'semana-03.md',
        title: 'Clases, objetos y atributos',
        desc: 'Definir clases, crear instancias y distinguir atributos de clase e instancia.',
        tags: ['class', '__init__', 'self', 'Atributos']
      },
      {
        num: 4,
        dir: 'unidad-01-fundamentos-poo/semana-04-metodos-constructores-encapsulamiento',
        doc: 'semana-04.md',
        title: 'Métodos, constructores y encapsulamiento',
        desc: 'Métodos de instancia, classmethod, staticmethod, properties y validaciones.',
        tags: ['Métodos', 'Constructores', '@property', 'Validación']
      }
    ]
  },
  {
    id: 'u2',
    num: 2,
    title: 'Relaciones, herencia y polimorfismo',
    short: 'Relaciones y herencia',
    color: 'blue',
    weeksLabel: 'Semanas 6–11',
    desc: 'Modela sistemas con varias clases: asociación, agregación, composición, jerarquías, clases abstractas y polimorfismo.',
    result: 'RA2 · Implementa soluciones con relaciones entre clases, herencia, clases abstractas, contratos y polimorfismo.',
    tags: ['Asociación', 'Agregación', 'Composición', 'Herencia', 'ABC', 'Polimorfismo'],
    weeks: [
      {
        num: 6,
        dir: 'unidad-02-relaciones-herencia-polimorfismo/semana-06-relaciones-clases',
        doc: 'semana-06.md',
        title: 'Relaciones entre clases',
        desc: 'Asociación, dependencia, multiplicidad y diagramas UML.',
        tags: ['Asociación', 'Dependencia', 'UML', 'Multiplicidad']
      },
      {
        num: 7,
        dir: 'unidad-02-relaciones-herencia-polimorfismo/semana-07-agregacion-composicion',
        doc: 'semana-07.md',
        title: 'Agregación y composición',
        desc: 'Relaciones todo-parte, ciclos de vida y cuándo usar cada una.',
        tags: ['Agregación', 'Composición', 'Todo-parte']
      },
      {
        num: 8,
        dir: 'unidad-02-relaciones-herencia-polimorfismo/semana-08-herencia',
        doc: 'semana-08.md',
        title: 'Herencia',
        desc: 'super(), sobrescritura, MRO y herencia múltiple.',
        tags: ['Herencia', 'super()', 'MRO', 'Override']
      },
      {
        num: 9,
        dir: 'unidad-02-relaciones-herencia-polimorfismo/semana-09-clases-abstractas',
        doc: 'semana-09.md',
        title: 'Clases abstractas',
        desc: 'ABC, métodos abstractos, contratos de comportamiento y Protocol.',
        tags: ['ABC', 'abstractmethod', 'Contratos', 'Protocol']
      },
      {
        num: 10,
        dir: 'unidad-02-relaciones-herencia-polimorfismo/semana-10-polimorfismo',
        doc: 'semana-10.md',
        title: 'Polimorfismo',
        desc: 'Mismo mensaje, distintas respuestas: herencia, duck typing y dunders.',
        tags: ['Polimorfismo', 'Duck typing', 'Dunders', 'singledispatch']
      }
    ]
  },
  {
    id: 'u3',
    num: 3,
    title: 'Interfaces gráficas e integración',
    short: 'GUI e integración',
    color: 'purple',
    weeksLabel: 'Semanas 12–16',
    desc: 'Construye interfaces funcionales con Tkinter, conecta eventos con la lógica de negocio y entrega una aplicación completa por capas.',
    result: 'RA3 · Desarrolla una interfaz gráfica funcional integrada con los principios de la POO.',
    tags: ['Tkinter', 'ttk', 'Layouts', 'Eventos', 'MVC', 'Integración'],
    weeks: [
      {
        num: 12,
        dir: 'unidad-03-gui-integracion/semana-12-arquitectura-gui',
        doc: 'semana-12.md',
        title: 'Arquitectura de GUI',
        desc: 'Ventanas, widgets, pack/grid/place y separación entre interfaz y lógica.',
        tags: ['Tkinter', 'Widgets', 'Layouts', 'MVC']
      },
      {
        num: 13,
        dir: 'unidad-03-gui-integracion/semana-13-componentes-organizacion-visual',
        doc: 'semana-13.md',
        title: 'Componentes y organización visual',
        desc: 'ttk, formularios, estilos, validación visual y prototipos.',
        tags: ['ttk', 'Formularios', 'Estilos', 'Validación']
      },
      {
        num: 14,
        dir: 'unidad-03-gui-integracion/semana-14-eventos-integracion-oo',
        doc: 'semana-14.md',
        title: 'Eventos e integración de una aplicación OO',
        desc: 'Callbacks, command, arena de combate y persistencia JSON.',
        tags: ['Eventos', 'command', 'bind', 'JSON']
      },
      {
        num: 16,
        dir: 'unidad-03-gui-integracion/semana-16-cierre-retroalimentacion',
        doc: 'semana-16.md',
        title: 'Retroalimentación y cierre',
        desc: 'Sustentaciones, code review, portafolio y siguientes pasos.',
        tags: ['Sustentación', 'Code review', 'Portafolio']
      }
    ]
  }
];

const PROJECTS = [
  {
    id: 'p1',
    num: 5,
    unit: 'u1',
    weight: 25,
    title: 'P1 · Creador de personajes RPG',
    desc: 'Aplicación de consola, individual, para crear y gestionar personajes de videojuego con atributos encapsulados y validados.',
    dir: 'unidad-01-fundamentos-poo/proyecto-unidad-01',
    doc: 'README.md',
    tags: ['Consola', 'Clases', 'Encapsulamiento', 'Individual'],
    modality: 'Individual',
    criteria: ['CE1.1', 'CE1.2']
  },
  {
    id: 'p2',
    num: 11,
    unit: 'u2',
    weight: 30,
    title: 'P2 · Arcade de combate por turnos',
    desc: 'Videojuego de consola en equipos: guerrero, mago y arquero se enfrentan por turnos usando herencia, clases abstractas y polimorfismo.',
    dir: 'unidad-02-relaciones-herencia-polimorfismo/proyecto-unidad-02',
    doc: 'README.md',
    tags: ['Consola', 'Herencia', 'ABC', 'Polimorfismo', 'Equipos 2–3'],
    modality: 'Equipos 2–3',
    criteria: ['CE2.1', 'CE2.2']
  },
  {
    id: 'p3',
    num: 15,
    unit: 'u3',
    weight: 45,
    title: 'P3 · Arcade con interfaz gráfica',
    desc: 'Aplicación de escritorio con Tkinter para gestionar personajes e ítems, con CRUD, capas, eventos y persistencia.',
    dir: 'unidad-03-gui-integracion/proyecto-integrador-unidad-03',
    doc: 'README.md',
    tags: ['Tkinter', 'CRUD', 'Capas', 'JSON', 'Equipos 2–3'],
    modality: 'Equipos 2–3',
    criteria: ['CE3.1', 'CE3.2']
  }
];

const FORMATIVE = [
  {
    id: 'u1',
    title: 'Refuerzo Unidad 1',
    desc: '20 ejercicios extra de clases, objetos y encapsulamiento.',
    dir: 'ejercicios-formativos/unidad-01.md',
    tag: 'U1'
  },
  {
    id: 'u2',
    title: 'Refuerzo Unidad 2',
    desc: '20 ejercicios extra de relaciones, herencia y polimorfismo.',
    dir: 'ejercicios-formativos/unidad-02.md',
    tag: 'U2'
  },
  {
    id: 'u3',
    title: 'Refuerzo Unidad 3',
    desc: '15 ejercicios extra de Tkinter e integración.',
    dir: 'ejercicios-formativos/unidad-03.md',
    tag: 'U3'
  }
];

const CRITERIA = [
  { code: 'CE1.1', unit: 'u1', weight: 15, label: 'Clases, objetos y constructores' },
  { code: 'CE1.2', unit: 'u1', weight: 15, label: 'Encapsulamiento y validaciones' },
  { code: 'CE2.1', unit: 'u2', weight: 20, label: 'Relaciones entre clases' },
  { code: 'CE2.2', unit: 'u2', weight: 20, label: 'Abstractas, contratos y polimorfismo' },
  { code: 'CE3.1', unit: 'u3', weight: 15, label: 'Interfaz gráfica y organización' },
  { code: 'CE3.2', unit: 'u3', weight: 15, label: 'Eventos e integración con la lógica' }
];

const RESOURCES = [
  {
    title: 'Documentación oficial de Python',
    desc: 'Referencia del lenguaje en español.',
    url: 'https://docs.python.org/es/3/',
    label: 'docs.python.org'
  },
  {
    title: 'PEP 8 · Guía de estilo',
    desc: 'Convenciones de nombres, indentación y legibilidad.',
    url: 'https://peps.python.org/pep-0008/',
    label: 'peps.python.org'
  },
  {
    title: 'Tkinter · Documentación',
    desc: 'Widgets, geometrías y eventos de la stdlib.',
    url: 'https://docs.python.org/es/3/library/tkinter.html',
    label: 'docs.python.org'
  },
  {
    title: 'Pro Git (español)',
    desc: 'Control de versiones de principio a fin.',
    url: 'https://git-scm.com/book/es/v2',
    label: 'git-scm.com'
  },
  {
    title: 'VS Code + Python',
    desc: 'Configurar editor, intérprete y depuración.',
    url: 'https://code.visualstudio.com/docs/python/python-tutorial',
    label: 'code.visualstudio.com'
  },
  {
    title: 'Real Python · OOP',
    desc: 'Artículos y ejemplos adicionales de POO.',
    url: 'https://realpython.com/python3-object-oriented-programming/',
    label: 'realpython.com'
  }
];
