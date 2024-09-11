from typing import List, Dict


class Meeting: # Weekend
    def __init__(
        self,
        Season:int = None,
        Sessions:Dict = None,
        Key:int = None,
        Code:str = None,
        Number:int = None,
        Location:str = None,
        OfficialName:str = None,
        Name:str = None,
        Country:Dict = None,
        Circuit:Dict = None
        ):

        self.season = Season
        self.name = Name
        self.official_name = OfficialName
        self.key = Key
        self.code = Code
        self.number = Number
        self.location = Location

        # Special classes will come for these attributes
        self.sessions = Sessions
        self.country = Country
        self.circuit = Circuit