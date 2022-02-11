import numpy as np
import pandas as pd

# https://docs.microsoft.com/nl-nl/learn/modules/predict-meteor-showers-using-python/

# show all data
pd.set_option("display.max_rows", None, "display.max_columns", None)

meteor_showers = pd.read_csv('Data/meteorshowers.csv')
moon_phases = pd.read_csv('Data/moonphases.csv')
constellations = pd.read_csv('Data/constellations.csv')
cities = pd.read_csv('Data/cities.csv')

# convert month text to number
months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10, 'november': 11, 'december': 12}
meteor_showers.bestmonth = meteor_showers.bestmonth.map(months)
meteor_showers.startmonth = meteor_showers.startmonth.map(months)
meteor_showers.endmonth = meteor_showers.endmonth.map(months)
moon_phases.month = moon_phases.month.map(months)
constellations.bestmonth = constellations.bestmonth.map(months)

# Convert to date time
meteor_showers['startdate'] = pd.to_datetime(2020 * 10000 + meteor_showers.startmonth * 100 + meteor_showers.startday,
                                             format='%Y%m%d')
meteor_showers['enddate'] = pd.to_datetime(2020 * 10000 + meteor_showers.endmonth * 100 + meteor_showers.endday,
                                           format='%Y%m%d')
moon_phases['date'] = pd.to_datetime(2020 * 10000 + moon_phases.month * 100 + moon_phases.day, format='%Y%m%d')

# convert hemispheres to numbers
hemispheres = {'northern': 0, 'southern': 1, 'northern, southern': 3}
meteor_showers.hemisphere = meteor_showers.hemisphere.map(hemispheres)
constellations.hemisphere = constellations.hemisphere.map(hemispheres)

phases = {'new moon': 0, 'third quarter': 0.5, 'first quarter': 0.5, 'full moon': 1.0}
moon_phases['percentage'] = moon_phases.moonphase.map(phases)
# print(moon_phases.head())

meteor_showers = meteor_showers.drop(['startmonth', 'startday', 'endmonth', 'endday', 'hemisphere'], axis=1)
moon_phases = moon_phases.drop(['month', 'day', 'moonphase', 'specialevent'], axis=1)
constellations = constellations.drop(['besttime'], axis=1)

# make var lastPhase
# Loop all rows if null, row = lastphase else row = lastPhase

lastPhase = 0

for index, row in moon_phases.iterrows():
    if pd.isnull(row['percentage']):
        moon_phases.at[index, 'percentage'] = lastPhase
    else:
        lastPhase = row['percentage']
# test
'''
print("\nmeteor_showers")
meteor_showers.info()
print("\nmoon_phases")
moon_phases.info()
print("\nconstellations")
constellations.info()
print("\ncities")
cities.info()'''

# predictor-function
'''Determine the latitude of a city.
Use latitude to find which constellations are visible.
Use constellations to determine which meteor showers are visible.
Use meteor showers to determine the dates on which they are visible.
Use dates to find the optimal date with the least moonlight.'''


def predict_best_meteor_shower_viewing(city):
    # Create an empty string to return the message back to the user
    meteor_shower_string = ""

    if city not in cities.values:
        meteor_shower_string = "Unfortunately, " + city + " isn't available for a prediction at this time."
        return meteor_shower_string

    # Get the latitude of the city from the cities DataFrame
    latitude = cities.loc[cities['city'] == city, 'latitude'].iloc[0]

    # Get the list of constellations that are viewable from that latitude
    constellation_list = constellations.loc[(constellations['latitudestart'] >= latitude) & (
                constellations['latitudeend'] <= latitude), 'constellation'].tolist()

    # If no constellations are viewable, let the user know
    if not constellation_list:
        meteor_shower_string = "Unfortunately, there are no meteor showers viewable from " + city + "."

        return meteor_shower_string

    meteor_shower_string = "In " + city + " you can see the following meteor showers:\n"

    # Iterate through each constellation that is viewable from the city
    for constellation in constellation_list:
        # Find the meteor shower that is nearest to that constellation
        meteor_shower = meteor_showers.loc[meteor_showers['radiant'] == constellation, 'name'].iloc[0]

        # Find the start and end dates for that meteor shower
        meteor_shower_startdate = meteor_showers.loc[meteor_showers['radiant'] == constellation, 'startdate'].iloc[0]
        meteor_shower_enddate = meteor_showers.loc[meteor_showers['radiant'] == constellation, 'enddate'].iloc[0]

        # Find the Moon phases for each date within the viewable time frame of that meteor shower
        moon_phases_list = moon_phases.loc[
            (moon_phases['date'] >= meteor_shower_startdate) & (moon_phases['date'] <= meteor_shower_enddate)]

        # Find the first date where the Moon is the least visible
        best_moon_date = moon_phases_list.loc[moon_phases_list['percentage'].idxmin()]['date']

        # Add that date to the string to report back to the user
        meteor_shower_string += meteor_shower + " is best seen if you look towards the " + constellation + " constellation on " + best_moon_date.to_pydatetime().strftime(
            "%B %d, %Y") + ".\n"

    return meteor_shower_string

print(predict_best_meteor_shower_viewing('Abu Dhabi'))

