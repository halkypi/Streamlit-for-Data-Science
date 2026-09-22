from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1]

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.title("SF Trees Map")

trees_df = pd.read_csv(DATA_DIR / "trees.csv")
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.head(n=100)

lat_avg = trees_df["latitude"].mean()
lon_avg = trees_df["longitude"].mean()
m = folium.Map(location=[lat_avg, lon_avg], zoom_start=12)

for _, row in trees_df.iterrows():
    # Vector markers avoid an extra remote marker-icon dependency.
    folium.CircleMarker(
        [row["latitude"], row["longitude"]], radius=5, fill=True, fill_opacity=0.8,
    ).add_to(m)

events = st_folium(m, key="tree_map", returned_objects=["last_object_clicked"])
st.write(events)
