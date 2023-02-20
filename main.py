import osmnx as ox
import geopandas as gpd
import pandas as pd
import sqlite3
import datetime

city = "Lviv, Ukraine"

city_boundary = ox.geometries_from_place(city, tags={"boundary": "administrative"})

buildings = ox.geometries_from_place(city, tags={"building": True})

buildings = gpd.sjoin(buildings, city_boundary, how="left", op="within")

numbers = []
streets = []
areas = []

for i, row in buildings.iterrows():
    number = row.get("addr:housenumber")
    if type(number) == float:
        number = 'Unknown'
    numbers.append(number)

    street = row.get("addr:street")
    if type(street) == float:
        street = 'Unknown'
    streets.append(street)

    area = row.get("name_right")
    if type(area) == float:
        area = 'Unknown'
    areas.append(area)

data = {"Number of Building": numbers, "Street": streets, "Area": areas}
df = pd.DataFrame(data)

mask = df.apply(lambda row: 'Unknown' in row.values, axis=1)

df = df[~mask]
conn = sqlite3.connect('identifier.sqlite')
c = conn.cursor()
conn = sqlite3.connect('database.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE users2 (id INTEGER PRIMARY KEY, Name TEXT, 
              Last_Name TEXT, 
              Street TEXT, 
              Building_Number TEXT, 
              Area TEXT, 
              Time DATETIME)''')
except sqlite3.OperationalError:
    pass

def find_area(building_number, street_name, df):
    area = df.loc[(df['Street'] == street_name) & (df['Number of Building'] == building_number), 'Area']
    return area


def insert_data(name, last_name, building_number, street_name, df):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    area = find_area(building_number, street_name, df)
    unique_id = str(datetime.datetime.now().timestamp()).replace('.', '')[:8]
    c.execute("INSERT INTO users2 VALUES (?, ?, ?, ?, ?, ?, ?)",
              (unique_id, name, last_name, street_name, building_number, str(area), time))
    conn.commit()


insert_data('Misha', 'Dik', 'Білогорща вулиця', '98а', df)
