from urllib.request import urlopen
import json
import pandas as pd
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get meeting_keys for ingestion session table
meetings = pd.read_json('historic/data/meetings.json')

# Getting sessions for each meeting_key:

all_data = []
for i in meetings.meeting_key:
    url = f"https://api.openf1.org/v1/sessions?meeting_key={i}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    all_data.append(data)

flattened_data = [session for sublist in all_data for session in sublist]
sessions = pd.DataFrame(flattened_data)
sessions.to_json("historic/data/sessions.json", orient="records")

