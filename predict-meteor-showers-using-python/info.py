import pandas as pd

# https://docs.microsoft.com/nl-nl/learn/modules/predict-meteor-showers-using-python/

# show all data
pd.set_option("display.max_rows", None, "display.max_columns", None)

meteor_showers = pd.read_csv('Data/meteorshowers.csv')
moon_phases = pd.read_csv('Data/moonphases.csv')
constellations = pd.read_csv('Data/constellations.csv')
cities = pd.read_csv('Data/cities.csv')

print("\n meteor_showers info,head")
print(meteor_showers.head(), "\n")
meteor_showers.info()

print("\n moon_phases info,head")
print(moon_phases.head(), "\n")
moon_phases.info()

print("\n constellations info,head")
print(constellations.head(), "\n")
constellations.info()

print("\n cities info,head")
print(cities.head(), "\n")
cities.info()
