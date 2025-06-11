import streamlit as st
from src.core.llm_handler import LLMHandler
import json
import os
import pandas as pd # Para un posible uso futuro de datos estructurados

class SalesActivatorAgent:
    def __init__(self, llm_handler: LLMHandler):
        self.llm_handler = llm_handler
        self.data_file = "data/processed/enriched_companies.json"
        self._ensure_data_file_exists()

        self.system_prompt_enrich = (
            "Eres un experto en inteligencia de mercado y ventas de hospitalidad de lujo, "
            "especializado en el segmento MICE (Meetings, Incentives, Conferences, Exhibitions). "
            "Tu tarea es analizar la información de una empresa y enriquecerla con detalles clave "
            "relevantes para una propuesta de hotel de lujo. Proporciona la información en formato JSON. "
            "Identifica el segmento de la industria, contactos clave, necesidades potenciales y un punto de dolor."
        )

        self.system_prompt_sequence = (
            "Eres un redactor experto en secuencias de correos electrónicos de ventas para hoteles de lujo, "
            "dirigidas a empresas del segmento MICE. Crea una secuencia de 3 emails persuasivos y profesionales. "
            "Cada email debe tener un propósito claro (ej: Introducción, Valor, Llamada a la Acción/Seguimiento). "
            "Adapta el tono a la sofisticación de un hotel de lujo y sé conciso. "
            "Usa el nombre de la empresa, su punto de dolor y sus necesidades potenciales para personalizar. "
            "No incluyas corchetes para placeholders (e.g. [Nombre Empresa], en su lugar, integra la información directamente). "
            "El output debe ser texto plano."
        )

    def _ensure_data_file_exists(self):
        """Asegura que el archivo JSON de datos exista y sea válido."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f) # Crea un archivo JSON vacío con una lista

    def _load_data(self):
        """Carga los datos de empresas."""
        self._ensure_data_file_exists()
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data):
        """Guarda los datos de empresas."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def enrich_company_data(self, company_name: str, website: str = ""):
        """
        Enriquece la información de una empresa usando el LLM.
        """
        user_prompt = (
            f"Analiza la empresa '{company_name}'. "
            f"Sitio web (si disponible): {website if website else 'No proporcionado'}. "
            "Genera un JSON con los siguientes campos, evita listas dentro de listas, usa español: "
            "{'name': 'Nombre de la empresa', 'industry_segment': 'Ej: Tech MICE, Pharma Incentives', "
            "'key_contacts': 'Ej: Head of HR, Event Manager', 'potential_needs': 'Ej: Espacios grandes, catering vegano, actividades de team-building', "
            "'pain_point': 'Ej: Dificultad para encontrar venues con servicio personalizado, falta de flexibilidad'}"
        )
        
        json_output = self.llm_handler.get_completion(
            system_prompt=self.system_prompt_enrich,
            user_prompt=user_prompt,
            temperature=0.3 # Menor temperatura para datos estructurados
        )
        try:
            # A veces el LLM puede añadir texto antes o después del JSON. Buscamos el JSON.
            json_start = json_output.find('{')
            json_end = json_output.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                clean_json_output = json_output[json_start:json_end]
                enriched_data = json.loads(clean_json_output)
                return enriched_data
            else:
                print(f"Advertencia: No se encontró un JSON válido en la respuesta: {json_output}")
                return None
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON del LLM: {e}. Respuesta: {json_output}")
            return None

    def generate_outbound_sequences(self, company_data: dict):
        """
        Genera secuencias de correo electrónico de outbound usando el LLM.
        """
        user_prompt = (
            f"Para la empresa '{company_data['name']}', que opera en el segmento '{company_data['industry_segment']}', "
            f"con potenciales necesidades como '{company_data['potential_needs']}' y un punto de dolor como '{company_data['pain_point']}', "
            "genera una secuencia de 3 correos electrónicos de ventas. "
            "Email 1: Introducción y captación de interés. "
            "Email 2: Profundización en valor y solución de punto de dolor. "
            "Email 3: Llamada a la acción clara y seguimiento. "
            "Asegúrate de que cada email sea profesional, conciso y adapte el tono de un hotel de lujo."
        )

        sequences = self.llm_handler.get_completion(
            system_prompt=self.system_prompt_sequence,
            user_prompt=user_prompt,
            temperature=0.7 # Mayor temperatura para creatividad en el texto
        )
        return sequences

    def process_new_company(self, company_name: str, website: str = ""):
        """
        Procesa una nueva empresa de principio a fin.
        """
        current_companies = self._load_data()
        
        # Verificar si la empresa ya existe
        if any(c['name'].lower() == company_name.lower() for c in current_companies):
            return False, f"La empresa '{company_name}' ya ha sido procesada."

        # Paso 1: Enriquecer datos
        st.info(f"Enriqueciendo datos para {company_name}...")
        enriched_data = self.enrich_company_data(company_name, website)
        
        if not enriched_data:
            return False, f"Fallo al enriquecer datos para {company_name}. Revisa la respuesta del LLM."

        enriched_data['status'] = "Datos Enriquecidos"
        enriched_data['website'] = website # Añadir el website al JSON
        
        # Paso 2: Generar secuencias de outbound
        st.info(f"Generando secuencias de contacto para {company_name}...")
        outbound_sequences = self.generate_outbound_sequences(enriched_data)
        
        enriched_data['outbound_sequences_generated'] = outbound_sequences # Versión acortada para tabla
        enriched_data['outbound_sequences_full'] = outbound_sequences # Versión completa para detalle
        enriched_data['status'] = "Secuencias Generadas"

        # Añadir al listado y guardar
        current_companies.append(enriched_data)
        self._save_data(current_companies)

        return True, f"Agente SalesActivator ha procesado exitosamente a '{company_name}'."

