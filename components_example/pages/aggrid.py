from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1]

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.title("Streamlit AgGrid Example: Penguins")
penguins_df = pd.read_csv(DATA_DIR / "penguins.csv")
st.write("AgGrid DataFrame:")
response = AgGrid(penguins_df, height=500, editable=True, key="penguin_grid", update_on=["cellValueChanged"])
df_edited = response["data"]
st.write("Edited DataFrame:")
st.dataframe(df_edited)
