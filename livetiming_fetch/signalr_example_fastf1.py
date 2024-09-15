####


import logging
from livetiming_fetch.client import SignalRClient


log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClient("TimingData.json", debug=False, timeout=600, topics=["TimingData"])
""" 
topics argument can be changed. 
Default: ["CarData.z"]

parameters:
    ["Heartbeat", "CarData.z", "Position.z",
    "ExtrapolatedClock", "TopThree", "RcmSeries",
    "TimingStats", "TimingAppData",
    "WeatherData", "TrackStatus", "DriverList",
    "RaceControlMessages", "SessionInfo",
    "SessionData", "LapCount", "TimingData"]
"""

client.start()





