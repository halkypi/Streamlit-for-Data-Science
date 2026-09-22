from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1]

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events

st.title("Streamlit Plotly Events Example: Penguins")
df = pd.read_csv(DATA_DIR / "penguins.csv")


fig = px.scatter(df, x="bill_length_mm", y="bill_depth_mm", color="species",
                 color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"])
# This component bundles older Plotly.js, which needs JSON lists, not typed arrays.
for trace in fig.data:
    x, y = list(trace.x), list(trace.y)
    # Clear first: Plotly can otherwise retain an equal NumPy array internally.
    trace.x = None
    trace.y = None
    trace.x = x
    trace.y = y
selected_point = plotly_events(fig, click_event=True, key="penguin_click")
if len(selected_point) == 0:
    st.stop()

selected_x_value = selected_point[0]["x"]
selected_y_value = selected_point[0]["y"]

df_selected = df[
    (df["bill_length_mm"] == selected_x_value)
    & (df["bill_depth_mm"] == selected_y_value)
]
st.write("Data for selected point:")
st.write(df_selected)
