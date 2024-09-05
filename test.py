from liveF1Wrapper.events import *

df = get_all_events(2024)
print(df)

session_path = select_session(2024,"Barcelona","Race")
print(session_path)

get_car_data_stream(session_path)