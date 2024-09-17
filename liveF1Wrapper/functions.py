from liveF1Wrapper.adapter import LivetimingF1Adapter

def get_season(
    season:int
    ):
    adapter = LivetimingF1Adapter()
    endpoint = urllib.parse.urljoin(str(season) + "/", "Index.json")
    res_text = adapter.get(endpoint=endpoint)
    data = json.loads(res_text)

    return data

def get_meeting(
    season:int, 
    location:string = None,
    meeting_no:int = None
    ):
    pass

    

def get_session():
    pass

def get_race():
    pass