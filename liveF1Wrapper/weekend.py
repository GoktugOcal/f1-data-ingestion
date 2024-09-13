from typing import List, Dict
import liveF1Wrapper

class Meeting: # Weekend
    def __init__(
        self,
        # Season:int = None,
        # Sessions:Dict = None,
        # Key:int = None,
        # Code:str = None,
        # Number:int = None,
        # Location:str = None,
        # OfficialName:str = None,
        # Name:str = None,
        # Country:Dict = None,
        # Circuit:Dict = None,

        **kwargs
        ):

        # self.season = Season
        # self.name = Name
        # self.official_name = OfficialName
        # self.key = Key
        # self.code = Code
        # self.number = Number
        # self.location = Location

        # # Special classes will come for these attributes
        # self.sessions = Sessions
        # self.country = Country
        # self.circuit = Circuit

        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

        
        if hasattr(self, "sessions"):
            self.sessions_json = self.sessions
            self.sessions = []
            for session_data in self.sessions_json:
                self.sessions.append(liveF1Wrapper.Session(**session_data))