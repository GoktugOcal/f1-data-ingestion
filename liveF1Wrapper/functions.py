from liveF1Wrapper.adapter import LivetimingF1Adapter, LivetimingF1Request
from liveF1Wrapper import (
    Session,
    Season,
    Meeting
)

from .api import download_data
from .utils import json_parser_for_objects

import urllib

def get_season(
    season:int
    ):
    # season_data = LivetimingF1Request(urllib.parse.urljoin(str(season) + "/", "Index.json"))
    season_data = download_data(season_identifier=season)
    return Season(**json_parser_for_objects(season_data))

def get_meeting(
    season:int, 
    location:str = None,
    meeting_no:int = None
    ):
    meeting_data = download_data(
        season_identifier=season,
        location_identifier=location)
    return Meeting(**json_parser_for_objects(meeting_data))

def get_session(
    season:int, 
    location:str = None,
    meeting_no:int = None,
    session:str = None,
    session_no:int = None
    ):
    session_data = download_data(
        season_identifier=season,
        location_identifier=location,
        session_identifier=session)
    return Session(**json_parser_for_objects(session_data))

def get_race():
    pass