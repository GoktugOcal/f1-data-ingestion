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

