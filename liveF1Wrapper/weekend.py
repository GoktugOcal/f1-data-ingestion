from typing import List, Dict
from liveF1Wrapper import (
    utils,
    Session
)

class Meeting: # Weekend
    def __init__(
        self,
        code:int = None,
        key:str = None,
        number:int = None,
        location:str = None,
        officialName:str = None,
        name:str = None,
        country:Dict = None,
        circuit:Dict = None,
        sessions:List = None,
        **kwargs # In case new information comes from the API in future
        ):

        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

        if hasattr(self, "sessions"):
            self.sessions_json = self.sessions
            self.sessions = []
            for session_data in self.sessions_json:
                self.sessions.append(Session(meeting = self, **session_data))

        
        
    def parse_seasons(self):
        session_all_data = []

        for session in self.sessions:
            session_data = {
                "season_year" : dateutil.parser.parse(session["StartDate"]).year,
                "meeting_code" : self.code,
                "meeting_key" : self.key,
                "meeting_number" : self.number,
                "meeting_location" : self.location,
                "meeting_offname" : self.officialName,
                "meeting_name" : self.name,
                "meeting_country_key" : self.country["Key"],
                "meeting_country_code" : self.country["Code"],
                "meeting_country_name" : self.country["Name"],
                "meeting_circuit_key" : self.circuit["Key"],
                "meeting_circuit_shortname" : self.circuit["ShortName"],
                "session_key" : session.get("Key", None),
                "session_type" : session["Type"] + " " + str(session["Number"]) if "Number" in session else session["Type"],
                "session_name" : session.get("Name", None),
                "session_startDate" : session.get("StartDate", None),
                "session_endDate" : session.get("EndDate", None),
                "gmtoffset" : session.get("GmtOffset", None),
                "path" : session.get("Path", None),
            }
            session_all_data.append(session_data)

        self.sessions_table = pd.DataFrame(session_all_data).set_index(["season_year","meeting_location","session_type"])
