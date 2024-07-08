from datetime import date
from sensor import SensorVisitors
from stores import StoreSensor

def create_sensor():
    perc_mal = 0.1
    perc_break = 0.06

    sensor = SensorVisitors(1500, 500, perc_mal=perc_mal, perc_break=perc_break)
    return sensor


def create_app() -> dict:
    """
    Create the available stores in our API
    5 stores, with each 8 sensors
    Each stores has a different number of people coming to it
    As well as different break and malfunction percentages
    (Not realistic, but we keep things simple)
    """

    store_name = ["Sfax", "Sousse", "Tozeur", "Tatouine", "Tunis"]
    store_avg_visit = [3000, 8000, 6000, 2000, 1700]
    store_std_visit = [500, 800, 500, 400, 100]
    perc_malfunction = [0.05, 0.1, 0.08, 0.05, 0.05]
    perc_break = [0.05, 0.08, 0.05, 0.02, 0]

    store_dict = dict()

    for i in range(len(store_name)):
        store_dict[store_name[i]] = StoreSensor(
            store_name[i],
            store_avg_visit[i],
            store_std_visit[i],
            perc_malfunction[i],
            perc_break[i],
        )
    return store_dict
