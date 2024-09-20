from .session import Session
from .season import Season
from .weekend import Meeting

from .api import (
    download_data
)
from .utils import *

from .adapter import LivetimingF1Adapter

from .functions import (
    get_season,
    get_meeting,
    get_session
    )

class easyf1():
    def __init__(
        self,
        year_from:int = None,
        year_to:int = None
        ):
        pass
        

