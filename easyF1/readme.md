# EasyF1

![Infrastructure](./docs/figures/easyf1_infrastructure_v01.png)

## USAGE

#### Import the library
```python
from easyF1 as easyF1
```

#### Get season object and its meetings + sessions
```python
season = easyF1.get_season(
    season = 2024
)

print(season) # Shows the dataframe table of sessions and their informations
print(season.meetings) # Get meeting objects
```

#### Get meeting object and its sessions
```python
meeting = easyF1.get_meeting(
    season = 2024,
    location = "Monza"
)

print(meeting) # Shows the dataframe table of sessions and their informations
print(meeting.sessions) # Get session objects
```

#### Get session object and load data
```python
session = easyF1.get_session(
    season=2024,
    location="Monza",
    session="Race"
)

session.get_feeds() # load /Info.json
print(session.feeds_info)
```

```json
{
  "SessionInfo": {
    "KeyFramePath": "SessionInfo.json",
    "StreamPath": "SessionInfo.jsonStream"
  },
  "ArchiveStatus": {
    "KeyFramePath": "ArchiveStatus.json",
    "StreamPath": "ArchiveStatus.jsonStream"
  },
  "Position.z": {
    "KeyFramePath": "Position.z.json",
    "StreamPath": "Position.z.jsonStream"
  },
  "CarData.z": {
    .
    .
    .
```

Load specific data by name of data
```python
data = session.get_data(
    dataName = "Position.z",
    dataType = "StreamPath",
    stream = True
)

print(type(data))
# <class 'easyF1.data_processing.data_models.BasicResult'>

print(data)
#     SessionKey     timestamp                           Utc DriverNo   Status     X      Y     Z
# 0         9590  00:00:30.209  2024-09-01T12:08:13.7879709Z        1  OnTrack     0      0     0
# 1         9590  00:00:30.209  2024-09-01T12:08:13.7879709Z        3  OnTrack     0      0     0
# 2         9590  00:00:30.209  2024-09-01T12:08:13.7879709Z        4  OnTrack     0      0     0
# 3         9590  00:00:30.209  2024-09-01T12:08:13.7879709Z       10  OnTrack     0      0     0

print(data.value)
# [
#   {'SessionKey': 9590, 'timestamp': '00:00:30.209', 'Utc': '2024-09-01T12:08:13.7879709Z', 'DriverNo': '1', 'Status': 'OnTrack', 'X': 0, 'Y': 0, 'Z': 0},
#   {'SessionKey': 9590, 'timestamp': '00:00:30.209', 'Utc': '2024-09-01T12:08:13.7879709Z', 'DriverNo': '3', 'Status': 'OnTrack', 'X': 0, 'Y': 0, 'Z': 0},
#   {'SessionKey': 9590, 'timestamp': '00:00:30.209', 'Utc': '2024-09-01T12:08:13.7879709Z', 'DriverNo': '4', 'Status': 'OnTrack', 'X': 0, 'Y': 0, 'Z': 0},
#   .
#   .
#   .
# ]
```


## Usage Scenerios

### 1. Data Engine

- Structured data accessing and processing approach

### 2. Raw Requests

- Accessing specific meetings/sessions
- Data output;
    - Raw
    - Translated
    - Structured
    - with Objects (similar to engine)

### 3. Totally Raw

- Get onyl raw data

