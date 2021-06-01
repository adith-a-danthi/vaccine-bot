import requests
from datetime import datetime

BASE_URL = "https://cdn-api.co-vin.in/api"
CALENDAR_BY_DISTRICT = "/v2/appointment/sessions/public/calendarByDistrict"


def get_slot_details(district_id):
    try:
        today = datetime.now()
        date = today.strftime("%d-%m-%Y")
        r = requests.get(f"{BASE_URL}{CALENDAR_BY_DISTRICT}?district_id={district_id}&date={date}")

        r.raise_for_status()
        response = r.json()
        failed = False
    except requests.HTTPError:
        print(requests.HTTPError)
        response = None
        failed = True
    except requests.ConnectionError:
        print('Connection Error')
        response = None
        failed = True
    return (response, failed)
