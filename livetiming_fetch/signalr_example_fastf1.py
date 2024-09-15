"""Using the Fast-F1 signalr client?
======================================

Demonstrates the usage of the SignalRClient
"""
import logging

from fastf1.livetiming.client import SignalRClient


log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClient(filename="output.txt", debug=True, timeout=600)
client.start()






import fastf1
from fastf1.livetiming.data import LiveTimingData

livedata = LiveTimingData('output2.txt')
session = fastf1.get_testing_session(year=2023, test_number=1, session_number=1)
session.load(livedata=livedata)

print(session.car_data['44'])







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





