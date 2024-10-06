import json
import pandas as pd
from typing import (
    Optional,
    Union
) 

def parse_car_data(data:json):

    return json, csv, pandas

def session():
    pass

class basicResult:
    def __init__(
        self,
        data:json
        ):
        self.value = data

    def __get__(self):
        return self.value
    
    def __str__(self):
        return pd.DataFrame(self.value).__str__()


class easyF1_sessionETL:
    def __init__(self, session):
        self.session = session
        self.functionMap = {
            'SessionInfo': None,
            'ArchiveStatus': None,
            'TrackStatus': None,
            'SessionData': parse_session_data,
            'ContentStreams': None,
            'AudioStreams': None,
            'ExtrapolatedClock': parse_extrapolated_clock,
            'DriverList': parse_driver_list,
            'TimingDataF1': parse_timing_data,
            'TimingData': parse_timing_data, # what is the difference with timingdataf1
            'LapSeries': parse_lap_series,
            'TopThree': parse_top_three,
            'TimingAppData': None,
            'TimingStats': None,
            'SessionStatus': None,
            'TyreStintSeries': parse_tyre_stint_series,
            'Heartbeat': None,
            'Position.z': None,
            'WeatherData': None,
            'WeatherDataSeries': None,
            'CarData.z': None,
            'TeamRadio': None,
            'TlaRcm': None,
            'RaceControlMessages': None,
            'PitLaneTimeCollection': None,
            'CurrentTyres': parse_current_tyres,
            'DriverRaceInfo': parse_driver_race_info
            }

    def unifiedParse(self, title, data):
        return self.functionMap[title](
            data,
            self.session.key
            )




def parse_tyre_stint_series(
    data,
    sessionKey
    ):
    for key, value in data.items():
        for driver_no, stint in value["Stints"].items():
            if stint:
                for pit_count, current_info in stint.items():
                    record = {
                        **{
                            "session_key": sessionKey,
                            "timestamp": key,
                            "DriverNo": driver_no,
                            "PitCount": pit_count,
                        },
                        **current_info
                    }

                    yield record

def parse_driver_race_info(
    data,
    sessionKey
    ):
    for key, value in data.items():
        for driver_no, info in value.items():
            record = {
                **{
                    "session_key": sessionKey,
                    "timestamp": key,
                    "DriverNo": driver_no,
                },
                **info
            }
            
            yield record

def parse_current_tyres(
    data,
    sessionKey
    ):
    for key, value in data.items():
        for driver_no, info in value["Tyres"].items():
            record = {
                **{
                    "session_key": sessionKey,
                    "timestamp": key,
                    "DriverNo": driver_no,
                },
                **info
            }
            yield record

def parse_driver_list(
    data,
    sessionKey
    ):
    for driver_no, info in data.items():
        record = {
            **{ 
                "session_key" : sessionKey,
                "DriverNo": driver_no,
            },
            **info
        }
        
        yield record

def parse_session_data(
    data,
    sessionKey
    ):
    for key, value in data.items():
        for driver_no, info in value.items():
            try:
                record = {
                    **{
                        "session_key" : sessionKey
                    },
                    **list(info.values())[0]
                }
                
                yield record
            except Exception as e:
                pass

def parse_extrapolated_clock(
    data,
    sessionKey
    ):
    for key, info in data.items():
        record = {
            **{
                "session_key": sessionKey,
                "timestamp": key,
            },
            **info
        }
        yield record

def parse_timing_data(
    data,
    sessionKey
    ):
    def parse_helper(info, record, prefix=""):
        for info_k, info_v in info.items():

            if isinstance(info_v, list):
                record = {
                    **record,
                    **{
                        **{info_k + "_" + str(sector_no+1) + "_" + k : v  for sector_no in range(len(info_v)) for k,v in info_v[sector_no].items()}
                    }
                }

            elif isinstance(info_v, dict):
                record = parse_helper(info_v, record, prefix= prefix + info_k + "_")
                # record = {
                #     **record,
                #     **{
                #         info_k + "_" + k : v for k,v in info_v.items()
                #     }
                # }

            else:
                record = {
                    **record,
                    **{
                        prefix + info_k : info_v 
                    }
                }
        
        return record

    for ts, value in data.items():
        if "Withheld" in value.keys(): withTheId = value["Withheld"]
        else: withTheId = None
        
        for driver_no, info in value["Lines"].items():
            record= {
                    "SessionKey" : sessionKey,
                    "timestamp" : ts,
                    "DriverNo" : driver_no
                }

            record = parse_helper(info, record)

            yield record

def parse_lap_series(
    data,
    sessionKey
    ):
    for ts, ts_value in data.items():
        for driver_no, driver_data in ts_value.items():
            if isinstance(driver_data["LapPosition"], list):
                for position in driver_data["LapPosition"]:
                    record = {
                            "SessionKey" : sessionKey,
                            "timestamp" : ts,
                            "DriverNo" : driver_no,
                            "Lap" : 0,
                            "LapPosition" : position
                        }
                    yield record
                
            
            elif isinstance(driver_data["LapPosition"], dict):
                for lap, position in driver_data["LapPosition"].items():
                    record = {
                            "SessionKey" : SessionKey,
                            "timestamp" : ts,
                            "DriverNo" : driver_no,
                            "Lap" : lap,
                            "LapPosition" : position
                        }
                    yield record


def parse_top_three(
    data,
    sessionKey
    ):
    for ts, ts_value in data.items():
        if "Withheld" in ts_value.keys():
            continue

        for position, info in ts_value["Lines"].items():

            record = {
                **{
                    "SessionKey" : sessionKey,
                    "timestamp" : ts,
                    "DriverAtPosition" : position
                },
                **info
            }
            yield record

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