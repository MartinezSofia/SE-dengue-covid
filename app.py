import streamlit as st
from motor import HechosPaciente, MotorInferencia, construir_base_conocimiento
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

def generar_grafo_regla_pyvis(regla):

    net = Network(
        height="400px",
        width="100%",
        bgcolor="#FFFFFF",
        font_color="black",
        directed=True
    )

    net.set_options("""
        var options = {

        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "LR",
                "sortMethod": "directed",
                "nodeSpacing": 140,
                "levelSeparation": 220
            }
        },

        "physics": {
            "enabled": false
        },

        "interaction": {
            "zoomView": true,
            "dragView": true
        }
        }
        """)

    # =========================
    # HECHOS (condiciones)
    # =========================
    for condicion in regla.condiciones:
        net.add_node(
            condicion,
            label=condicion,
            color="#5DADE2",
            shape="dot",
            size=18,
            level=0
        )

    # =========================
    # REGLA
    # =========================
    net.add_node(
        regla.id,
        label=regla.id,
        color="#F7DC6F",
        shape="box",
        size=20,
        title=regla.nombre,
        level=1
    )

    # =========================
    # CONCLUSIÓN
    # =========================
    net.add_node(
        regla.conclusion,
        label=regla.conclusion,
        color="#58D68D",
        shape="diamond",
        size=22,
        level=2
    )

    # =========================
    # CONEXIONES
    # =========================
    for condicion in regla.condiciones:
        net.add_edge(condicion, regla.id)

    net.add_edge(regla.id, regla.conclusion)

    # =========================
    # EXPORTAR
    # =========================
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:

        net.save_graph(tmp_file.name)

        with open(tmp_file.name, "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = html_content.replace(
            "</script>",
            """
            network.once("afterDrawing", function () {
                network.fit({
                    animation: {
                        duration: 800,
                        easingFunction: "easeInOutQuad"
                    }
                });
            });
            </script>
            """
        )

    with open(tmp_file.name, "w", encoding="utf-8") as f:
        f.write(html_content)

    return tmp_file.name


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

st.set_page_config(
    page_title="Sistema Experto Dengue/COVID",
    page_icon="🩺",
    layout="wide"
)

# ==========================================================
# TÍTULO PRINCIPAL
# ==========================================================

st.title("🩺 Sistema Experto de Apoyo Diagnóstico")
st.subheader("Detección de Dengue y COVID-19")

st.divider()

# ==========================================================
# SIDEBAR - DATOS DEL PACIENTE
# ==========================================================

st.sidebar.title("🧾 Datos del Paciente")

hechos = HechosPaciente()

# ==========================================================
# SÍNTOMAS CLÍNICOS
# ==========================================================

with st.sidebar.expander("🩺 Síntomas Clínicos", expanded=True):

    #fiebre y su subtipo
    hechos.fiebre = st.checkbox("Fiebre")
    hechos.fiebre_alta = False

    if hechos.fiebre:

        tipo_fiebre = st.radio(
            "Tipo de fiebre",
            [
                "Leve",
                "Moderada",
                "Alta"
            ],
            horizontal=True
        )

        hechos.fiebre_alta = tipo_fiebre == "Alta"
    #hechos.fiebre = st.checkbox("Fiebre")
    #hechos.fiebre_alta = st.checkbox("Fiebre alta (≥39°C)")
    hechos.tos = st.checkbox("Tos")
    hechos.tos_seca = False

    if hechos.tos:

        tipo_tos = st.radio(
            "Tipo de tos",
            [
                "Seca",
                "Productiva"
            ],
            horizontal=True
        )

        hechos.tos_seca = tipo_tos == "Seca"
    #hechos.tos = st.checkbox("Tos")
    #hechos.tos_seca = st.checkbox("Tos seca")
    hechos.dolor_garganta = st.checkbox("Dolor de garganta")
    hechos.dolor_cabeza = st.checkbox("Dolor de cabeza")
    hechos.dolor_muscular = st.checkbox("Dolor muscular")
    hechos.dolor_articular = st.checkbox("Dolor articular")
    hechos.dolor_retroorbital = st.checkbox("Dolor retroorbital")
    hechos.erupcion_cutanea = st.checkbox("Erupción cutánea / rash")
    hechos.perdida_olfato_gusto = st.checkbox("Pérdida de olfato/gusto")
    hechos.nauseas_vomitos = st.checkbox("Náuseas o vómitos")
    hechos.dificultad_respiratoria = st.checkbox("Dificultad respiratoria")
    hechos.fatiga = st.checkbox("Fatiga intensa")
    hechos.sangrado = st.checkbox("Sangrado espontáneo")

# ==========================================================
# EPIDEMIOLOGÍA
# ==========================================================

with st.sidebar.expander("🌎 Epidemiología", expanded=False):

    hechos.viaje_zona_endemica_dengue = st.checkbox(
        "Viaje a zona endémica de Dengue"
    )

    hechos.contacto_caso_dengue = st.checkbox(
        "Contacto con caso confirmado de Dengue"
    )

    hechos.contacto_caso_covid = st.checkbox(
        "Contacto con caso confirmado de COVID-19"
    )

# ==========================================================
# CONTEXTO REGIONAL
# ==========================================================

with st.sidebar.expander("📍 Contexto Regional", expanded=False):

    hechos.residencia_zona_endemica = st.checkbox(
        "Residencia en zona endémica"
    )

    hechos.zona_brote_dengue = st.checkbox(
        "Brote activo de Dengue"
    )

    hechos.prevalencia_dengue_alta = st.checkbox(
        "Alta prevalencia de Dengue"
    )

    hechos.epoca_verano = st.checkbox(
        "Época de verano"
    )

    hechos.prevalencia_covid_activa = st.checkbox(
        "Circulación activa de COVID-19"
    )

# ==========================================================
# ANTECEDENTES
# ==========================================================

with st.sidebar.expander("🧬 Antecedentes", expanded=False):

    hechos.antecedente_asma = st.checkbox(
        "Antecedente de asma"
    )

    hechos.toma_antihipertensivos = st.checkbox(
        "Uso de antihipertensivos"
    )

    hechos.inmunocomprometido = st.checkbox(
        "Paciente inmunocomprometido"
    )

# ==========================================================
# BOTÓN DE ANÁLISIS
# ==========================================================

analizar = st.sidebar.button(
    "🔍 Analizar Paciente",
    use_container_width=True
)

# ==========================================================
# INFORMACIÓN DEL SISTEMA
# ==========================================================

with st.sidebar.expander("ℹ️ Información del Sistema"):

    st.write("""
Este sistema utiliza reglas clínicas y epidemiológicas
para analizar síntomas compatibles con Dengue y COVID-19.
""")

    st.write(f"""
📚 Reglas cargadas: {len(construir_base_conocimiento())}
""")

    ver_reglas = st.checkbox("📋 Ver reglas disponibles")

# ==========================================================
# PANTALLA INICIAL
# ==========================================================

if not analizar:

    st.info("""
Complete los datos del paciente en el panel izquierdo
y presione **Analizar Paciente**.
""")

# ==========================================================
# EJECUCIÓN DEL SISTEMA
# ==========================================================

if analizar:

    motor = MotorInferencia()

    with st.spinner("Analizando datos del paciente..."):

        diagnostico = motor.ejecutar(hechos)

    # ======================================================
    # RESULTADOS PRINCIPALES
    # ======================================================

    st.header("📈 Resultado del Análisis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🦟 Probabilidad Dengue",
            f"{motor.certeza_dengue}%"
        )

        st.progress(motor.certeza_dengue / 100)

    with col2:

        st.metric(
            "🦠 Probabilidad COVID-19",
            f"{motor.certeza_covid}%"
        )

        st.progress(motor.certeza_covid / 100)

    st.divider()

    # ======================================================
    # DIAGNÓSTICO FINAL
    # ======================================================

    if "DENGUE" in diagnostico.upper():

        st.warning(f"📌 {diagnostico}")

    elif "COVID" in diagnostico.upper():

        st.info(f"📌 {diagnostico}")

    else:

        st.error(f"📌 {diagnostico}")

    # ======================================================
    # RESUMEN DEL ANÁLISIS
    # ======================================================

    st.subheader("📊 Resumen del Análisis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📚 Total de reglas",
            len(construir_base_conocimiento())
        )

    with col2:

        st.metric(
            "⚡ Reglas aplicadas",
            len(motor.reglas_disparadas)
        )

    # ======================================================
    # DETALLE DEL ANÁLISIS
    # ======================================================

    with st.expander("📑 Ver detalle completo del análisis"):

        reglas_ordenadas = sorted(
            motor.reglas_disparadas,
            key=lambda r: int(r.id.replace("R", ""))
        )

        for regla in reglas_ordenadas:

            with st.expander(f"{regla.id} — {regla.nombre}"):

                # DESCRIPCIÓN
                st.write(regla.accion)

                # IMPACTOS
                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Impacto Dengue",
                        regla.certeza_dengue
                    )

                with col2:

                    st.metric(
                        "Impacto COVID",
                        regla.certeza_covid
                    )

                # EVENTOS RELACIONADOS A LA REGLA
                eventos_regla = [
                    e for e in motor.traza
                    if e["tipo"] == "REGLA_DISPARADA"
                    and e["regla_id"] == regla.id
                ]

                # MOSTRAR ACUMULADOS
                for evento in eventos_regla:

                    st.write(
                        f"🦟 Acumulado Dengue: {evento['certeza_dengue']}%"
                    )

                    st.write(
                        f"🦠 Acumulado COVID-19: {evento['certeza_covid']}%"
                    )

# ==========================================================
# REGLAS DISPONIBLES DEL SISTEMA
# ==========================================================

if ver_reglas:

    st.divider()

    st.header("📚 Reglas Disponibles del Sistema")

    st.caption("""
Estas son las reglas clínicas y epidemiológicas
que el sistema utiliza para razonar.
""")

    reglas = construir_base_conocimiento()

    # ORDEN CORRECTO R01 -> R20
    reglas_ordenadas = sorted(
        reglas,
        key=lambda r: int(r.id.replace("R", ""))
    )

    for r in reglas_ordenadas:

        with st.expander(f"{r.id} — {r.nombre}"):

            st.markdown(f"""
    ### {r.id} — {r.nombre}

    - Impacto Dengue: **{r.certeza_dengue}**
    - Impacto COVID: **{r.certeza_covid}**
    - Prioridad: **{r.prioridad}**
    """)

            st.divider()

            st.subheader("🔗 Grafo de Inferencia")

            archivo_html = generar_grafo_regla_pyvis(r)

            with open(archivo_html, "r", encoding="utf-8") as f:
                html_content = f.read()

            col1, col2, col3 = st.columns([1, 3, 1])

            with col2:
                components.html(html_content, height=600, scrolling=False)
            

