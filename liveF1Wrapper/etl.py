import json
from typing import (
    Optional,
    Union
) 

def parse_car_data(data:json):

    return json, csv, pandas

def session():
    pass


def parse_tyre_stint_series(data):
    for key, value in data.items():
        for driver_no, stint in value["Stints"].items():
            if stint:
                for pit_count, current_info in stint.items():
                    record = {
                        **{
                            "timestamp": key,
                            "DriverNo": driver_no,
                            "PitCount": pit_count,
                        },
                        **current_info
                    }

                    yield record

def parse_driver_race_info(data):
    for key, value in data.items():
        for driver_no, info in value.items():
            record = {
                **{
                    "timestamp": key,
                    "DriverNo": driver_no,
                },
                **info
            }
            
            yield record


def parse_current_tyres(data):
    for key, value in data.items():
        for driver_no, info in value["Tyres"].items():
            record = {
                **{
                    "timestamp": key,
                    "DriverNo": driver_no,
                },
                **info
            }
            yield record

def parse_driver_list(data):
    for driver_no, info in data.items():
        record = {
            **{
                "DriverNo": driver_no,
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