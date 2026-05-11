## 🧠 Sistema Experto Determinístico Basado en Reglas

En este trabajo se desarrolló un sistema experto basado en reglas orientado a la identificación preliminar de dos enfermedades: dengue y COVID-19. El sistema permite ingresar síntomas de un paciente y, a partir de un conjunto de reglas previamente definidas, determina si existe una mayor probabilidad de que el paciente presente dengue, COVID-19 o si el diagnóstico resulta indeterminado.

### Objetivo

El objetivo principal fue diseñar e implementar un sistema experto capaz de simular el razonamiento básico de un profesional de la salud mediante reglas de inferencia.

El sistema busca:

- Recibir síntomas ingresados por el usuario
- Analizar la combinación de síntomas presentes
- Aplicar reglas predefinidas
- Determinar una posible clasificación:
  - Posible dengue
  - Posible COVID-19
  - Diagnóstico indeterminado


### Tipo de sistema

El proyecto se clasifica como un sistema experto basado en reglas.

En este caso, el conocimiento médico se representa mediante reglas del tipo:

**SI condición → ENTONCES conclusión**

Por ejemplo:

* Si el paciente presenta fiebre alta, dolor muscular y dolor detrás de los ojos → posible dengue
* Si presenta fiebre, tos y pérdida del olfato → posible COVID-19

Estas reglas permiten que el sistema tome decisiones sin necesidad de aprendizaje automático, redes neuronales o modelos probabilísticos complejos.


### 🧩 Componentes del sistema experto

### 1️⃣ Base de Conocimiento
La base de conocimiento está compuesta por el conjunto de síntomas relevantes y las reglas médicas utilizadas para inferir una posible enfermedad.
Estas reglas, a las que llamamos *reglas de producción* fueron construidas considerando síntomas característicos de dengue y COVID-19, especialmente aquellos que permiten diferenciarlos en una primera evaluación.

Cada regla contiene:
* identificador
* nombre
* condiciones
* acción
* pesos de certeza
* prioridad
* conclusión inferida.


### 2️⃣ Memoria de Trabajo

Contiene toda la información que el sistema conoce temporalmente durante una evaluación clínica.
La memoria de trabajo almacena:
- síntomas seleccionados
- antecedentes
- factores epidemiológicos
- contexto geográfico
- antecedentes

que fueron ingresados por el usuario desde la interfaz.
   
Ejemplo:

fiebre = True
tos = True
dolor_garganta = True

Cada dato ingresado por el usuario desde la interfaz se transforma internamente en hechos lógicos booleanos.

### 3️⃣ Motor de Inferencia

Es el núcleo lógico del sistema, el cual se encarga de:
 - recorrer las reglas
 - evaluar condiciones
 - disparar reglas válidas
 - acumular evidencias
 - generar conclusiones.

El motor toma hechos (desde la memoria de trabajo) y los compara contra las reglas (desde la base de conocimiento).

### Estrategias de Inferencia Utilizadas
El sistema utiliza la estrategia de encadenamiento hacia adelante (Forward Chaining).
En este método de inferencia, el razonamiento comienza a partir de hechos iniciales presentes en la memoria de trabajo y luego el motor analiza qué reglas poseen condiciones compatibles con dichos hechos y, cuando las condiciones se cumplen, la regla se dispara generando nuevas inferencias.
El flujo lógico implementado puede representarse de la siguiente forma:

                                                  HECHOS → REGLAS → INFERENCIAS → CONCLUSIONES

El sistema implementa implícitamente mecanismos clásicos de inferencia lógica, como por ejemplo ***Modus Ponens***  → uando las condiciones son verdaderas en la memoria de trabajo, el motor activa la conclusión correspondiente.

### Sistema de Prioridades y Acumulación de Evidencia
Cada regla posee además:
 - una prioridad
 - valores de impacto o certeza.

Las prioridades permiten establecer diferentes niveles de relevancia clínica o epidemiológica.
Por ejemplo, definimos distintas reglas que poseen mayor prioridad debido a su importancia diagnóstica, como ser:

✅ sangrado espontáneo
✅ dificultad respiratoria
✅ brotes epidemiológicos


Además, el sistema implementa acumulación heurística de evidencia mediante puntajes asociados a Dengue y COVID-19.Estos valores permiten reforzar la sospecha diagnóstica a medida que múltiples reglas se activan simultáneamente.

## Representación visual del conocimiento
Como complemento explicativo, se incorporó un sistema de visualización de inferencias mediante grafos interactivos.
Para esto utilizamos un módulo de Python denominado Pyvis, el cual nos permitió desarrollar grafos interactivos para representar:

 - hechos
 - reglas
- conclusiones
- relaciones de inferencia

Estos grafos permiten visualizar el flujo de razonamiento del motor de inferencia y cómo múltiples hechos pueden activar diferentes reglas y conclusiones

## Tecnologías utilizadas

Para el desarrollo del sistema se utilizaron las siguientes herramientas:

* Python como lenguaje principal
* Streamlit para la construcción de la interfaz interactiva
* Pyvis para la visualización de grafos
* Programación basada en reglas condicionales
* Lógica booleana para la inferencia de resultados
* GitHub para el control de versiones y almacenamiento del proyecto


## Posibles mejoras futuras

Como mejoras futuras del sistema se podrían incorporar:

* Más síntomas clínicos y niveles de gravedad
* Interfaz gráfica más amigable para el usuario
* Base de datos de pacientes e historial clínico
* Recomendaciones iniciales según el posible diagnóstico
* Integración con sistemas médicos reales

Estas mejoras permitirían transformar el proyecto en una herramienta más robusta y aplicable a contextos reales.


## Conclusión

El desarrollo de este sistema experto permitió aplicar conceptos fundamentales de inteligencia artificial relacionados con representación del conocimiento, motores de inferencia y toma de decisiones basada en reglas.

Se logró construir una herramienta funcional capaz de analizar síntomas y emitir una clasificación preliminar entre dengue, COVID-19 o un resultado indeterminado, simulando el razonamiento básico de un experto humano.

En conclusión, este proyecto representa una implementación simple pero efectiva de un sistema experto orientado al apoyo en diagnósticos preliminares.
