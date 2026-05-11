"""
SISTEMA EXPERTO: Detección de Dengue y COVID-19
================================================
Arquitectura: Sistema basado en reglas determinísticas (Forward Chaining)
Enfoque académico: Reglas IF-THEN con certeza y trazabilidad completa
"""

# =====================
# MEMORIA DE TRABAJO
# =====================

class HechosPaciente:
    def __init__(self):
        # --- Síntomas clínicos ---
        self.fiebre = False
        self.fiebre_alta = False
        self.tos = False
        self.tos_seca = False
        self.dolor_garganta = False
        self.dolor_cabeza = False
        self.dolor_muscular = False
        self.dolor_articular = False
        self.dolor_retroorbital = False   # detrás de los ojos 
        self.erupcion_cutanea = False 
        self.nauseas_vomitos = False
        self.perdida_olfato_gusto = False 
        self.dificultad_respiratoria = False
        self.fatiga = False
        self.escalofrios = False
        self.sangrado = False   

        # --- Epidemiología ---
        self.viaje_zona_endemica_dengue = False
        self.contacto_caso_dengue = False
        self.contacto_caso_covid = False
        self.zona_brote_dengue = False
        self.zona_circulacion_covid = False

        # --- Contexto geográfico/temporal ---
        self.residencia_zona_endemica = False 
        self.epoca_verano = False              
        self.prevalencia_dengue_alta = False
        self.prevalencia_covid_activa = False

        # --- Antecedentes/historia clínica del paciente ---
        self.antecedente_asma = False
        self.toma_antihipertensivos = False  
        self.inmunocomprometido = False

# ======================
# BASE DE CONOCIMIENTO 
# ======================

class Regla:
    """Representa una regla IF-THEN del sistema experto."""

    def __init__(self, id, nombre, condicion_fn, condiciones,conclusion, accion, certeza_dengue=0, certeza_covid=0, prioridad=1):
        self.id = id
        self.nombre = nombre
        self.condicion_fn = condicion_fn      # función que evalúa la condición
        self.condiciones = condiciones        # hechos (utilizado para la representacion del grafo de inferencia)
        self.conclusion = conclusion          # utilizado para la representacion del grafo de inferencia
        self.accion = accion                  # descripción de lo que hace la regla
        self.certeza_dengue = certeza_dengue  # delta de certeza para dengue (-100 a +100)
        self.certeza_covid = certeza_covid    # delta de certeza para COVID  (-100 a +100)
        self.prioridad = prioridad             # orden de aplicación


def construir_base_conocimiento():
    """
    Retorna la lista completa de reglas del sistema experto.
    Organizadas por categorías: síntomas, epidemiología, contexto.
    """
    reglas = [

        # ===================================================================
        # GRUPO 1: SÍNTOMAS BÁSICOS COMPARTIDOS
        # (síntomas que pueden ser de ambas enfermedades)
        # ===================================================================

        Regla(
            id="R01",
            nombre="Tríada inicial: fiebre + tos + dolor de garganta",
            condicion_fn=lambda p: p.fiebre and p.tos and p.dolor_garganta,
            condiciones=[
                "Fiebre",
                "Tos",
                "Dolor garganta"
            ],
            conclusion='Sospecha COVID Moderada',
            accion="Se detecta tríada sintomática compatible con infección respiratoria. "
                   "Activa sospecha inicial MODERADA de COVID-19 y BAJA de Dengue.",
            certeza_dengue=+15,
            certeza_covid=+30,
            prioridad=1
        ),

        Regla(
            id="R02",
            nombre="Fiebre alta (>= 39°C)",
            condicion_fn=lambda p: p.fiebre_alta,
            condiciones=["Fiebre Alta"],
            conclusion='Posible Dengue',
            accion="Fiebre alta es más característica de Dengue. Aumenta certeza Dengue.",
            certeza_dengue=+20,
            certeza_covid=+5,
            prioridad=2
        ),

        Regla(
            id="R03",
            nombre="Tos seca persistente",
            condicion_fn=lambda p: p.tos_seca,
            condiciones=["Tos Seca"],
            conclusion='Evidencia Respiratoria COVID',
            accion="Tos seca es síntoma cardinal de COVID-19.",
            certeza_dengue=0,
            certeza_covid=+20,
            prioridad=2
        ),

        # ===================================================================
        # GRUPO 2: SÍNTOMAS ALTAMENTE ESPECÍFICOS
        # ===================================================================

        Regla(
            id="R04",
            nombre="Dolor retroorbital (detrás de los ojos)",
            condicion_fn=lambda p: p.dolor_retroorbital,
            condiciones=["Dolor Retroorbital"],
            conclusion='Dengue Compatible',
            accion="El dolor retroorbital es patognomónico del Dengue. Alta especificidad.",
            certeza_dengue=+35,
            certeza_covid=-10,
            prioridad=2
        ),

        Regla(
            id="R05",
            nombre="Erupción cutánea (rash)",
            condicion_fn=lambda p: p.erupcion_cutanea,
            condiciones=["Erupción Cutánea"],
            conclusion='Dengue Clínico Compatible',
            accion="El exantema (rash) es un signo muy específico de Dengue.",
            certeza_dengue=+30,
            certeza_covid=-5,
            prioridad=2
        ),

        Regla(
            id="R06",
            nombre="Pérdida de olfato y/o gusto (anosmia/ageusia)",
            condicion_fn=lambda p: p.perdida_olfato_gusto,
            condiciones=["Pérdida Olfato/Gusto"],
            conclusion='COVID Altamente Compatible',
            accion="Anosmia/ageusia es síntoma altamente específico de COVID-19.",
            certeza_dengue=-15,
            certeza_covid=+40,
            prioridad=2
        ),

        Regla(
            id="R07",
            nombre="Dolor muscular y articular intenso",
            condicion_fn=lambda p: p.dolor_muscular and p.dolor_articular,
            condiciones=["Dolor Muscular",
                        "Dolor Articular"],
            conclusion='Dengue Sintomático',
            accion="La combinación de mialgia + artralgia intensa es característica del "
                   "Dengue (conocido como 'fiebre rompehuesos').",
            certeza_dengue=+25,
            certeza_covid=+5,
            prioridad=2
        ),

        Regla(
            id="R08",
            nombre="Dificultad respiratoria",
            condicion_fn=lambda p: p.dificultad_respiratoria,
            condiciones=["Dificultad Respiratoria"],
            conclusion='COVID con Compromiso Respiratorio',
            accion="Dificultad respiratoria sugiere compromiso pulmonar, más frecuente en COVID-19.",
            certeza_dengue=0,
            certeza_covid=+25,
            prioridad=2
        ),

        Regla(
            id="R09",
            nombre="Signos de alarma: sangrado espontáneo",
            condicion_fn=lambda p: p.sangrado,
            condiciones=["Sangrado Espontáneo"],
            conclusion='Dengue Grave',
            accion="ALERTA: sangrado espontáneo puede indicar Dengue grave/hemorrágico.",
            certeza_dengue=+40,
            certeza_covid=-10,
            prioridad=1  # alta prioridad
        ),

        # ===================================================================
        # GRUPO 3: EPIDEMIOLOGÍA 
        # ===================================================================

        Regla(
            id="R10",
            nombre="Viaje reciente a zona endémica de Dengue",
            condicion_fn=lambda p: p.viaje_zona_endemica_dengue,
            condiciones=["Viaje Zona Endémica"],
            conclusion='Riesgo Epidemiológico Dengue',
            accion="Antecedente de viaje a zona endémica de Dengue (Brasil): "
                   "incrementa significativamente la probabilidad de Dengue.",
            certeza_dengue=+30,
            certeza_covid=-10,
            prioridad=1
        ),

        Regla(
            id="R11",
            nombre="Contacto directo con caso confirmado de Dengue",
            condicion_fn=lambda p: p.contacto_caso_dengue,
            condiciones=["Contacto Caso Dengue"],
            conclusion='Exposición Confirmada Dengue',
            accion="Contacto con familiar con Dengue confirmado: indica exposición "
                   "al vector Aedes aegypti en mismo entorno.",
            certeza_dengue=+25,
            certeza_covid=-5,
            prioridad=1
        ),

        Regla(
            id="R12",
            nombre="Contacto con caso confirmado de COVID-19",
            condicion_fn=lambda p: p.contacto_caso_covid,
            condiciones=["Contacto Caso COVID"],
            conclusion='Exposición Confirmada COVID',
            accion="Contacto estrecho con caso COVID-19 confirmado: "
                   "incrementa probabilidad de COVID-19.",
            certeza_dengue=-10,
            certeza_covid=+30,
            prioridad=1
        ),

        # ===================================================================
        # GRUPO 4: CONTEXTO GEOGRÁFICO Y EPIDEMIOLÓGICO REGIONAL
        # ===================================================================

        Regla(
            id="R13",
            nombre="Residencia en zona endémica de Dengue (Corrientes)",
            condicion_fn=lambda p: p.residencia_zona_endemica,
            condiciones=["Residencia Zona Endémica"],
            conclusion='Contexto Endémico Dengue',
            accion="Corrientes, Argentina es zona endémica de Dengue. "
                   "La prevalencia basal aumenta la probabilidad prior de Dengue.",
            certeza_dengue=+20,
            certeza_covid=0,
            prioridad=2
        ),

        Regla(
            id="R14",
            nombre="Prevalencia alta de Dengue en la región (época de verano)",
            condicion_fn=lambda p: p.prevalencia_dengue_alta and p.epoca_verano,
            condiciones=["Alta Prevalencia Dengue",
                        "Época Verano"],
            conclusion='Alta Circulación Dengue',
            accion="Alta prevalencia de Dengue en verano correntino: "
                   "factor epidemiológico que refuerza la sospecha.",
            certeza_dengue=+20,
            certeza_covid=-5,
            prioridad=2
        ),

        Regla(
            id="R15",
            nombre="Brote activo de Dengue en zona cercana",
            condicion_fn=lambda p: p.zona_brote_dengue,
            condiciones=["Brote Activo Dengue"],
            conclusion='Brote Activo Dengue',
            accion="Brote reciente de Dengue en área cercana al centro de emergencias: "
                   "incremento adicional en la certeza de Dengue.",
            certeza_dengue=+25,
            certeza_covid=-5,
            prioridad=1
        ),

        Regla(
            id="R16",
            nombre="COVID-19 circulando activamente en la región",
            condicion_fn=lambda p: p.prevalencia_covid_activa,
            condiciones=["Circulación COVID Regionall"],
            conclusion='Circulación COVID Regional',
            accion="COVID-19 con circulación activa regional: "
                   "mantiene sospecha de COVID como diagnóstico diferencial.",
            certeza_dengue=0,
            certeza_covid=+15,
            prioridad=2
        ),

        # ===================================================================
        # GRUPO 5: ANTECEDENTES 
        # ===================================================================

        Regla(
            id="R17",
            nombre="Antecedente de asma",
            condicion_fn=lambda p: p.antecedente_asma,
            condiciones=["Antecedente Asma"],
            conclusion='Riesgo COVID Elevado',
            accion="El asma es factor de riesgo para COVID-19 grave. "
                   "No diferencia diagnóstico pero aumenta relevancia clínica de COVID.",
            certeza_dengue=0,
            certeza_covid=+10,
            prioridad=3
        ),

        Regla(
            id="R18",
            nombre="Uso de antihipertensivos (IECA/ARA2)",
            condicion_fn=lambda p: p.toma_antihipertensivos,
            condiciones=["Uso Antihipertensivos"],
            conclusion='Riesgo COVID Asociado',
            accion="Los IECA/ARA2 interactúan con el receptor ACE2, vía de entrada "
                   "del SARS-CoV-2. Relevante para riesgo de COVID grave.",
            certeza_dengue=0,
            certeza_covid=+8,
            prioridad=3
        ),

        # ===================================================================
        # GRUPO 6: REGLAS COMBINADAS (encadenamiento hacia adelante)
        # ===================================================================

        Regla(
            id="R19",
            nombre="Perfil epidemiológico completo de Dengue",
            condicion_fn=lambda p: (p.viaje_zona_endemica_dengue and
                                     p.contacto_caso_dengue and
                                     p.residencia_zona_endemica),
            condiciones=["Viaje Zona Endémica",
                        "Contacto Caso Dengue",
                        "Residencia Zona Endémica"],
            conclusion='Perfil Epidemiológico Completo Dengue',
            accion="COMBINACIÓN CRÍTICA: viaje + contacto + residencia endémica. "
                   "El paciente reúne el perfil epidemiológico completo de Dengue. "
                   "Se aplica refuerzo adicional por encadenamiento de evidencias.",
            certeza_dengue=+20,
            certeza_covid=-15,
            prioridad=1
        ),

        Regla(
            id="R20",
            nombre="Coinfección: síntomas compartidos en contexto de doble circulación",
            condicion_fn=lambda p: (p.prevalencia_dengue_alta and
                                     p.prevalencia_covid_activa and
                                     p.fiebre and p.tos),
            condiciones=["Alta Prevalencia Dengue",
                        "Circulación COVID Regional",
                        "Fiebre",
                        "Tos"],
            conclusion='Sospecha Diferencial Mixta',
            accion="En contexto de doble circulación activa, los síntomas compartidos "
                   "(fiebre + tos) no descartan ninguna enfermedad. "
                   "Se mantiene sospecha diferencial hasta confirmar con laboratorio.",
            certeza_dengue=+5,
            certeza_covid=+5,
            prioridad=3
        ),
    ]

    return sorted(reglas, key=lambda r: r.prioridad)


# ========================
# MOTOR DE INFERENCIA 
# ========================

class MotorInferencia:
    """
    Implementa encadenamiento hacia adelante (Forward Chaining).
    Evalúa todas las reglas contra los hechos del paciente y acumula certeza.
    """

    CERTEZA_INICIAL_DENGUE = 5   # certeza base (prior epidemiológico)
    CERTEZA_INICIAL_COVID  = 5   # certeza base
    CERTEZA_MAX = 100
    CERTEZA_MIN = 0

    def __init__(self):
        self.reglas = construir_base_conocimiento()
        self.reglas_disparadas = []
        self.certeza_dengue = self.CERTEZA_INICIAL_DENGUE
        self.certeza_covid  = self.CERTEZA_INICIAL_COVID
        self.traza = []   # explicabilidad: registro de cada paso

    def ejecutar(self, hechos: HechosPaciente):
        """
        Ciclo de inferencia principal.
        Aplica todas las reglas que se satisfacen y actualiza certezas.
        """
        self.traza = []
        self.certeza_dengue = self.CERTEZA_INICIAL_DENGUE
        self.certeza_covid  = self.CERTEZA_INICIAL_COVID
        self.reglas_disparadas = []

        self.traza.append({
            "paso": 0,
            "tipo": "INICIO",
            "descripcion": "Motor de inferencia iniciado. "
                           f"Certeza inicial — Dengue: {self.certeza_dengue}% | COVID: {self.certeza_covid}%",
            "certeza_dengue": self.certeza_dengue,
            "certeza_covid": self.certeza_covid,
        })

        # Ciclo de disparo de reglas (agenda-based forward chaining)
        for regla in self.reglas:
            if regla.condicion_fn(hechos):
                self.reglas_disparadas.append(regla)

                # Actualizar certezas (con límites)
                self.certeza_dengue = max(self.CERTEZA_MIN,
                                          min(self.CERTEZA_MAX,
                                              self.certeza_dengue + regla.certeza_dengue))
                self.certeza_covid  = max(self.CERTEZA_MIN,
                                          min(self.CERTEZA_MAX,
                                              self.certeza_covid  + regla.certeza_covid))

                self.traza.append({
                    "paso": len(self.traza),
                    "tipo": "REGLA_DISPARADA",
                    "regla_id": regla.id,
                    "regla_nombre": regla.nombre,
                    "descripcion": regla.accion,
                    "delta_dengue": regla.certeza_dengue,
                    "delta_covid": regla.certeza_covid,
                    "certeza_dengue": self.certeza_dengue,
                    "certeza_covid": self.certeza_covid,
                })

        # Conclusión
        diagnostico = self._clasificar()
        self.traza.append({
            "paso": len(self.traza),
            "tipo": "CONCLUSION",
            "descripcion": f"Clasificación final: {diagnostico}. "
                           f"Certeza Dengue: {self.certeza_dengue}% | "
                           f"Certeza COVID: {self.certeza_covid}%",
            "certeza_dengue": self.certeza_dengue,
            "certeza_covid": self.certeza_covid,
        })

        return diagnostico

    def _clasificar(self):
        """Determina la clasificación final según umbral de certeza."""
        d = self.certeza_dengue
        c = self.certeza_covid

        if d >= 70 and d > c * 1.5:
            return "SOSPECHA ALTA DE DENGUE"
        elif c >= 70 and c > d * 1.5:
            return "SOSPECHA ALTA DE COVID-19"
        elif d >= 50 and d > c:
            return "SOSPECHA MODERADA DE DENGUE (No se descarta que pueda tratarse de COVID)"
        elif c >= 50 and c > d:
            return "SOSPECHA MODERADA DE COVID-19 (No se descarta que pueda tratarse de Dengue)"
        elif d >= 40 or c >= 40:
            return "DIAGNÓSTICO DIFERENCIAL: DENGUE / COVID-19 — Requiere laboratorio"
        else:
            return "EVIDENCIA INSUFICIENTE — Requiere evaluación clínica adicional"
