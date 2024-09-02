from datetime import timedelta
import os
import re
import json
import pandas as pd
from urllib.request import urlopen
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


# Get driver_number and session_key for ingestion drivers table
sessions = pd.read_json('historic/data/sessions.json')
sessions["date_start"] = pd.to_datetime(sessions["date_start"])
sessions["date_end"] = pd.to_datetime(sessions["date_end"])
sessions.sort_values("date_start")

## HTTP 500 HATASI SONRASI

num_list = []
path = "historic/data/locations"
for root, dirs, files in os.walk(path):
    for file in files:
        match = re.search(r'_(\d+)\.json$', file)
        if match:
            num = match.group(1)
            num_list.append(int(num))

sessions = sessions[~sessions['session_key'].isin(num_list)]

##

def fetch_location_chunk(session_key, start, end):
    starttime = start.strftime('%Y-%m-%dT%H:%M:%S')
    endtime = end.strftime('%Y-%m-%dT%H:%M:%S')
    url = f"https://api.openf1.org/v1/location?session_key={session_key}&date>={starttime}&date<{endtime}"
    print(url)

    try:
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def process_session_location(session_key, start_date, end_date):
    start = start_date
    end = start + timedelta(seconds=120)
    location_list = []

    while end <= end_date + timedelta(minutes=60):
        data = fetch_location_chunk(session_key, start, end)
        if data:
            location_list.append(data)
        else:
            print(f"No data fetched for session key: {session_key} from {start} to {end}")
        start = end
        end = start + timedelta(seconds=120)
        time.sleep(0.2)

    # Save data as JSON with session_name if data exists
    if location_list:
        with open(f"historic/data/locations/location_{session_key}.json", 'w') as outfile:
            json.dump(location_list, outfile)
        return pd.concat([pd.DataFrame(d) for d in location_list], ignore_index=True)
    else:
        print(f"No data to concatenate for session key: {session_key}")
        return pd.DataFrame()


start_time = time.time()
for session_key, start_date, end_date in zip(sessions.session_key, sessions.date_start, sessions.date_end):
    process_session_location(session_key, end_date, end_date)
end_time = time.time()
operation_time = end_time - start_time



# Combining All JSONS

location = pd.DataFrame()
path = "historic/data/locations"
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.json'):
            dosya_yolu = os.path.join(root, file)
            with open(dosya_yolu, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(dosya_yolu)
            flattened_data = [location_values for sublist in data for location_values in sublist]
            location = pd.concat([location, pd.DataFrame(flattened_data)], ignore_index=True)
            location.to_json("historic/data/location.json", orient="records")
