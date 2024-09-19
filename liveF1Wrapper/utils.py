from typing import List, Dict
from liveF1Wrapper import constants
from urllib.parse import urljoin

def build_session_endpoint(session_path):
    return urljoin(urljoin(constants.BASE_URL, constants.STATIC_ENDPOINT), session_path)


def json_parser_for_objects(data:Dict) -> Dict:
    return {key.lower(): value for key, value in data.items()}