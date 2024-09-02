from urllib.request import urlopen
import json
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

## Meetings Ingestion
response = urlopen('https://api.openf1.org/v1/meetings')
data = json.loads(response.read().decode('utf-8'))
saving_path = "historic/data/meetings.json"
with open(saving_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

## Meetings Arrangement
meetings = pd.read_json("historic/data/meetings.json")
meetings["date_start"] = pd.to_datetime(meetings["date_start"])
meetings.to_json("historic/data/meetings.json", orient="records")