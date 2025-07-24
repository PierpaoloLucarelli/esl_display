import os
from datetime import datetime, timedelta

import pytz
import requests
from dotenv import load_dotenv

load_dotenv()
amsterdam_tz = pytz.timezone("Europe/Amsterdam")
ORIGIN_PLACE_ID = os.getenv("ORIGIN_PLACE_ID")
DESTINATION_PLACE_ID = os.getenv("DESTINATION_PLACE_ID")
API_KEY = os.getenv("GCP_DIRECTIONS_API")


def get_next_trams(n: int, start_date: datetime):
    next_trams = []
    for i in range(n):
        _dep_time = start_date + timedelta(minutes=i * 10)
        dep_time = int(_dep_time.timestamp())

        URL = (
            f"https://maps.googleapis.com/maps/api/directions/json"
            f"?destination={DESTINATION_PLACE_ID}"
            f"&mode=transit"
            f"&departure_time={dep_time}"
            f"&origin={ORIGIN_PLACE_ID}"
            f"&key={API_KEY}"
        )

        response = requests.get(URL).json()
        steps = response["routes"][0]["legs"][0]["steps"]
        if len(steps) == 1 or len(steps) != 3:  # Only walking option, too late bro
            continue

        leave_time = response["routes"][0]["legs"][0]["departure_time"]["value"]
        leave_time = datetime.utcfromtimestamp(leave_time)
        leave_time = leave_time.replace(tzinfo=pytz.utc).astimezone(amsterdam_tz)

        tram_step = steps[1]

        if tram_step["travel_mode"] != "TRANSIT":
            continue

        tram_time = tram_step["transit_details"]["departure_time"]["value"]
        tram_time = datetime.utcfromtimestamp(tram_time)
        amsterdam_time = tram_time.replace(tzinfo=pytz.utc).astimezone(amsterdam_tz)

        tram_number = tram_step["transit_details"]["line"]["short_name"]

        next_trams.append({"dep": amsterdam_time, "leave": leave_time, "num": tram_number})
    return next_trams


if __name__ == "__main__":
    next_trams = get_next_trams(3)
