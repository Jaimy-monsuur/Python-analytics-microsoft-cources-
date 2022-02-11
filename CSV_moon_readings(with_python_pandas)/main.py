import pandas as pd

# https://docs.microsoft.com/nl-nl/learn/modules/plan-moon-mission-using-python-pandas
rock_samples = pd.read_csv('data/rocksamples.csv')

'''info'''
rock_samples.info()
print("\nPrint first 5 lines")
print(rock_samples.head(5))

'''omzetten'''
rock_samples['Weight (g)'] = rock_samples['Weight (g)'].apply(lambda x: x * 0.001)
rock_samples.rename(columns={'Weight (g)': 'Weight (kg)'}, inplace=True)

'''print'''
print("\nPrint first 5 lines")
print(rock_samples.head(5))

'''Missie'''
missions = pd.DataFrame()
missions['Mission'] = rock_samples['Mission'].unique()
missions.head()

print("\nPrint first lines")
print(missions.head())
print("\ninfo")
missions.info()

'''Totaal gewicht '''
sample_total_weight = rock_samples.groupby('Mission')['Weight (kg)'].sum()
missions = pd.merge(missions, sample_total_weight, on='Mission')
missions.rename(columns={'Weight (kg)': 'Sample weight (kg)'}, inplace=True)
print("\n totaal gewicht per missie")
print(missions)

'''gewicht verschil'''
missions['Weight diff'] = missions['Sample weight (kg)'].diff()
print("\n verschil per missie")
print(missions)

'''NaN naar 0'''
missions['Weight diff'] = missions['Weight diff'].fillna(value=0)
print("\n verschil per missie zonder NaN")
print(missions)

'''Lunar module + command module gewicht en verschil'''
missions[
    'Lunar module (LM)'] = 'Eagle (LM-5)', 'Intrepid (LM-6)', 'Antares (LM-8)', 'Falcon (LM-10)', 'Orion (LM-11)', 'Challenger (LM-12) '
missions['LM mass (kg)'] = 15103, 15235, 15264, 16430, 16445, 16456
missions['LM mass diff'] = missions['LM mass (kg)'].diff()
missions['LM mass diff'] = missions['LM mass diff'].fillna(value=0)

missions['Command module (CM)'] = 'Columbia (CSM-107)', 'Yankee Clipper (CM-108)', 'Kitty Hawk (CM-110)', 'Endeavor (' \
                                                                                                          'CM-112)', \
                                  'Casper (CM-113)', 'America (CM-114) '
missions['CM mass (kg)'] = 5560, 5609, 5758, 5875, 5840, 5960
missions['CM mass diff'] = missions['CM mass (kg)'].diff()
missions['CM mass diff'] = missions['CM mass diff'].fillna(value=0)
print("\n Lunar module + command module gewicht")
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(missions)

'''totaal gewicht Lunar module + command module plus verschil per missie'''
missions['Total weight (kg)'] = missions['LM mass (kg)'] + missions['CM mass (kg)']
missions['Total weight diff'] = missions['LM mass diff'] + missions['CM mass diff']
print("\n Lunar module + command module gewicht")
print(missions)

# Sample-to-weight ratio
saturnVPayload = 43500
'''Calculate crew area,netto sample lading'''
missions['Crewed area : Payload'] = missions['Total weight (kg)'] / saturnVPayload
missions['Sample : Crewed area'] = missions['Sample weight (kg)'] / missions['Total weight (kg)']
missions['Sample : Payload'] = missions['Sample weight (kg)'] / saturnVPayload
print("\n Calculate crew area,netto sample lading")
print(missions)

# gemiddelde van verhoudingen over alle missies.
crewedArea_payload_ratio = missions['Crewed area : Payload'].mean()
sample_crewedArea_ratio = missions['Sample : Crewed area'].mean()
sample_payload_ratio = missions['Sample : Payload'].mean()
print("\ngemiddelde van verhoudingen over alle missies")
print(crewedArea_payload_ratio)
print(sample_crewedArea_ratio)
print(sample_payload_ratio)

# Basic artemis dataframe
artemis_crewedArea = 26520
artemis_mission = pd.DataFrame({'Mission': ['artemis1', 'artemis1b', 'artemis2'],
                                'Total weight (kg)': [artemis_crewedArea, artemis_crewedArea, artemis_crewedArea],
                                'Payload (kg)': [26988, 37965, 42955]})
print("\nBasic artemis dataframe")
print(artemis_mission)

# Voorspelling artemis
artemis_mission['Sample weight from total (kg)'] = artemis_mission['Total weight (kg)'] * sample_crewedArea_ratio
artemis_mission['Sample weight from payload (kg)'] = artemis_mission['Payload (kg)'] * sample_payload_ratio
print("\nVoorspelling artemis ")
print(artemis_mission)

# Voorspelling Gemiddelde
artemis_mission['Estimated sample weight (kg)'] = (artemis_mission['Sample weight from payload (kg)'] + artemis_mission[
    'Sample weight from total (kg)']) / 2
print("\nVoorspelling gemiddelde ")
print(artemis_mission)

# Maan stenen prioriteren
rock_samples['Remaining (kg)'] = rock_samples['Weight (kg)'] * (rock_samples['Pristine (%)'] * .01)
print("\nRemaining (kg) Maan stenen")
print(rock_samples.head(10))

# use .describe with big datasets.
print("\n.describe() rock_samples")
print(rock_samples.describe())

# Samples that have been used alot
low_samples = rock_samples.loc[(rock_samples['Weight (kg)'] >= .16) & (rock_samples['Pristine (%)'] <= 50)]
print("\nlow samples")
print(low_samples.head())

print("\ninfo")
low_samples.info()

print("\nunique from low_sample")
print(low_samples.Type.unique())

print("\nunique from rock sample")
print(rock_samples.Type.unique())

print("\nHoeveel van elk type")
print(low_samples.groupby('Type')['Weight (kg)'].count())

# Top 2
print("\n2 meest voor komende steen soorten info")
needed_samples = low_samples[low_samples['Type'].isin(['Basalt', 'Breccia'])]
needed_samples.info()
print("\n2 meest voor komende steen soorten")
print(needed_samples)

print("\n Sum of needed samples")
print(needed_samples.groupby('Type')['Weight (kg)'].sum())

print("\n Sum of rock samples")
print(rock_samples.groupby('Type')['Weight (kg)'].sum())

print("\nCrustal is low, add it to needed samples")
needed_samples = needed_samples.append(rock_samples.loc[rock_samples['Type'] == 'Crustal'])
# FutureWarning: The frame.append method is deprecated and will be removed from pandas

needed_samples_overview = pd.DataFrame()
needed_samples_overview['Type'] = needed_samples.Type.unique()
print("\n overvieuw needed samples")
print(needed_samples_overview)

# totaal gewicht needed samples
print("\ntotaal gewicht needed samples")
needed_sample_weights = needed_samples.groupby('Type')['Weight (kg)'].sum().reset_index()
needed_samples_overview = pd.merge(needed_samples_overview, needed_sample_weights, on='Type')
needed_samples_overview.rename(columns={'Weight (kg)': 'Total weight (kg)'}, inplace=True)
print(needed_samples_overview)

# gemiddelde gewicht steen soort
print("\ngemiddeld gewicht per steen soort in needes samples")
needed_sample_ave_weights = needed_samples.groupby('Type')['Weight (kg)'].mean().reset_index()
needed_samples_overview = pd.merge(needed_samples_overview, needed_sample_ave_weights, on='Type')
needed_samples_overview.rename(columns={'Weight (kg)': 'Average weight (kg)'}, inplace=True)
print(needed_samples_overview)

# totaal samples en percentage
total_rock_count = rock_samples.groupby('Type')['ID'].count().reset_index()
needed_samples_overview = pd.merge(needed_samples_overview, total_rock_count, on='Type')
needed_samples_overview.rename(columns={'ID': 'Number of samples'}, inplace=True)
total_rocks = needed_samples_overview['Number of samples'].sum()
needed_samples_overview['Percentage of rocks'] = needed_samples_overview['Number of samples'] / total_rocks
print("totaal samples en percentage")
print(needed_samples_overview)

# terug koppelen naar schatting voor artemis missie
print("\nterug koppelen naar schatting voor artemis missie")
artemis_ave_weight = artemis_mission['Estimated sample weight (kg)'].mean()
print(artemis_ave_weight, " geschat gemiddelde gewicht artemis missie")

#Hoeveel van de needed samples moet er dan verzameld worden. als je alleen needed samples gaat verzamelen
print("\nHoeveel van de needed samples moet er dan verzameld worden. als je alleen needed samples gaat verzamelen")
needed_samples_overview['Weight to collect'] = needed_samples_overview['Percentage of rocks'] * artemis_ave_weight
needed_samples_overview['Rocks to collect'] = needed_samples_overview['Weight to collect'] / needed_samples_overview['Average weight (kg)']
print(needed_samples_overview)

