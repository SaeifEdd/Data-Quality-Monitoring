import sys
from datetime import date, datetime, timedelta
import requests
from src import create_app
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
        business_date = date(2024, 3, 15)
        hour = 10

    start_date = business_date
    now_date = date.today()

    current_date = start_date
    while current_date <= now_date:
        data = get_data_api(current_date, hour)
        if data is not None:
            print(current_date, " : ", data)
        else:
            print("no data found")

        current_date += timedelta(days=1)
