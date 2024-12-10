import os
from datetime import datetime, timedelta

import pytz
import requests
from dotenv import load_dotenv

load_dotenv()
start_date = datetime(2024, 12, 11, 7, 0, 0)
amsterdam_tz = pytz.timezone("Europe/Amsterdam")
ORIGIN_PLACE_ID="place_id:ChIJZ2xEayaxxUcRs0sDQXPFhnc"
DESTINATION_PLACE_ID="place_id:ChIJq6qamBe3xUcRcE_U3hgSZ1M"
API_KEY = os.getenv("GCP_DIRECTIONS_API")

def get_next_trams(n: int):
    next_trams = []
    for i in range(n):
        _dep_time = start_date + timedelta(minutes=i*10)
        dep_time = int(_dep_time.timestamp())

        URL = f"https://maps.googleapis.com/maps/api/directions/json" \
              f"?destination={DESTINATION_PLACE_ID}" \
              f"&mode=transit" \
              f"&departure_time={dep_time}" \
              f"&origin={ORIGIN_PLACE_ID}" \
              f"&key={API_KEY}"

        response = requests.get(URL).json()
        tram_time = response["routes"][0]["legs"][0]["steps"][1]["transit_details"]["departure_time"]["value"]
        tram_time = datetime.utcfromtimestamp(tram_time)
        amsterdam_time = tram_time.replace(tzinfo=pytz.utc).astimezone(amsterdam_tz)

        next_trams.append(amsterdam_time)
    return next_trams


if __name__ == "__main__":
    next_trams = get_next_trams(3)
    print(next_trams)