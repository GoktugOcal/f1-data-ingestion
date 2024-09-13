from typing import List, Dict
from liveF1Wrapper import adapter, utils
from urllib.parse import urljoin

class Session:
    def __init__(
        self,
        **kwargs
        ):
        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
        
        if hasattr(self, "path"):
            self.full_path = utils.build_session_endpoint(self.path)
            self.get_feeds() #Get and save Feed information

    def get_feeds(self):
        self.feeds_info = adapter.request(urljoin(self.full_path, "Index.json"))["Feeds"]
        return self.feeds_info

# SessionData.json
