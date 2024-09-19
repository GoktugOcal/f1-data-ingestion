from liveF1Wrapper.adapter import LivetimingF1Adapter, LivetimingF1Request
from liveF1Wrapper import (
    Session,
    Season
)

import urllib

def get_season(
    season:int
    ):
    season_data = LivetimingF1Request(urllib.parse.urljoin(str(season) + "/", "Index.json"))
    return Season(**season_data)

def get_meeting(
    season:int, 
    location:str = None,
    meeting_no:int = None
    ):
    pass

    

def get_session():
    pass

def get_race():
    pass