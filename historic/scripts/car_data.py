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

## HTTP 500 HATASI SONRASI

num_list = []
path = "historic/data/car_data"
for root, dirs, files in os.walk(path):
    for file in files:
        match = re.search(r'_(\d+)\.json$', file)
        if match:
            num = match.group(1)
            num_list.append(int(num))

sessions = sessions[~sessions['session_key'].isin(num_list)]

##

def fetch_car_data_chunk(session_key, start, end):
    starttime = start.strftime('%Y-%m-%dT%H:%M:%S')
    endtime = end.strftime('%Y-%m-%dT%H:%M:%S')
    url = f"https://api.openf1.org/v1/car_data?session_key={session_key}&date>={starttime}&date<{endtime}"
    print(url)

    try:
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def process_session_car_data(session_key, start_date, end_date):
    start = start_date
    end = start + timedelta(seconds=120)
    car_data_list = []

    while end <= end_date + timedelta(minutes=60):
        data = fetch_car_data_chunk(session_key, start, end)
        if data:
            car_data_list.append(data)
        else:
            print(f"No data fetched for session key: {session_key} from {start} to {end}")
        start = end
        end = start + timedelta(seconds=120)
        time.sleep(0.2)

    # Save data as JSON with session_name if data exists
    if car_data_list:
        with open(f"historic/data/car_data/car_data_{session_key}.json", 'w') as outfile:
            json.dump(car_data_list, outfile)
        return pd.concat([pd.DataFrame(d) for d in car_data_list], ignore_index=True)
    else:
        print(f"No data to concatenate for session key: {session_key}")
        return pd.DataFrame()


start_time = time.time()
for session_key, start_date, end_date in zip(sessions.session_key, sessions.date_start, sessions.date_end):
    process_session_car_data(session_key, start_date, end_date)
end_time = time.time()
operation_time = end_time - start_time


# Combining All JSONS

start_time = time.time()
car_data = pd.DataFrame()
path = "historic/data/sessions"
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.json'):
            dosya_yolu = os.path.join(root, file)
            with open(dosya_yolu, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(dosya_yolu)
            flattened_data = [car_data_values for sublist in data for car_data_values in sublist]
            car_data = pd.concat([car_data, pd.DataFrame(flattened_data)], ignore_index=True)
            car_data.to_json("historic/data/car_data.json", orient="records")

end_time = time.time()
operation_time = end_time - start_time

