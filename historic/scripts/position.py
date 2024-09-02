from urllib.request import urlopen
import json
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get session_key for ingestion session table
sessions = pd.read_json('historic/data/sessions.json')

# Getting sessions for each session_key:

all_data = []
for i in sessions.session_key:
    url = f"https://api.openf1.org/v1/position?session_key={i}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    all_data.append(data)

flattened_data = [position for sublist in all_data for position in sublist]
position = pd.DataFrame(flattened_data)
position.to_json("historic/data/position.json", orient="records")

position.shape
