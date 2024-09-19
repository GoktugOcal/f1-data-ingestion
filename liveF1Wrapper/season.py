from liveF1Wrapper.adapter import LivetimingF1Adapter
import liveF1Wrapper
import urllib
import json
import pandas as pd
import dateutil

class Season:
    def __init__(
        self,
        **kwargs
        ):
        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
        
        self.parse_meetings()

        self.meetingObjs = []
        for meeting in self.meetings:
            self.meetingObjs.append(liveF1Wrapper.Meeting(**meeting))
            
    # def load(self):
    #     adapter = LivetimingF1Adapter()
    #     endpoint = urllib.parse.urljoin(str(self.year) + "/", "Index.json")
    #     res_text = adapter.get(endpoint=endpoint)
    #     self.json_data = json.loads(res_text)
    #     self.parse_meetings()

    def parse_meetings(self):
        session_all_data = []

        for meeting in self.meetings:
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

    def __repr__(self):
        display(self.meetings_table)
    
    def __str__(self):
        print(self.meetings_table)