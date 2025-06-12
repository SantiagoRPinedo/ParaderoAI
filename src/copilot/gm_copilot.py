from src.core.llm_handler import LLMHandler
import json

class GMCopilot:
    def __init__(self, llm_handler: LLMHandler):
        self.llm_handler = llm_handler
        self.system_prompt_base = (
            "Eres un copiloto de IA altamente competente para un Gerente General de un hotel de lujo, "
            "Paradero AI. Tu objetivo es proporcionar recomendaciones estratégicas, proactivas y alineadas con la marca, "
            "basadas en las mejores prácticas de la hotelería de lujo y los SOPs de Paradero. "
            "Mantén un tono profesional, conciso y de alto nivel. Siempre prioriza la experiencia del huésped "
            "y la eficiencia operativa. Cuando sea posible, sugiere acciones concretas."
        )
        # Aquí se carga más conocimiento, como plantillas de moral, etc.
        self.sops = self._load_sops_from_file("data/knowledge_base/sop_hospitality_tone.txt")
        self.morale_templates = self._load_json_data("data/knowledge_base/team_morale_templates.json")


    def _load_sops_from_file(self, filepath):
        """Carga los SOPs o el tono de la marca desde un archivo."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Advertencia: Archivo de SOPs no encontrado en {filepath}. El copiloto no tendrá este grounding.")
            return ""

    def _load_json_data(self, filepath):
        """Carga datos JSON desde un archivo."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Advertencia: Archivo JSON no encontrado o corrupto en {filepath}. Omitiendo datos.")
            return {}

    def get_recommendation(self, gm_question: str):
        """
        Genera una recomendación para el GM basada en su pregunta, los SOPs
        y la inteligencia del LLM.
        """
        # lógica simple para "aterrizar" la pregunta
        # con información relevante de tus los SOPs o base de conocimiento (simulando RAG)
        context_info = ""
        if "moral" in gm_question.lower() or "equipo" in gm_question.lower():
            context_info = f"\nConsidera estos principios sobre la moral del equipo de Paradero:\n{self.morale_templates.get('general_morale_principles', '')}"
            if "limpieza" in gm_question.lower():
                context_info += f"\nEspecíficamente para Housekeeping:\n{self.morale_templates.get('housekeeping_specific', '')}"

        # Combina el prompt base con los SOPs y la pregunta del GM
        full_system_prompt = f"{self.system_prompt_base}\n\nSOPs de Paradero y Tono:\n{self.sops}{context_info}"
        
        response_content = self.llm_handler.get_completion(
            system_prompt=full_system_prompt,
            user_prompt=gm_question,
            temperature=0.4 # Menor temperatura para respuestas más directas y menos creativas
        )
        
        # Lógica para sugerir una acción/agente (Bonus)
        suggested_action = self._suggest_agent_action(response_content, gm_question)

        return response_content, suggested_action

    def _suggest_agent_action(self, llm_response: str, original_question: str):
        """
        Analiza la respuesta del LLM y la pregunta original para sugerir una acción o agente.
        Esto es una simulación de la Capa de Ejecución.
        """
        suggestion = None
        response_lower = llm_response.lower()
        question_lower = original_question.lower()

        if "moral" in response_lower or "equipo" in response_lower or "bienestar" in response_lower:
            suggestion = "El agente **EnergyPulse** podría generar plantillas de reuniones de moral o check-ins 1:1."
        elif "ventas" in response_lower or "ocupación" in response_lower or "promoción" in response_lower or "leads" in response_lower:
            suggestion = "El agente **SalesActivator** puede ayudarte a lanzar campañas segmentadas."
        elif "tarifas" in response_lower or "revenue" in response_lower or "precios" in response_lower:
            suggestion = "El agente **PricingAI** puede ajustar las tarifas de OTA en tiempo real."
        elif "marketing" in response_lower or "campañas" in response_lower:
            suggestion = "El agente **CampaignSynth** puede optimizar tu copia de anuncios."
        
        return suggestion