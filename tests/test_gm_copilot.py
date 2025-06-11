
import unittest
import os
from unittest.mock import MagicMock, patch
import json

# Asegúrate de que Python pueda encontrar tus módulos
# Esto es necesario si ejecutas las pruebas directamente desde la carpeta 'tests'
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.llm_handler import LLMHandler
from src.copilot.gm_copilot import GMCopilot

class TestGMCopilot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Configuración que se ejecuta una vez antes de todas las pruebas de la clase.
        Simula la API Key para que no falle la inicialización de LLMHandler.
        """
        os.environ['OPENAI_API_KEY'] = 'fake_api_key_for_testing'
        # Crear los archivos de conocimiento simulados si no existen
        cls.ensure_knowledge_base_files()

    @classmethod
    def tearDownClass(cls):
        """
        Limpieza que se ejecuta una vez después de todas las pruebas de la clase.
        Elimina la API Key simulada.
        """
        del os.environ['OPENAI_API_KEY']
        # Opcional: limpiar los archivos de conocimiento si los creaste solo para la prueba
        cls.cleanup_knowledge_base_files()

    @classmethod
    def ensure_knowledge_base_files(cls):
        """Crea archivos de conocimiento simulados para las pruebas."""
        os.makedirs('data/knowledge_base', exist_ok=True)
        
        # sop_hospitality_tone.txt
        with open('data/knowledge_base/sop_hospitality_tone.txt', 'w', encoding='utf-8') as f:
            f.write("Principio 1: Siempre la excelencia en el servicio al huésped.\n")
            f.write("Principio 2: Fomentar un ambiente positivo en el equipo.\n")
            f.write("Principio 3: Proactividad en la resolución de problemas.")
        
        # team_morale_templates.json
        with open('data/knowledge_base/team_morale_templates.json', 'w', encoding='utf-8') as f:
            json.dump({
                "general_morale_principles": "Fomentar la comunicación abierta y el reconocimiento.",
                "housekeeping_specific": "Asegurar equipos adecuados y descansos."
            }, f, ensure_ascii=False, indent=4)

    @classmethod
    def cleanup_knowledge_base_files(cls):
        """Elimina los archivos de conocimiento simulados después de las pruebas."""
        # Considera si quieres borrar estos archivos después de cada test o solo al final.
        # Para este ejemplo, los dejamos porque la clase los crea y usa.
        # Si fueras a borrarlos, usarías os.remove()
        pass


    def setUp(self):
        """
        Configuración que se ejecuta antes de cada método de prueba.
        Mockea LLMHandler para controlar sus respuestas.
        """
        # patch.object reemplaza el método 'create' de OpenAI().chat.completions.
        # Es importante simular la respuesta que esperarías de la API de OpenAI.
        self.mock_llm_client = MagicMock()
        
        # Simular la respuesta del LLM para el método create de chat.completions
        # Se necesita un objeto con una estructura específica que OpenAI.completions.create devolvería
        self.mock_llm_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Respuesta simulada del LLM sobre moral. Considera el agente EnergyPulse."))]
        )
        
        # Parchear el método LLMHandler.__init__ para que use nuestro mock client
        # Y también parchear el método get_completion para que retorne directamente lo que queremos.
        # Esto nos da control total sobre la respuesta del LLM.
        with patch('src.core.llm_handler.OpenAI', return_value=self.mock_llm_client):
             self.llm_handler = LLMHandler()
        
        # Aquí, vamos a parchear directamente el método get_completion para simplificar
        # el control de lo que el LLM "respondería" en cada prueba.
        self.llm_handler.get_completion = MagicMock(return_value="Respuesta simulada del LLM.")
        
        self.copilot = GMCopilot(self.llm_handler)

    def test_get_recommendation_basic(self):
        """Prueba que el copiloto genera una recomendación básica."""
        self.llm_handler.get_completion.return_value = "La recomendación es mejorar el flujo de check-in."
        question = "¿Cómo podemos mejorar la experiencia de check-in?"
        recommendation, suggested_action = self.copilot.get_recommendation(question)

        self.assertIn("recomendación", recommendation)
        self.assertIsNone(suggested_action) # No debería sugerir agente para esta pregunta

        # Verifica que el LLMHandler.get_completion fue llamado
        self.llm_handler.get_completion.assert_called_once()
        args, kwargs = self.llm_handler.get_completion.call_args
        self.assertIn("experiencia de check-in", args[1]) # Verifica que la pregunta del usuario fue pasada

    def test_get_recommendation_with_morale_context(self):
        """
        Prueba que el copiloto genera una recomendación con contexto de moral
        y sugiere el agente EnergyPulse.
        """
        self.llm_handler.get_completion.return_value = (
            "Para la moral del equipo de limpieza, recomendamos una reunión de feedback y reconocimiento. "
            "Un chequeo semanal de pulso es crucial."
        )
        question = "¿Qué puedo hacer para mejorar la moral del equipo de limpieza?"
        recommendation, suggested_action = self.copilot.get_recommendation(question)

        self.assertIn("moral del equipo de limpieza", recommendation)
        self.assertIn("EnergyPulse", suggested_action)

        self.llm_handler.get_completion.assert_called_once()
        args, kwargs = self.llm_handler.get_completion.call_args
        # Asegúrate de que el prompt del sistema incluya el contexto relevante de moral
        self.assertIn("Fomentar la comunicación abierta y el reconocimiento", args[0])
        self.assertIn("Asegurar equipos adecuados y descansos", args[0])


    def test_get_recommendation_with_sales_context(self):
        """
        Prueba que el copiloto sugiere el agente SalesActivator para preguntas de ventas.
        """
        self.llm_handler.get_completion.return_value = (
            "Para aumentar los leads MICE, enfócate en campañas dirigidas y personalizadas."
        )
        question = "¿Cómo podemos atraer más clientes MICE?"
        recommendation, suggested_action = self.copilot.get_recommendation(question)

        self.assertIn("clientes MICE", recommendation)
        self.assertIn("SalesActivator", suggested_action)
        self.llm_handler.get_completion.assert_called_once()

    def test_get_recommendation_with_pricing_context(self):
        """
        Prueba que el copiloto sugiere el agente PricingAI para preguntas de precios.
        """
        self.llm_handler.get_completion.return_value = (
            "Considera ajustar dinámicamente las tarifas OTA en función de la demanda estacional."
        )
        question = "¿Deberíamos ajustar nuestros precios para la temporada baja?"
        recommendation, suggested_action = self.copilot.get_recommendation(question)

        self.assertIn("ajustar", recommendation)
        self.assertIn("PricingAI", suggested_action)
        self.llm_handler.get_completion.assert_called_once()

    def test_copilot_loads_sops(self):
        """Verifica que el copiloto carga los SOPs al inicializarse."""
        # Se ejecuta en setUp, pero aquí validamos que se hayan cargado.
        self.assertIsNotNone(self.copilot.sops)
        self.assertIn("excelencia en el servicio", self.copilot.sops)
        self.assertGreater(len(self.copilot.sops), 50) # Asegura que no esté vacío

    def test_copilot_loads_morale_templates(self):
        """Verifica que el copiloto carga las plantillas de moral al inicializarse."""
        self.assertIsNotNone(self.copilot.morale_templates)
        self.assertIn("general_morale_principles", self.copilot.morale_templates)
        self.assertIn("Fomentar la comunicación abierta", self.copilot.morale_templates['general_morale_principles'])


if __name__ == '__main__':
    unittest.main()