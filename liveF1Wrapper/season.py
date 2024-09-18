from liveF1Wrapper.adapter import LivetimingF1Adapter
import urllib
import json
import pandas as pd
import dateutil

class Season:
    def __init__(
        self,
        season_year:int
        ):

        adapter = LivetimingF1Adapter()
        endpoint = urllib.parse.urljoin(str(season_year) + "/", "Index.json")
        res_text = adapter.get(endpoint=endpoint)
        self.json_data = json.loads(res_text)
        self.parse_meetings()

    def parse_meetings(self):
        session_all_data = []

        for meeting in self.json_data["Meetings"]:
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

        self.meetings_table = pd.DataFrame(session_all_data).set_index(["season_year","meeting_location","session_type"])



