from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from penguins_ml import ISLANDS, SEXES, NUMERIC, encode_features, train_model

st.title("Penguin Classifier")
st.write("Use six measurements to predict penguin species with a reproducible random forest.")
st.caption("Teaching password: streamlit_is_great (this is not authentication).")
if st.text_input("What is the Password?", type="password") != "streamlit_is_great":
    st.stop()

penguin_file = st.file_uploader("Upload your own penguin data", type=["csv"])
try:
    penguin_df = pd.read_csv(penguin_file if penguin_file is not None else Path(__file__).resolve().parent / "penguins.csv")
except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as error:
    st.error(f"Please upload a readable CSV: {error}")
    st.stop()


@st.cache_data(ttl=3600, max_entries=4)
def fit_classifier(data):
    # Cache by data content: widget reruns do not retrain the same dataset.
    return train_model(data)


try:
    model, species, score = fit_classifier(penguin_df)
except ValueError as error:
    st.error(str(error))
    st.stop()
st.write(f"Held-out accuracy: {score:.1%}")
st.caption("Trained with the current environment; the historical pickles are not loaded.")

with st.form("user_inputs"):
    island = st.selectbox("Penguin Island", ISLANDS)
    sex = st.selectbox("Sex", SEXES)
    bill_length = st.number_input("Bill Length (mm)", min_value=1.0, value=44.0)
    bill_depth = st.number_input("Bill Depth (mm)", min_value=1.0, value=17.0)
    flipper_length = st.number_input("Flipper Length (mm)", min_value=1.0, value=200.0)
    body_mass = st.number_input("Body Mass (g)", min_value=1.0, value=4200.0)
    submitted = st.form_submit_button("Predict species")

if not submitted:
    st.info("Adjust the measurements and submit the form to predict.")
    st.stop()

measurements = [bill_length, bill_depth, flipper_length, body_mass]
row = pd.DataFrame([dict(zip(NUMERIC, measurements), island=island, sex=sex)])
features = encode_features(row)
assert list(features.columns) == list(model.feature_names_in_)
predicted_species = species[model.predict(features)[0]]
st.subheader("Predicting Your Penguin's Species:")
st.write(f"We predict your penguin is of the {predicted_species} species")

fig, ax = plt.subplots()
sns.barplot(x=model.feature_importances_, y=model.feature_names_in_, ax=ax)
ax.set(title="Which features predict species?", xlabel="Importance")
st.pyplot(fig)
plt.close(fig)

st.write("Histograms by species; each vertical line marks your input.")
for column, value in zip(NUMERIC, measurements):
    fig, ax = plt.subplots()
    sns.histplot(data=penguin_df, x=column, hue="species", ax=ax)
    ax.axvline(value)
    st.pyplot(fig)
    plt.close(fig)
