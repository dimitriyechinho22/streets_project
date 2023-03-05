import osmnx as ox
import geopandas as gpd
import pandas as pd


city = "Lviv, Ukraine"

city_boundary = ox.geometries_from_place(city, tags={"boundary": "administrative"})
buildings = ox.geometries_from_place(city, tags={"building": True})
buildings = gpd.sjoin(buildings, city_boundary, how="left", op="within")

df = pd.DataFrame()
df["Number of Building"] = buildings["addr:housenumber"].fillna("Unknown")
df["Street"] = buildings["addr:street"].fillna("Unknown")
df["Area"] = buildings["name_right"].fillna("Unknown")

df = df[df["Area"].str.contains("район")]