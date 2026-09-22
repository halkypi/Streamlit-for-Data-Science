from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1]

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from importlib.util import find_spec
from streamlit_lottie import st_lottie
from streamlit_plotly_events import plotly_events


@st.cache_data(ttl=3600, max_entries=8)
def load_lottieurl(url: str):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        animation = response.json()
    except (requests.RequestException, ValueError):
        return None
    return animation if isinstance(animation, dict) and "layers" in animation else None


lottie_penguin = load_lottieurl(
    "https://assets9.lottiefiles.com/private_files/lf30_lntyk83o.json"
)

if lottie_penguin is not None:
    st_lottie(lottie_penguin, height=200, speed=1.5)
else:
    st.caption("Optional animation unavailable; the lesson works without it.")

st.title("Streamlit Plotly Events + Lottie Example: Penguins")
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

st.subheader("Pandas Profiling of Penguin Dataset")
if find_spec("data_profiling") is None:
    st.info("For the profiling report, run: uv run --project environments/profiling streamlit run components_example/streamlit_app.py")
else:
    from data_profiling import ProfileReport

    @st.cache_data(ttl=3600, max_entries=2)
    def profile_html(data):
        return ProfileReport(data, explorative=True, progress_bar=False).to_html()

    if st.checkbox("Generate profiling report"):
        # Only profile the bundled teaching data, never untrusted HTML.
        st.iframe(profile_html(df), height=700)


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
