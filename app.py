from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import date
from src.sensor import SensorVisitors
from src import create_sensor

asensor = create_sensor()
app = FastAPI()


@app.get("/")
def sensor_visitors(year: int, month: int, day: int, hour: int) -> JSONResponse:
    business_date = date(year, month, day)
    visits_number = asensor.get_exact_visits(business_date, hour)
    return JSONResponse(status_code=200, content=visits_number)
