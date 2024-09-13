from liveF1Wrapper import constants
from urllib.parse import urljoin

def build_session_endpoint(session_path):
    return urljoin(urljoin(constants.BASE_URL, constants.STATIC_ENDPOINT), session_path)