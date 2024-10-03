from typing import List, Dict
from liveF1Wrapper import adapter, utils
from urllib.parse import urljoin

from .adapter import LivetimingF1Request, LivetimingF1GetData
from .utils import get_car_data_stream
from .etl import *

class Session:
    def __init__(
        self,
        season:"Season" = None,
        year:int = None,
        meeting:"Meeting" = None,
        key:int = None,
        name:str = None,
        type:str = None,
        number:int = None,
        startdate:str = None,
        enddate:str = None,
        gmtoffset:str = None,
        path:Dict = None,
        loaded:bool = False,
        **kwargs
        ):

        self.season = season
        self.loaded = loaded
        self.etl_parser = easyF1_sessionETL(session = self)
        
        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in locals().items():
            if value: setattr(self, key.lower(), value)
        
        if hasattr(self, "path"):
            self.full_path = utils.build_session_endpoint(self.path)

    # def load_meeting(self):
    #     get_meeting(
    #         season = self.year,
    #         location = self.
    #         )

    def get_feeds(self):
        self.feeds_info = LivetimingF1Request(urljoin(self.full_path, "Index.json"))["Feeds"]
        return self.feeds_info

    
    def get_data(self, dataName, dataType, stream):
        data = LivetimingF1GetData(
            urljoin(self.full_path, self.feeds_info[dataName][dataType]),
            stream=stream
            )
        
        return list(self.etl_parser.unifiedParse(
            dataName,
            data
        ))


    
    # def __str__(self):
    #     return f""

    # SessionInfo
    # this data is static, stream is not needed
    def load_session_info(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["SessionInfo"]["KeyFramePath"]))
        return data

    # ArchiveStatus
    def load_archive_status(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["ArchiveStatus"]["KeyFramePath"]))
        return data

    # TrackStatus    
    def load_track_stauts(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["TrackStatus"]["KeyFramePath"]))
        return data
    
    # SessionData
    def load_session_data(self):
        data = LivetimingF1GetData(
            urljoin(self.full_path, self.feeds_info["SessionData"]["StreamPath"]),
            stream=True
            )
        
        return list(parse_session_data(
            data=data,
            session_key = self.key
        ))
    
    # ContentStreams
    def load_content_streams(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["ContentStreams"]["KeyFramePath"]))
        return data

    # AudioStreams
    def load_audio_streams(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["AudioStreams"]["KeyFramePath"]))
        return data
    
    # ExtrapolatedClock
    def load_extrapolated_clock(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["ExtrapolatedClock"]["KeyFramePath"]))
        return data

    # CarData.z
    def load_car_data(self, stream=True):
        # if stream: data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["CarData.z"]["StreamPath"]))
        # else: data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["CarData.z"]["KeyFramePath"]))
        if stream: data = get_car_data_stream(urljoin(self.full_path, self.feeds_info["CarData.z"]["StreamPath"]))
        else: data = get_car_data_stream(urljoin(self.full_path, self.feeds_info["CarData.z"]["KeyFramePath"]))
        
        return data
    
    # Position.z
    def load_position(self, stream=True):
        if stream: data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["Position.z"]["StreamPath"]))
        else: data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["Position.z"]["KeyFramePath"]))
        return data
    
    # TimingDataF1
    def load_timing_data_f1(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["TimingDataF1"]["KeyFramePath"]))
        return data
    
    # TimingData
    def load_timing_data(self):
        data = LivetimingF1Request(urljoin(self.full_path, self.feeds_info["TimingData"]["KeyFramePath"]))
        return data
    
    # DriverList
    # this data is static, stream is not needed
    def load_driver_list(self):
        data = LivetimingF1GetData(
            urljoin(self.full_path, self.feeds_info["DriverList"]["KeyFramePath"]),
            stream=False
            )
        return list(parse_driver_list(
            data=data,
            session_key = self.key
            ))

    # TyreStintSeries
    def load_tyre_stint_series(self):
        data = LivetimingF1GetData(
            urljoin(self.full_path, self.feeds_info["TyreStintSeries"]["StreamPath"]),
            stream=True
            )

        return list(self.etl_parser.unifiedParse(
            "TyreStintSeries",
            data
        ))
    
    # DriverRaceInfo
    def load_driver_race_info(self):
        data = LivetimingF1GetData(
            urljoin(self.full_path, self.feeds_info["DriverRaceInfo"]["StreamPath"]),
            stream=True
            )
        return list(parse_driver_race_info(
            data=data,
            session_key = self.key
            ))


    # SessionStatus
    # LapSeries
    # TopThree
    # TimingAppData
    # TimingStats
    # Heartbeat
    # WeatherData
    # WeatherDataSeries
    # TlaRcm
    # RaceControlMessages
    # PitLaneTimeCollection
    # CurrentTyres
    def load_current_tyres(self):
        data = LivetimingF1GetData(
            urljoin(self.full_path, self.feeds_info["CurrentTyres"]["StreamPath"]),
            stream=True
            )
        return list(parse_current_tyres(
            data=data,
            session_key = self.key
            ))

    # TeamRadio