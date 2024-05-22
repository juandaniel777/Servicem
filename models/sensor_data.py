from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    current: float
    voltage: float
    temperature: float
    humidity: float
    date: datetime