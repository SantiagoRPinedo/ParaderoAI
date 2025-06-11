import streamlit as st
from src.core.llm_handler import LLMHandler
from src.copilot.gm_copilot import GMCopilot

# Configuración de la página de Streamlit
st.set_page_config(page_title="Paradero AI - Copiloto para GM", layout="centered")

# --- Inicialización ---
# Inicializar LLMHandler y GMCopilot solo una vez para evitar múltiples instancias
# st.session_state permite mantener el estado de la aplicación entre recargas
if "llm_handler" not in st.session_state:
    try:
        st.session_state.llm_handler = LLMHandler(model_name="gpt-4o") # Puedes probar gpt-4o para un rendimiento más rápido
    except ValueError as e:
        st.error(f"Error de configuración: {e}. Asegúrate de que OPENAI_API_KEY esté en tu archivo .env")
        st.stop() # Detiene la ejecución si no hay API key

if "gm_copilot" not in st.session_state:
    st.session_state.gm_copilot = GMCopilot(st.session_state.llm_handler)

# --- Interfaz de Usuario ---
st.title("👨‍💼 Paradero AI - Copiloto Inteligente para Gerentes Generales")
st.markdown("Tu aliado estratégico para optimizar las operaciones de hotelería de lujo.")

st.write("Escribe tu pregunta o situación para recibir una recomendación experta de Paradero AI.")

# Entrada de texto para la pregunta del GM
user_question = st.text_area("Tu pregunta para el Copiloto:", height=100, placeholder="Ej: ¿Cómo podemos reducir la rotación del personal de limpieza?")

# Botón para enviar la pregunta
if st.button("Obtener Recomendación"):
    if user_question:
        with st.spinner("Paradero AI está pensando..."):
            recommendation, suggested_action = st.session_state.gm_copilot.get_recommendation(user_question)
        
        st.subheader("💡 Recomendación de Paradero AI:")
        st.write(recommendation)

        if suggested_action:
            st.markdown(f"---")
            st.subheader("🚀 Acción Sugerida (Capa de Ejecución):")
            st.info(f"👉 {suggested_action}")
            st.write("Considera desplegar este agente para automatizar o facilitar la acción.")
    else:
        st.warning("Por favor, escribe tu pregunta antes de obtener una recomendación.")

st.markdown("---")
st.caption("Desarrollado por Paradero AI - La Pila de Inteligencia Vertical para la Hospitalidad de Lujo.")