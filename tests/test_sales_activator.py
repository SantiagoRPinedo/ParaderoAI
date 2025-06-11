import json

if __name__ == "__main__":
     # Prueba de uso del agente (solo para probar el módulo)
     from src.core.llm_handler import LLMHandler
     from src.agents.sales_activator import SalesActivatorAgent
     
     llm_h = LLMHandler()
     sales_agent = SalesActivatorAgent(llm_h)

     print("Probando el agente SalesActivator...")
     success, message = sales_agent.process_new_company("Empresa de Eventos Corporativos", "www.eventoscorp.com")
     print(message)
     if success:
         data = sales_agent._load_data()
         print(json.dumps(data, indent=4, ensure_ascii=False))