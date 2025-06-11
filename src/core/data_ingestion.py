import pandas as pd
import os

class DataIngestion:
    def __init__(self, base_path="data/raw/"):
        self.base_path = base_path

    def load_simulated_company_leads(self, filename="company_leads.csv"):
        """
        Carga leads de empresas desde un archivo CSV simulado.
        Esto simularía la "Capa de Medición" obteniendo leads.
        """
        filepath = os.path.join(self.base_path, filename)
        try:
            df = pd.read_csv(filepath)
            return df.to_dict(orient='records') # Retorna lista de diccionarios
        except FileNotFoundError:
            print(f"Advertencia: Archivo de leads no encontrado en {filepath}. Creando uno de ejemplo.")
            # Crear un archivo de ejemplo si no existe
            sample_data = {
                'name': ['Global Events Co.', 'Incentive Travel Planners'],
                'website': ['www.globalevents.com', 'www.incentivetravel.com'],
                'direction': ['123 Event Plaza'],
                'status': ['Active', 'UnActive']
            }
            df_sample = pd.DataFrame(sample_data)
            os.makedirs(self.base_path, exist_ok=True)
            df_sample.to_csv(filepath, index=False)
            return df_sample.to_dict(orient='records')
        except Exception as e:
            print(f"Error al cargar datos simulados de leads: {e}")
            return []

    # Puedes añadir más métodos aquí para simular la ingesta de PMS, POS, HRIS, etc.
    def get_simulated_hr_data(self):
        """Simula obtener datos de un sistema HRIS."""
        return {
            "housekeeping_turnover_risk": 0.25, # 25% de riesgo
            "team_sentiment_housekeeping": "low",
            "peer_recognition_frequency": "low"
        }