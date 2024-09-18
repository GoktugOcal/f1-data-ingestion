from liveF1Wrapper.events import *
from liveF1Wrapper.weekend import Meeting
from liveF1Wrapper.season import Season
from liveF1Wrapper import utils

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


season = Season(2024)
print(season.meetings_table)