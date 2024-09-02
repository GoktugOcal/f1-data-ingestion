from urllib.request import urlopen
import json
import time
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get session_key for ingestion session table
sessions = pd.read_json('historic/data/sessions.json')

# Getting sessions for each session_key:

all_data = []
start_time = time.time()
for i in sessions.session_key:
    url = f"https://api.openf1.org/v1/team_radio?session_key={i}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    all_data.append(data)
    time.sleep(0.25)
end_time = time.time()
diff = end_time - start_time

flattened_data = [team_radio for sublist in all_data for team_radio in sublist]
team_radio = pd.DataFrame(flattened_data)
team_radio.to_json("historic/data/team_radio.json", orient="records")

team_radio.shape
