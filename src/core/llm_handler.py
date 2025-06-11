import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class LLMHandler:
    def __init__(self, model_name="gpt-4o-mini"):
        # Obtener la API key de las variables de entorno
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno.")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name

    def get_completion(self, system_prompt: str, user_prompt: str, temperature: float = 0.7):
        """
        Obtiene una respuesta del modelo de lenguaje.

        Args:
            system_prompt (str): Rol e instrucciones para el LLM.
            user_prompt (str): La pregunta o solicitud del usuario.
            temperature (float): Controla la creatividad de la respuesta (0.0 a 1.0).

        Returns:
            str: La respuesta generada por el LLM.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error al obtener la respuesta del LLM: {e}")
            return "Lo siento, hubo un error al procesar tu solicitud."

# Ejemplo de uso (puedes ejecutar este archivo directamente para probar el handler)
if __name__ == "__main__":
    llm_handler = LLMHandler()

    system_persona = "Eres un asistente de IA experto en operaciones de hotelería de lujo."
    user_question = "¿Cuáles son las 3 claves para una experiencia de check-in excepcional?"

    print(f"Pregunta del GM: {user_question}")
    response = llm_handler.get_completion(system_persona, user_question, temperature=0.5)
    print(f"Respuesta del Copiloto:\n{response}")