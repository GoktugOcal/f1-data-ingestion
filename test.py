from liveF1Wrapper.events import *
from liveF1Wrapper.weekend import Meeting
from liveF1Wrapper.season import Season
from liveF1Wrapper import utils
from liveF1Wrapper.adapter import LivetimingF1Request
import liveF1Wrapper

from liveF1Wrapper.api import download_data
import pandas as pd

import json

s = liveF1Wrapper.get_session(
    season=2024,
    location="Monza",
    session="Race"
)

s.get_feeds()
# print(json.dumps(s.feeds_info, indent=2))

# print(s.load_car_data())
# print(s.load_driver_list())

df = s.get_data(
    dataName = "Position.z",
    dataType = "StreamPath",
    stream = True
)

print(type(df))
for line in df.value[:10]:
    print(line)