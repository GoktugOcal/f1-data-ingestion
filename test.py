from liveF1Wrapper.events import *
from liveF1Wrapper.weekend import Meeting
from liveF1Wrapper.season import Season
from liveF1Wrapper import utils
from liveF1Wrapper.adapter import LivetimingF1Request
import liveF1Wrapper

# df = get_all_events(2024)
# print(df)

# session_path = select_session(2024,"Barcelona","Race")
# print(session_path)

# get_car_data_stream(session_path)


season = 2024

# # Create an adapter
# adapter = LivetimingF1Adapter()

# # Get the data from {season_year}/Index.json
# endpoint = urllib.parse.urljoin(str(season) + "/", "Index.json")
# res_text = adapter.get(endpoint=endpoint)

# data = json.loads(res_text)

# for weekend_data in data["Meetings"]:
#     meeting = Meeting(
#         Season=data["Year"],
#         **weekend_data
#         )

#     # print(meeting.season)
#     print(meeting.sessions[0].get_feeds())


# season = Season(season)
# print(season.meetings_table)

# get_season(2024)

from liveF1Wrapper.api import download_data

# data = download_data(2024, "Monza", "Race")
# # loader(2024, "Monza")
# # loader(2024)
# # loader(2024, "Race"),


# print(data)

# s = Season(2024)
# print(s.meetings[0].load(force=True))

# m = Meeting(
#     year = 2024,
#     location = "Monza")
# m.load()
# m.parse_sessions()
# print(m.sessions_table)


# sess = m.sessions[0]
# sess.get_feeds()

# for title in sess.feeds_info.keys():

#     print(title)

s = liveF1Wrapper.get_session(
    season=2024,
    location="Monza",
    session="Race"
)

s.get_feeds()

print(s.load_car_data())