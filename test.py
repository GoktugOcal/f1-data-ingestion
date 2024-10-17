import easyF1

s = easyF1.get_session(
    season=2024,
    location="Monza",
    session="Race"
)


s.get_feeds()

df = s.get_data(
    dataName = "Position.z",
    dataType = "StreamPath",
    stream = True
)

print(df)

# print(type(df))
# for line in df.value[:10]:
#     print(line)


# easyF1.download_data(
#     season_identifier=2024,
#     location_identifier="Monaza"
# )