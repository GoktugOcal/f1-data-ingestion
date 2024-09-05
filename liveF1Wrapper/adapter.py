import requests
import urllib
from typing import List, Dict

base_hostname = "https://livetiming.formula1.com"

class LivetimingF1Adapter:
    def __init__(self):
        self.url = urllib.parse.urljoin(base_hostname,"static/") # https://livetiming.formula1.com/static/ this is for base, endpoint is required
    
    def get(self, endpoint: str, header: Dict = None):
        req_url = urllib.parse.urljoin(self.url, endpoint) # Build the url for request
        response = requests.get(
            url=req_url,
            headers=header
            )

        res_text = response.content.decode('utf-8-sig')
        return res_text