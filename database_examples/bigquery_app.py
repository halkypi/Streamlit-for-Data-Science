import streamlit as st
from queries import get_streamlit_pypi_data

st.title("BigQuery App")
try:
    account_info = dict(st.secrets["bigquery_service_account"])
except (FileNotFoundError, KeyError):
    st.info("Add a [bigquery_service_account] table to .streamlit/secrets.toml to query BigQuery.")
    st.stop()

from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import GoogleAuthError
from google.cloud import bigquery
from google.oauth2 import service_account


@st.cache_resource(ttl=3600, scope="session")
def get_bigquery_client(info):
    credentials = service_account.Credentials.from_service_account_info(info)
    return bigquery.Client(credentials=credentials, project=info.get("project_id"))


@st.cache_data(ttl=600, max_entries=30, scope="session")
def get_dataframe_from_sql(query):
    return get_bigquery_client(account_info).query(query).to_dataframe(create_bqstorage_client=False)


days_lookback = st.slider("How many days of data do you want to see?", 1, 30, 5)
try:
    downloads_df = get_dataframe_from_sql(get_streamlit_pypi_data(days_lookback))
except (GoogleAPIError, GoogleAuthError, ValueError):
    st.error("BigQuery could not complete the query. Check service-account configuration, permissions and connectivity.")
    st.stop()
st.line_chart(downloads_df, x="file_downloads_timestamp_date", y="file_downloads_count")
