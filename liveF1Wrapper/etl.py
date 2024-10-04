import json
from typing import (
    Optional,
    Union
) 

def parse_car_data(data:json):

    return json, csv, pandas

def session():
    pass


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
            'TimingData': None,
            'LapSeries': None,
            'TopThree': None,
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
    session_key
    ):
    for key, value in data.items():
        for driver_no, stint in value["Stints"].items():
            if stint:
                for pit_count, current_info in stint.items():
                    record = {
                        **{
                            "session_key": session_key,
                            "timestamp": key,
                            "DriverNo": driver_no,
                            "PitCount": pit_count,
                        },
                        **current_info
                    }

                    yield record

def parse_driver_race_info(
    data,
    session_key
    ):
    for key, value in data.items():
        for driver_no, info in value.items():
            record = {
                **{
                    "session_key": session_key,
                    "timestamp": key,
                    "DriverNo": driver_no,
                },
                **info
            }
            
            yield record

def parse_current_tyres(
    data,
    session_key
    ):
    for key, value in data.items():
        for driver_no, info in value["Tyres"].items():
            record = {
                **{
                    "session_key": session_key,
                    "timestamp": key,
                    "DriverNo": driver_no,
                },
                **info
            }
            yield record

def parse_driver_list(
    data,
    session_key
    ):
    for driver_no, info in data.items():
        record = {
            **{ 
                "session_key" : session_key,
                "DriverNo": driver_no,
            },
            **info
        }
        
        yield record

def parse_session_data(
    data,
    session_key
    ):
    for key, value in data.items():
        for driver_no, info in value.items():
            try:
                record = {
                    **{
                        "session_key" : session_key
                    },
                    **list(info.values())[0]
                }
                
                yield record
            except Exception as e:
                pass

def parse_extrapolated_clock(
    data,
    session_key
    ):
    for key, info in data.items():
        record = {
            **{
                "session_key": session_key,
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