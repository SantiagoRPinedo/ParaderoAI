import streamlit as st
import pandas as pd
import json
import os

# módulos del proyecto
from src.core.llm_handler import LLMHandler
from src.copilot.gm_copilot import GMCopilot
from src.agents.sales_activator import SalesActivatorAgent # Asegúrate de que exista este archivo y clase

# --- Configuración de la página de Streamlit ---
st.set_page_config(page_title="Paradero AI - Centro de Operaciones", layout="wide", initial_sidebar_state="expanded")

# --- Inicialización de Clases (usando st.session_state para mantener el estado) ---
if "llm_handler" not in st.session_state:
    try:
        st.session_state.llm_handler = LLMHandler(model_name="gpt-4o") # Usamos gpt-4o para velocidad
    except ValueError as e:
        st.error(f"Error de configuración: {e}. Asegúrate de que OPENAI_API_KEY esté en tu archivo .env")
        st.stop()

if "gm_copilot" not in st.session_state:
    st.session_state.gm_copilot = GMCopilot(st.session_state.llm_handler)

if "sales_agent" not in st.session_state:
    st.session_state.sales_agent = SalesActivatorAgent(st.session_state.llm_handler)

# --- Funciones Auxiliares para cargar/guardar datos del SalesActivator ---
# Estas funciones simulan una base de datos para el agente
DATA_FILE = "data/processed/enriched_companies.json"

def load_company_data():
    """Carga los datos de empresas enriquecidas desde un archivo JSON."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Retorna una lista vacía si el archivo no existe o está corrupto

def save_company_data(data):
    """Guarda los datos de empresas enriquecidas en un archivo JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True) # Asegura que el directorio exista
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Sidebar para Navegación ---
st.sidebar.title("Menú de Paradero AI")
page_selection = st.sidebar.radio(
    "Navega entre las funcionalidades:",
    ["🤖 Copiloto GM", "📈 Agente SalesActivator", "📊 Vista General"]
)

# --- Contenido Principal del Dashboard ---

if page_selection == "🤖 Copiloto GM":
    st.header("👨‍💼 Copiloto Inteligente para Gerentes Generales")
    st.markdown("Tu aliado estratégico para optimizar las operaciones de hotelería de lujo.")

    gm_question = st.text_area(
        "Tu pregunta para el Copiloto:",
        height=100,
        placeholder="Ej: ¿Cómo podemos mejorar la experiencia de check-in en horas pico?"
    )

    if st.button("Obtener Recomendación del Copiloto"):
        if gm_question:
            with st.spinner("Paradero AI está pensando..."):
                recommendation, suggested_action = st.session_state.gm_copilot.get_recommendation(gm_question)

            st.subheader("💡 Recomendación de Paradero AI:")
            st.write(recommendation)

            if suggested_action:
                st.markdown("---")
                st.subheader("🚀 Acción Sugerida (Capa de Ejecución):")
                st.info(f"👉 {suggested_action}")
                st.write("Considera la posibilidad de que un agente automatizado pueda facilitar esta acción.")
        else:
            st.warning("Por favor, escribe tu pregunta para el Copiloto.")

elif page_selection == "📈 Agente SalesActivator":
    st.header("🎯 Agente SalesActivator - Grupos & MICE")
    st.markdown("Automatiza la identificación, enriquecimiento y generación de contactos para el segmento MICE.")

    st.subheader("1. Identificar/Simular Nuevas Empresas (Individual)")
    # Para el MVP, simularemos la identificación. Podrías pegar un nombre de empresa
    company_name_input = st.text_input("Nombre de la empresa para activar el agente:", placeholder="Ej: Eventos Corporativos SA")
    company_website_input = st.text_input("Sitio web (URL) de la empresa (opcional):", placeholder="Ej: www.eventoscorporativos.com")

    if st.button("Activar Agente para Empresa Individual"):
        if company_name_input:
            with st.spinner(f"Activando SalesActivator para {company_name_input}..."):
                success, message = st.session_state.sales_agent.process_new_company(
                    company_name_input, company_website_input
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
            st.rerun() # Recarga para mostrar los datos actualizados
        else:
            st.warning("Por favor, ingresa el nombre de la empresa.")

    st.subheader("2. Cargar CSV y Enriquecer Múltiples Empresas")
    uploaded_file = st.file_uploader("Sube un archivo CSV con empresas (columnas: 'name', 'website')", type=["csv"])

    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            st.write("Vista previa del CSV cargado:")
            st.dataframe(df_uploaded.head())

            if st.button("Enriquecer Empresas del CSV"):
                # Verificar que las columnas necesarias existan
                if 'name' not in df_uploaded.columns:
                    st.error("El CSV debe contener una columna 'name'.")
                else:
                    companies_to_process = df_uploaded.to_dict(orient='records')
                    total_companies = len(companies_to_process)
                    processed_count = 0
                    
                    st.info(f"Iniciando el enriquecimiento para {total_companies} empresas. Esto puede tardar unos minutos...")

                    # Usar un placeholder para actualizar el progreso
                    progress_text = st.empty()
                    progress_bar = st.progress(0)

                    for i, company_data in enumerate(companies_to_process):
                        company_name = company_data.get('name')
                        company_website = company_data.get('website', '') # 'website' es opcional
                        
                        if company_name:
                            progress_text.text(f"Procesando empresa {i+1}/{total_companies}: {company_name}...")
                            success, message = st.session_state.sales_agent.process_new_company(
                                company_name, company_website
                            )
                            if success:
                                st.success(f"✔️ {company_name}: {message}")
                            else:
                                st.warning(f"⚠️ {company_name}: {message}")
                        else:
                            st.warning(f"Empresa en la fila {i+1} sin nombre, omitiendo.")
                        
                        processed_count += 1
                        progress_bar.progress(processed_count / total_companies)

                    st.success(f"¡Procesamiento de {processed_count} empresas completado!")
                    st.balloons()
                    st.rerun() # Recarga para mostrar los datos actualizados
        except Exception as e:
            st.error(f"Error al leer el CSV o durante el procesamiento: {e}")

    st.subheader("3. Estado de Empresas MICE y Secuencias de Contacto") # El número de subsección ha cambiado a 3.
    # Muestra las empresas procesadas por el agente
    companies = load_company_data()
    if companies:
        df_companies = pd.DataFrame(companies)
        # Seleccionar y reordenar columnas para una mejor vista
        display_columns = [
            "name", "status", "industry_segment", "key_contacts", "potential_needs",
            "pain_point", "outbound_sequences_generated"
        ]
        df_display = df_companies[display_columns].copy()

        # Acortar el contenido de las secuencias para la vista de tabla
        df_display['outbound_sequences_generated'] = df_display['outbound_sequences_generated'].apply(
            lambda x: x[:100] + '...' if len(x) > 100 else x
        )
        
        st.dataframe(df_display, use_container_width=True)

        st.markdown("---")
        st.subheader("Detalle de Secuencias de Contacto")
        selected_company_name = st.selectbox(
            "Selecciona una empresa para ver el detalle de sus secuencias:",
            options=[c['name'] for c in companies]
        )
        if selected_company_name:
            selected_company = next((c for c in companies if c['name'] == selected_company_name), None)
            if selected_company and 'outbound_sequences_full' in selected_company:
                st.text_area(f"Secuencias de Contacto para {selected_company_name}:",
                             value=selected_company['outbound_sequences_full'],
                             height=400)
            else:
                st.info("No hay secuencias de contacto detalladas disponibles para esta empresa.")
    else:
        st.info("Aún no hay empresas procesadas por el Agente SalesActivator.")

elif page_selection == "📊 Vista General":
    st.header("📊 Vista General de Operaciones (Simulado)")
    st.markdown("Un vistazo rápido al rendimiento clave del hotel.")

    # Simular métricas clave
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ocupación Actual", "78%", "↑ 2% vs. mes anterior")
        st.metric("NPS de Huéspedes", "9.2", "↑ 0.1")
    with col2:
        st.metric("Rotación de Personal", "18%", "↓ 3% (últimos 3 meses)")
        st.metric("Revenue F&B (Semanal)", "$15,500", "↑ 10% vs. semana anterior")
    with col3:
        st.metric("Leads MICE Nuevos (Últimos 7 días)", "12", "↑ 4")
        st.metric("Conversión MICE", "5.8%", "↑ 0.5%")

    st.markdown("---")
    st.subheader("Eventos y Alertas Recientes")
    st.info("""
    - **10/06/2025:** El Agente EnergyPulse detectó baja moral en el turno de noche de Cocina. Se sugirió reunión de equipo.
    - **09/06/2025:** Agente PricingAI ajustó tarifas para el 15/07 debido a baja ocupación esperada en fin de semana.
    - **08/06/2025:** Se generaron 3 nuevas secuencias de contacto para empresas MICE por el Agente SalesActivator.
    """)
    st.write("*(Esta sección es un mock, no se actualiza dinámicamente en este MVP)*")