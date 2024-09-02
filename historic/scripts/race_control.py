from urllib.request import urlopen
import json
import pandas as pd
import time
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get session_keys for ingestion session table
sessions = pd.read_json('historic/data/sessions.json')

# Getting race_control for each session_key:

all_data = []
start = time.time()
for i in sessions.session_key:
    url = f"https://api.openf1.org/v1/race_control?session_key={i}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    all_data.append(data)
end = time.time()
operation_time = end - start

flattened_data = [race_control for sublist in all_data for race_control in sublist]
race_control = pd.DataFrame(flattened_data)
race_control.to_json("historic/data/race_control.json", orient="records")

# Quality Check:

race_control.shape
race_control.describe()
