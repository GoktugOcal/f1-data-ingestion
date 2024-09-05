from liveF1Wrapper.adapter import LivetimingF1Adapter
import urllib


def get_all_events(season:int):

    adapter = LivetimingF1Adapter()
    endpoint = urllib.parse.urljoin(str(season) + "/", "Index.json")
    print(endpoint)
    # adapter.get()


get_all_events(2024)