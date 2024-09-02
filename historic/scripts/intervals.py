from datetime import timedelta
import json
import os
import pandas as pd
from urllib.request import urlopen
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get driver_number and session_key for ingestion drivers table
sessions = pd.read_json('historic/data/sessions.json')
sessions = sessions[sessions["session_name"] == "Race"]
sessions["date_start"] = pd.to_datetime(sessions["date_start"])
sessions["date_end"] = pd.to_datetime(sessions["date_end"])


def fetch_interval_chunk(session_key, start, end):
    starttime = start.strftime('%Y-%m-%dT%H:%M:%S')
    endtime = end.strftime('%Y-%m-%dT%H:%M:%S')
    url = f"https://api.openf1.org/v1/intervals?session_key={session_key}&date>={starttime}&date<{endtime}"
    print(url)
    try:
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except Exception as e:
        print(f"Error fetching data for {session_key} from {starttime} to {endtime}: {e}")
        return None

def process_session_interval(session_key, start_date, end_date):

    start = start_date
    end = start + timedelta(minutes=30)
    interval_list = []


    while end <= end_date:
        data = fetch_interval_chunk(session_key, start, end)
        if data:  # Check if data is not None or empty
            interval_list.append(data)
        start = end
        end = start + timedelta(minutes=30)
        time.sleep(0.25)


    if interval_list:
        json_file_path = f"historic/data/intervals/interval_{session_key}.json"
        with open(json_file_path, 'w') as outfile:
            json.dump(interval_list, outfile)

        # Concatenate and return the collected data as a DataFrame
        return pd.concat([pd.DataFrame(d) for d in interval_list], ignore_index=True)
    else:
        print(f"No data collected for session_key {session_key}.")
        return pd.DataFrame()

start_time = time.time()
for session_key, start_date, end_date in zip(sessions.session_key, sessions.date_start, sessions.date_end):
    result_df = process_session_interval(session_key, start_date, end_date)
    if not result_df.empty:
        print(f"Data collected for session_key {session_key}: {result_df.shape[0]} rows.")
    else:
        print(f"No data collected for session_key {session_key}.")
end_time = time.time()
operation_time = end_time - start_time

# Combining All JSONS

interval_data = pd.DataFrame()
path = "historic/data/intervals"
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.json'):
            dosya_yolu = os.path.join(root, file)
            with open(dosya_yolu, 'r', encoding='utf-8') as file:
                data = json.load(file)
            flattened_data = [interval_values for sublist in data for interval_values in sublist]
            interval_data = pd.concat([interval_data, pd.DataFrame(flattened_data)], ignore_index=True)
            interval_data.to_json("historic/data/interval.json", orient="records")


# Check

interval_data.shape