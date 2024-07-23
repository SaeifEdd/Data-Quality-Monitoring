import sys
import os
from datetime import date, datetime, timedelta
import requests
import pandas as pd
from init import create_app
import numpy as np
from fastapi.responses import JSONResponse

# use local api to extract data
def get_data_api(business_date, hour):
    year, month, day = business_date.year, business_date.month, business_date.day
    local_url = (
        f"http://127.0.0.1:8000/?year={year}&month={month}&day={day}&hour={hour}"
    )
    try:
        response = requests.get(local_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the response as JSON
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse JSON response")
    return None


# a dictionnary of stores
store_dict = create_app()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
        try:
            business_date = date(year, month, day)
            hour = 10
        except ValueError:
            print("date is incorrect")
    else:
        business_date = date(2024, 5, 15)
        hour = 10

    # create data dictionary for each month
    monthly_stores_data = {}
    start_date = business_date
    now_date = date.today()

    current_date = start_date
    while current_date <= now_date:
        month = current_date.month
        if month not in monthly_stores_data.keys():
            monthly_stores_data[month] = {
                "date": [],
                "hour": [],
                "store_id": [],
                "sensor_id": [],
                "nb_visitors": [],
                "unit": [],
            }
            # data = get_data_api(current_date, hour)
            for hour in range(24):
                for store, val in store_dict.items():
                    sensors_traffics = val.get_sensors_hourly_traffic(
                        current_date, hour
                    )
                    for i in sensors_traffics:
                        monthly_stores_data[month]["date"].append(current_date)
                        monthly_stores_data[month]["hour"].append(hour)
                        monthly_stores_data[month]["store_id"].append(store)
                        monthly_stores_data[month]["sensor_id"].append(i)
                        monthly_stores_data[month]["nb_visitors"].append(
                            sensors_traffics[i]
                        )
                        monthly_stores_data[month]["unit"].append(val.sensors[i].unit)
        else:
            for hour in range(24):
                for store, val in store_dict.items():
                    sensors_traffics = val.get_sensors_hourly_traffic(
                        current_date, hour
                    )
                    for i in sensors_traffics:
                        monthly_stores_data[month]["date"].append(current_date)
                        monthly_stores_data[month]["hour"].append(hour)
                        monthly_stores_data[month]["store_id"].append(store)
                        monthly_stores_data[month]["sensor_id"].append(i)
                        monthly_stores_data[month]["nb_visitors"].append(
                            sensors_traffics[i]
                        )
                        monthly_stores_data[month]["unit"].append(val.sensors[i].unit)

        current_date += timedelta(days=1)

    directory = "data/raw"
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    for month, data in monthly_stores_data.items():
        df = pd.DataFrame(data)
        false_data_perc = len(df) // 20
        change_indices = np.random.choice(df.index, size=false_data_perc, replace=False)
        # Set 'sensor_id' to None and 'unit' to 'nonsense_unit' using numpy
        df.loc[change_indices, "sensor_id"] = None
        df.loc[change_indices, "unit"] = "kg"

        csv_filename = f"data/raw/store_data_{month}.csv"
        df.to_csv(csv_filename, index=False)
