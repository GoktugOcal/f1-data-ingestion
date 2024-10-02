from .api import download_data
from .weekend import Meeting
from .utils import json_parser_for_objects, build_session_endpoint

import urllib
import json
import pandas as pd
import dateutil

class Season:
    def __init__(
        self,
        year,
        meetings
        ):
        self.year = year
        self.load()

    def load(self):
        self.json_data = download_data(self.year)
        for key, value in json_parser_for_objects(self.json_data).items():
            setattr(self, key.lower(), value)
        
        self.meetings_json = self.meetings
        self.meetings = []

        self.parse_sessions()
        self.set_meetings()

    def set_meetings(self):

        self.meetings = []
        for meeting in self.meetings_json:
            self.meetings.append(
                Meeting(
                    season = self,
                    loaded = True,
                    **json_parser_for_objects(meeting)
                    )
                )

    def parse_sessions(self):
        session_all_data = []

        for meeting in self.meetings_json:
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
                    "session_key" : session.get("Key", None),
                    "session_type" : session["Type"] + " " + str(session["Number"]) if "Number" in session else session["Type"],
                    "session_name" : session.get("Name", None),
                    "session_startDate" : session.get("StartDate", None),
                    "session_endDate" : session.get("EndDate", None),
                    "gmtoffset" : session.get("GmtOffset", None),
                    "path" : session.get("Path", None),
                }
                session_all_data.append(session_data)

        self.meetings_table = pd.DataFrame(session_all_data).set_index(["season_year","meeting_location","session_type"])

    # def __repr__(self):
    #     display(self.meetings_table)
    
    # def __str__(self):
    #     return self.meetings_table.__str__()