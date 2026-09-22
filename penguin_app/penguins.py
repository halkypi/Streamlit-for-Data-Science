import altair as alt
import pandas as pd
import streamlit as st

st.title("Palmer's Penguins")
st.markdown("Use this Streamlit app to make your own scatterplot about penguins!")

selected_x_var = st.selectbox(
    "What do you want the x variable to be?",
    ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
)
selected_y_var = st.selectbox(
    "What about the y?",
    ["bill_depth_mm", "bill_length_mm", "flipper_length_mm", "body_mass_g"],
)

penguin_file = st.file_uploader("Select Your Local Penguins CSV", type=["csv"])
if penguin_file is not None:
    try:
        penguins_df = pd.read_csv(penguin_file)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as error:
        st.error(f"Please upload a readable CSV: {error}")
        st.stop()
    required = {selected_x_var, selected_y_var, "species"}
    if not required.issubset(penguins_df.columns):
        st.error(f"CSV must include: {', '.join(sorted(required))}")
        st.stop()
    for column in {selected_x_var, selected_y_var}:
        penguins_df[column] = pd.to_numeric(penguins_df[column], errors="coerce")
else:
    st.info("Upload penguin_app/penguins.csv to start plotting.")
    st.stop()

alt_chart = (
    alt.Chart(penguins_df, title="Scatterplot of Palmer's Penguins")
    .mark_circle()
    .encode(
        x=selected_x_var,
        y=selected_y_var,
        color="species",
    )
    .interactive()
)
st.altair_chart(alt_chart, width="stretch")
