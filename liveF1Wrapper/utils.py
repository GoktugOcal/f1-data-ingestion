from typing import List, Dict
from liveF1Wrapper import constants
from urllib.parse import urljoin

import base64
import collections
import datetime
import zlib
import json
from typing import (
    Optional,
    Union
)

from .adapter import LivetimingF1Adapter

def build_session_endpoint(session_path):
    return urljoin(urljoin(constants.BASE_URL, constants.STATIC_ENDPOINT), session_path)


def json_parser_for_objects(data:Dict) -> Dict:
    return {key.lower(): value for key, value in data.items()}

############333

def get_data(path, stream):
    adapter = LivetimingF1Adapter()
    endpoint = path
    res_text = adapter.get(endpoint=endpoint)

    if stream:
        records = res_text.split('\r\n')[:-1]
        tl = 12
        return dict((r[:tl], r[tl:]) for r in records)
    else:
        records = res_text
        return records


def get_car_data_stream(path):
    adapter = LivetimingF1Adapter()
    endpoint = path
    res_text = adapter.get(endpoint=endpoint)
    records = res_text.split('\r\n')[:-1]

    tl = 12
    return dict((r[:12], r[12:]) for r in records)


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





def parse_helper_for_nested_dict(info, record, prefix=""):
    for info_k, info_v in info.items():
        if isinstance(info_v, list): record = {**record, **{**{info_k + "_" + str(sector_no+1) + "_" + k : v  for sector_no in range(len(info_v)) for k,v in info_v[sector_no].items()}}}
        elif isinstance(info_v, dict): record = parse_helper(info_v, record, prefix= prefix + info_k + "_")
        else: record = {**record, **{prefix + info_k : info_v}}
    return record