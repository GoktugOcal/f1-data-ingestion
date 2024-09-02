import fastf1
import os

# Cache dizinini oluştur
os.makedirs('cache', exist_ok=True)

# Cache'yi etkinleştiriyoruz
fastf1.Cache.enable_cache('cache')

# 2015 İtalya Grand Prix'sini yüklüyoruz
session = fastf1.get_session(2015, 'Monza', 'R')
session.load()

# İlk birkaç tur zamanını görüntülüyoruz
laps = session.laps
print(laps[['Driver', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']].head())
