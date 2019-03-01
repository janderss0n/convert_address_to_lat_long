import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv('data_file.csv', sep=';', decimal='.')


df['Full.Address'] = df['Full.Address'].str.replace('\n', ', ')




geolocator = Nominatim(user_agent="specify_your_app_name_here")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
df['location'] = df['Full.Address'].apply(geocode)

df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)


df.to_csv('temp_geo.csv')
geo = pd.read_csv('temp_geo.csv')

a = geo['point'].str.split(',', expand=True)
print(type(a))
b = a.rename(columns={0: 'latitude', 1: 'longitude'}).drop(columns=[2])

geo['latitude'] = b['latitude'].str.replace('(', '')
geo['longitude'] = b['longitude']
print(geo.head())
geo.to_csv('geocoded_data.csv', sep=';', decimal='.')
