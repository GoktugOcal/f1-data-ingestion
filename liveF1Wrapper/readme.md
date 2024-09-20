## USAGE

```python
from liveF1Wrapper as easyF1


season = eastF1.get_season(
    season = 2024
)

meeting = eastF1.get_meeting(
    season = 2024,
    location = "Monza"
)

# Session data
session = eastF1.get_session(
    season=2024,
    location="Monza",
    session="Race"
)

session.get_feeds() # load Info.json
session_info_raw = session.load_session_info() # load sessionInfo.json or others
session_car_data_raw = session.load_car_data() # load carData.z or others

```


## Usage Scenerios

### 1. Data Engine

- Structured data accessing and processing approach



```python
# Input:
#   No (optionally: seasons)
# ---
# Output:
#   List of events 
# ---

# to get weekend list
weekends_table = easyf1.get_weekends()

# to get sessions list
sessions_table = easyf1.get_sessions()

# to get races list
races_table = easyf1.get_races()
```

```python
# Input:
#   Season
#   Meeting = None,
#   Session = None
# ---
# Output:
#   List<Meeting>, List<Season>
# ---

# to get weekend list
weekends_table = easyf1.get_weekends()

# to get sessions list
sessions_table = easyf1.get_sessions()

# to get races list
races_table = easyf1.get_races()
```

Input: 

### 2. Raw Requests

- Accessing specific meetings/sessions
- Data output;
    - Raw
    - Translated
    - Structured
    - with Objects (similar to engine)

### 3. Totally Raw

- Get onyl raw data


