import urllib
import dateutil.parser
import json
import pandas as pd


from liveF1Wrapper.adapter import LivetimingF1Adapter

import base64
import collections
import datetime
import zlib
from typing import (
    Optional,
    Union
)


def get_all_events(season:int):

    # Create an adapter
    adapter = LivetimingF1Adapter()
    
    # Get the data from {season_year}/Index.json
    endpoint = urllib.parse.urljoin(str(season) + "/", "Index.json")
    res_text = adapter.get(endpoint=endpoint)

    data = json.loads(res_text)

    session_all_data = []
    for meeting in data["Meetings"]:
        for session in meeting["Sessions"]:
            session_data = {
                "season_year" : dateutil.parser.parse(session["StartDate"]).year,
                "meeting_code" : meeting["Code"],
                "meeting_key" : meeting["Key"],
                "meeting_number" : meeting["Number"],
                "meeting_location" : meeting["Location"],
                "meeting_offname" : meeting["OfficialName"],
                "meeting_name" : meeting["Name"],
                "meeting_country_key" : meeting["Country"]["Key"],
                "meeting_country_code" : meeting["Country"]["Code"],
                "meeting_country_name" : meeting["Country"]["Name"],
                "meeting_circuit_key" : meeting["Circuit"]["Key"],
                "meeting_circuit_shortname" : meeting["Circuit"]["ShortName"],
                "session_key" : session["Key"],
                "session_type" : session["Type"] + " " + str(session["Number"]) if "Number" in session else session["Type"],
                "session_name" : session["Name"],
                "session_startDate" : session["StartDate"],
                "session_endDate" : session["EndDate"],
                "gmtoffset" : session["GmtOffset"],
                "path" : session["Path"],
            }
            session_all_data.append(session_data)

    return pd.DataFrame(session_all_data).set_index(["season_year","meeting_location","session_type"])
    

def select_session(season: int, location: str, session_type:str):
    df_sessions = get_all_events(season)
    
    path = df_sessions.loc[season, location, session_type].path.values[0]
    return path

def build_session_page_urls():
    pass

def get_car_data():
    # class CarData ??? --> as data model
    pass


def get_car_data_stream(path):
    adapter = LivetimingF1Adapter()
    endpoint = urllib.parse.urljoin(path + "/", "CarData.z.jsonStream")
    res_text = adapter.get(endpoint=endpoint)
    records = res_text.split('\r\n')[:-1]

    tl = 12
    return dict((r[:12], r[12:]) for r in records)


def parse(text: str, zipped: bool = False) -> Union[str, dict]:
    """
    FastF1 code
    """
    if text[0] == '{':
        return json.loads(text)
    if text[0] == '"':
        text = text.strip('"')
    if zipped:
        text = zlib.decompress(base64.b64decode(text), -zlib.MAX_WBITS)
        return parse(text.decode('utf-8-sig'))
    # _logger.warning("Couldn't parse text")
    return text

def parse_hash(hash_code):
    tl=12
    return parse(hash_code, zipped=True)
