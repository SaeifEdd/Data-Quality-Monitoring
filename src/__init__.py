from src.sensor import SensorVisitors
from datetime import date


def create_sensor():
    perc_mal = 0.1
    perc_break = 0.06

    sensor = SensorVisitors(1500, 500, perc_mal=perc_mal, perc_break=perc_break)
    return sensor
