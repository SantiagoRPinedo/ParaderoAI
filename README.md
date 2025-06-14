
# 🏨 Paradero AI  
**Pila de Inteligencia Vertical para Hospitalidad de Lujo**

---

## 🚀 Resumen del Proyecto

Este es un MVP (Producto Mínimo Viable) de **Paradero AI**, un sistema de Inteligencia Artificial diseñado para transformar la operación de hoteles de lujo. Desarrollado en 72 horas, el prototipo demuestra cómo la IA puede **observar, razonar y actuar** de forma más contextual y útil que herramientas SaaS tradicionales.

### 🧠 Componentes clave:
- 🤖 **Copiloto del Gerente General:** Asistente IA conversacional que da recomendaciones estratégicas basadas en el contexto del hotel.
- 📈 **Agente SalesActivator:** Agente autónomo que simula la identificación y contacto de empresas del segmento MICE.

---

## ✨ Características Principales

- **Copiloto Inteligente:** Interfaz (Streamlit) conectada a un LLM (GPT-4o) que ofrece sugerencias personalizadas sobre operaciones, moral del equipo y más.
- **Agente SalesActivator:** Simula procesos de prospección y generación de campañas para el segmento MICE. Datos persistidos localmente en JSON.
- **Dashboard Unificado:** Consolida Copiloto y SalesActivator en una interfaz web amigable.
- **Arquitectura Modular:** Separación clara de lógica, datos y agentes para facilitar escalabilidad.
- **Human-in-the-Loop:** A pesar de ser MVP, permite supervisión humana en decisiones clave.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.9+
- **Interfaz:** Streamlit
- **LLMs:** OpenAI GPT-4o (configurable)
- **Dependencias:** pip + venv
- **Datos:** `pandas`, `json`
- **Variables de entorno:** `python-dotenv`
- **Testing:** `unittest`, `unittest.mock`

---

## 📂 Estructura del Proyecto

```
paradero_ai_project/
├── .venv/                      # Entorno virtual (ignorado por git)
├── src/
│   ├── agents/
│   │   └── sales_activator.py
│   ├── core/
│   │   ├── llm_handler.py
│   │   └── data_ingestion.py
│   ├── copilot/
│   │   └── gm_copilot.py
│   ├── dashboard/
│   │   └── dashboard_app.py
│   └── app.py                  # (opcional)
├── data/
│   ├── raw/
│   │   └── company_leads.csv
│   ├── processed/
│   │   └── enriched_companies.json
│   ├── knowledge_base/
│   │   ├── sop_hospitality_tone.txt
│   │   └── team_morale_templates.json
│   └── test_data/
├── notebooks/
│   └── llm_prompt_testing.ipynb
├── tests/
│   ├── test_gm_copilot.py
│   └── test_sales_activator.py
├── .env                        # Variables de entorno (⚠️ no subir)
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuración y Ejecución

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/paradero_ai_project.git
cd paradero_ai_project
```

### 2. Crear y Activar un Entorno Virtual

```bash
python -m venv .venv
```

- **Windows:**  
  ```bash
  .\.venv\Scripts\activate
  ```
- **macOS/Linux:**  
  ```bash
  source .venv/bin/activate
  ```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY="tu_clave_api_de_openai"
```

⚠️ ¡No subas este archivo a GitHub!

### 5. Poblar Datos Iniciales

Asegúrate de que existan estos archivos:

- `data/processed/enriched_companies.json`
- `data/knowledge_base/sop_hospitality_tone.txt`
- `data/knowledge_base/team_morale_templates.json`

Si no, créalos con datos simulados.

### 6. Ejecutar la Aplicación

```bash
streamlit run src/dashboard/dashboard_app.py
```

Esto abrirá la app web de Paradero AI en `http://localhost:8501`.

---

## 🧪 Pruebas

```bash
python -m unittest tests/test_gm_copilot.py
```

---

## 💡 Próximos Pasos

- 🔌 Integración con APIs reales (PMS, POS, CRM, HRIS)
- 🤖 Nuevos agentes: `PricingAI`, `EnergyPulse`, `CampaignSynth`, etc.
- 🧠 Grounding mejorado con RAG y base vectorial
- 🖥️ UI avanzada: migración a FastAPI + React
- 🕹️ Orquestación de agentes
- 📊 Observabilidad y métricas
- 🐳 Despliegue con Docker/Kubernetes

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte de un desafío técnico.  
¡Cualquier sugerencia, mejora o PR es bienvenida si el proyecto continúa su desarrollo!