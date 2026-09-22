from importlib.util import find_spec

import streamlit as st

st.title("Hugging Face Demo")
st.caption("English movie-review sentiment; model scores are not calibrated certainty.")
text = st.text_input("Enter text to analyze")
MODEL = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REVISION = "714eb0fa89d2f80546fda750413ed43d93601a13"


@st.cache_resource(max_entries=1)
def get_model():
    from transformers import pipeline
    return pipeline("text-classification", model=MODEL, revision=REVISION, device=-1)


if find_spec("transformers") is None or find_spec("torch") is None:
    st.info("Install the NLP extra with uv sync --extra nlp to run local sentiment analysis.")
elif st.button("Analyze locally", disabled=not text.strip()):
    try:
        result = get_model()(text, truncation=True)[0]
    except OSError:
        st.error("The model could not be loaded. Check Hugging Face access and the local model cache.")
    else:
        st.write("Sentiment:", result["label"])
        st.write("Model score:", result["score"])

st.title("OpenAI Version")
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key = None

if not api_key:
    st.info("The local lesson works without an API key. Add OPENAI_API_KEY to .streamlit/secrets.toml for this section.")
elif find_spec("openai") is None:
    st.info("Install the NLP extra with uv sync --extra nlp for this section.")
else:
    from openai import APIError, OpenAI
    system_message = st.text_area(
        "Enter a System Message to instruct OpenAI",
        "Classify the sentiment of the text and explain your assessment briefly.",
    )
    model_name = st.text_input("OpenAI model available to your account")
    if st.button("Analyze with OpenAI", disabled=not (text.strip() and model_name.strip())):
        try:
            with OpenAI(api_key=api_key, timeout=30, max_retries=0) as client:
                response = client.responses.create(
                    model=model_name.strip(), instructions=system_message, input=text,
                )
            st.write(response.output_text)
        except APIError:
            st.error("OpenAI request failed. Check the model name, account access, quota and connectivity.")
