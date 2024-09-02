from urllib.request import urlopen
import json
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get session_keys for ingestion session table
sessions = pd.read_json('historic/data/sessions.json')

# Getting drivers for each session_key:

all_data = []
for i in sessions.session_key:
    url = f"https://api.openf1.org/v1/drivers?session_key={i}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    all_data.append(data)

flattened_data = [drivers for sublist in all_data for drivers in sublist]
drivers = pd.DataFrame(flattened_data)
drivers.to_json("historic/data/drivers.json", orient="records")


#Check
drivers["first_name"].unique()

