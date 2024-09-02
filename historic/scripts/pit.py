from urllib.request import urlopen
import json
import pandas as pd
import time
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Get session_keys for ingestion session table
sessions = pd.read_json('historic/data/sessions.json')

# Getting pit for each session_key:

all_data = []
start = time.time()
for i in sessions.session_key:
    url = f"https://api.openf1.org/v1/pit?session_key={i}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    all_data.append(data)
    time.sleep(0.25)
end = time.time()
operation_time = end - start

flattened_data = [pit for sublist in all_data for pit in sublist]
pit = pd.DataFrame(flattened_data)
pit.to_json("historic/data/pit.json", orient="records")

# Quality Check:

pit.shape
pit.describe()
