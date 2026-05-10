En este trabajo se desarrolló un sistema experto basado en reglas orientado a la identificación preliminar de dos enfermedades: dengue y COVID-19. El sistema permite ingresar síntomas de un paciente y, a partir de un conjunto de reglas previamente definidas, determina si existe una mayor probabilidad de que el paciente presente dengue, COVID-19 o si el diagnóstico resulta indeterminado.


El objetivo principal fue diseñar e implementar un sistema experto capaz de simular el razonamiento básico de un profesional de la salud mediante reglas de inferencia.

El sistema busca:

* Recibir síntomas ingresados por el usuario
* Analizar la combinación de síntomas presentes
* Aplicar reglas predefinidas
* Determinar una posible clasificación:

  * Posible dengue
  * Posible COVID-19
  * Diagnóstico indeterminado


**-Tipo de sistema inteligente**

El proyecto se clasifica como un sistema experto basado en reglas.

En este caso, el conocimiento médico se representa mediante reglas del tipo:

**SI condición → ENTONCES conclusión**

Por ejemplo:

* Si el paciente presenta fiebre alta, dolor muscular y dolor detrás de los ojos → posible dengue
* Si presenta fiebre, tos y pérdida del olfato → posible COVID-19

Estas reglas permiten que el sistema tome decisiones sin necesidad de aprendizaje automático, redes neuronales o modelos probabilísticos complejos.


**-Tecnologías utilizadas**

Para el desarrollo del sistema se utilizaron las siguientes herramientas:

* Python como lenguaje principal
* Streamlit para la construcción de la interfaz interactiva
* Programación basada en reglas condicionales
* Lógica booleana para la inferencia de resultados
* GitHub para el control de versiones y almacenamiento del proyecto

**-Funcionamiento del sistema**

El sistema funciona a partir del ingreso manual de síntomas por parte del usuario.

Entre los síntomas evaluados se encuentran:

* Fiebre
* Tos
* Dolor muscular
* Dolor de cabeza
* Dolor detrás de los ojos
* Pérdida del olfato
* Dificultad respiratoria
* Cansancio general

Una vez ingresados los síntomas, el sistema analiza las combinaciones posibles y aplica las reglas previamente establecidas.

Ejemplo de reglas implementadas

* Si hay fiebre + dolor muscular + dolor detrás de los ojos → posible dengue
* Si hay fiebre + tos + pérdida del olfato → posible COVID-19
* Si existen síntomas compartidos entre ambas enfermedades o no hay coincidencia clara → diagnóstico indeterminado

Finalmente, el sistema devuelve al usuario el diagnóstico preliminar más probable.


**-Base de conocimiento**

La base de conocimiento está compuesta por el conjunto de síntomas relevantes y las reglas médicas utilizadas para inferir una posible enfermedad.

Estas reglas fueron construidas considerando síntomas característicos de dengue y COVID-19, especialmente aquellos que permiten diferenciarlos en una primera evaluación.



**-Posibles mejoras futuras**

Como mejoras futuras del sistema se podrían incorporar:

* Más síntomas clínicos y niveles de gravedad
* Interfaz gráfica más amigable para el usuario
* Base de datos de pacientes e historial clínico
* Recomendaciones iniciales según el posible diagnóstico
* Integración con sistemas médicos reales

Estas mejoras permitirían transformar el proyecto en una herramienta más robusta y aplicable a contextos reales.


**-Conclusión**

El desarrollo de este sistema experto permitió aplicar conceptos fundamentales de inteligencia artificial relacionados con representación del conocimiento, motores de inferencia y toma de decisiones basada en reglas.

Se logró construir una herramienta funcional capaz de analizar síntomas y emitir una clasificación preliminar entre dengue, COVID-19 o un resultado indeterminado, simulando el razonamiento básico de un experto humano.

En conclusión, este proyecto representa una implementación simple pero efectiva de un sistema experto orientado al apoyo en diagnósticos preliminares.
