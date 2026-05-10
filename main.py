"""
SISTEMA EXPERTO: Detección de Dengue / COVID-19
================================================
Punto de entrada principal. Permite:
  1. Ejecutar el caso del enunciado automáticamente
  2. Ingresar un paciente nuevo de forma interactiva
  3. Ver la base de conocimiento completa
"""

from motor import HechosPaciente, MotorInferencia, construir_base_conocimiento


def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     SISTEMA EXPERTO — CLASIFICACIÓN DE PACIENTES             ║
║     Dengue / COVID-19  |  Centro de Emergencias              ║
║     Materia: Inteligencia Artificial                         ║
╚══════════════════════════════════════════════════════════════╝
""")


def ejecutar_caso_enunciado():
    """Ejecuta exactamente el caso del enunciado y muestra la traza completa."""
    print("\n" + "═" * 65)
    print("  CASO CLÍNICO DEL ENUNCIADO")
    print("═" * 65)
    print("""
  Paciente: Masculino, 35 años
  Residencia: Corrientes, Argentina
  Síntomas: Fiebre, tos, dolor de garganta
  Antecedentes: Asma, medicación antihipertensiva
  Epidemiología:
    ✓ Viajó a Brasil hace 2 semanas
    ✓ Contacto con familiar con Dengue confirmado
    ✓ Zona con brote activo de Dengue
    ✓ COVID-19 circulando activamente en la región
    ✓ Alta prevalencia de Dengue (época de verano)
""")
    input("  Presione ENTER para iniciar la inferencia...")

    hechos = HechosPaciente()
    hechos.cargar_caso_enunciado()

    motor = MotorInferencia()
    motor.ejecutar(hechos)

    print("\n" + motor.reporte())


def ingresar_paciente_interactivo():
    """Permite ingresar un nuevo paciente síntoma por síntoma."""
    print("\n  INGRESO DE NUEVO PACIENTE")
    print("  Responda s/n a cada síntoma/dato\n")

    hechos = HechosPaciente()

    def preguntar(texto):
        while True:
            r = input(f"  {texto} (s/n): ").strip().lower()
            if r in ('s', 'si', 'sí', 'y', 'yes'):
                return True
            elif r in ('n', 'no'):
                return False
            print("  → Ingrese 's' o 'n'")

    print("\n  --- SÍNTOMAS CLÍNICOS ---")
    hechos.fiebre               = preguntar("¿Tiene fiebre?")
    if hechos.fiebre:
        hechos.fiebre_alta      = preguntar("  ¿La fiebre es >= 39°C?")
    hechos.tos                  = preguntar("¿Tiene tos?")
    if hechos.tos:
        hechos.tos_seca         = preguntar("  ¿La tos es seca?")
    hechos.dolor_garganta       = preguntar("¿Tiene dolor de garganta?")
    hechos.dolor_cabeza         = preguntar("¿Tiene dolor de cabeza?")
    hechos.dolor_muscular       = preguntar("¿Tiene dolor muscular?")
    hechos.dolor_articular      = preguntar("¿Tiene dolor articular?")
    hechos.dolor_retroorbital   = preguntar("¿Tiene dolor detrás de los ojos?")
    hechos.erupcion_cutanea     = preguntar("¿Tiene erupción en la piel (rash)?")
    hechos.perdida_olfato_gusto = preguntar("¿Tiene pérdida de olfato o gusto?")
    hechos.nauseas_vomitos      = preguntar("¿Tiene náuseas o vómitos?")
    hechos.dificultad_respiratoria = preguntar("¿Tiene dificultad para respirar?")
    hechos.fatiga               = preguntar("¿Tiene fatiga intensa?")
    hechos.sangrado             = preguntar("¿Tiene sangrado espontáneo?")

    print("\n  --- EPIDEMIOLOGÍA ---")
    hechos.viaje_zona_endemica_dengue = preguntar("¿Viajó a zona endémica de Dengue (Brasil, Paraguay, etc.)?")
    hechos.contacto_caso_dengue       = preguntar("¿Tuvo contacto con caso de Dengue?")
    hechos.contacto_caso_covid        = preguntar("¿Tuvo contacto con caso de COVID-19?")

    print("\n  --- CONTEXTO REGIONAL ---")
    hechos.residencia_zona_endemica   = preguntar("¿Reside en zona endémica de Dengue?")
    hechos.zona_brote_dengue          = preguntar("¿Hay brote activo de Dengue en su zona?")
    hechos.prevalencia_dengue_alta    = preguntar("¿La prevalencia de Dengue es alta actualmente?")
    hechos.epoca_verano               = preguntar("¿Es época de verano?")
    hechos.prevalencia_covid_activa   = preguntar("¿Hay circulación activa de COVID-19 en la región?")

    print("\n  --- ANTECEDENTES ---")
    hechos.antecedente_asma           = preguntar("¿Tiene antecedente de asma?")
    hechos.toma_antihipertensivos     = preguntar("¿Toma medicamentos para la presión arterial?")
    hechos.inmunocomprometido         = preguntar("¿Está inmunocomprometido?")

    print("\n  Procesando...")
    motor = MotorInferencia()
    motor.ejecutar(hechos)
    print("\n" + motor.reporte())


def mostrar_base_conocimiento():
    """Muestra todas las reglas del sistema experto."""
    reglas = construir_base_conocimiento()
    print(f"\n  BASE DE CONOCIMIENTO — {len(reglas)} reglas\n")
    print("  {:<5} {:<40} {:>8} {:>8}".format("ID", "Nombre", "Δ Dengue", "Δ COVID"))
    print("  " + "-" * 65)
    for r in reglas:
        d = f"+{r.certeza_dengue}" if r.certeza_dengue >= 0 else str(r.certeza_dengue)
        c = f"+{r.certeza_covid}"  if r.certeza_covid  >= 0 else str(r.certeza_covid)
        print(f"  {r.id:<5} {r.nombre[:40]:<40} {d:>8} {c:>8}")
    print()


def menu_principal():
    mostrar_banner()
    while True:
        print("\n  ¿Qué desea hacer?")
        print("  [1] Ejecutar el caso del enunciado")
        print("  [2] Ingresar un paciente nuevo")
        print("  [3] Ver la base de conocimiento")
        print("  [0] Salir\n")

        opcion = input("  Opción: ").strip()

        if opcion == "1":
            ejecutar_caso_enunciado()
        elif opcion == "2":
            ingresar_paciente_interactivo()
        elif opcion == "3":
            mostrar_base_conocimiento()
        elif opcion == "0":
            print("\n  Sistema cerrado.\n")
            break
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    menu_principal()
