from fastapi import APIRouter
from models.sensor_data import SensorData
from datetime import datetime
import joblib
import os
from sklearn.ensemble import ExtraTreesRegressor
import json
import pandas as pd
router = APIRouter()

def default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

class Predictor:
    def __init__(self, model_path):
        self.model_path = "regresors/modelo_entrenado_corriente.joblib"

    def predict(self, data):
        try:
            # Cargar el modelo desde la ruta completa
            model = joblib.load(self.model_path)
            data_df = pd.DataFrame(data, columns=['i_f_cuadrado', 'humedad','temperatura'])

            # Realizar predicciones usando el modelo
            predictions = model.predict(data_df)

            # Crear un DataFrame con las predicciones
            result_df = pd.DataFrame({'Predicciones': predictions})

            # Mostrar el DataFrame con las predicciones
            print(result_df)
            return predictions
        except Exception as e:
            print(f"Error al realizar predicciones: {e}")

            import traceback
            traceback.print_exc()



script_directory = os.path.dirname(os.path.abspath(__file__))




@router.post("/sensor-data/", tags=["EnergyService"])
async def receive_sensor_data(data: SensorData):
    model_path = os.path.join(script_directory, "regresors", "regresors/modelo_entrenado_corriente.joblib")
    # Convert the Pydantic model to a dictionary
    data_dict = data.dict()
    data_array = [data_dict['current']**2, data_dict['temperature'], data_dict['humidity']]
    predictor = Predictor(model_path)
    ipredict=predictor.predict([data_array])
    #print(data_array)
    #print(ipredict)
    print("corriente (A) =",ipredict.tolist()[0])
    # Use the custom default function for serialization
    print(json.dumps(data_dict, indent=4, default=default_converter))
    return {"message": "Data received successfully!"}

@router.get("/", tags=["ConnectionTest"])
async def test_connection():
    return {"message": "Connection successful!"}
