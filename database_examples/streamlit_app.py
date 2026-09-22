import streamlit as st

st.title("Snowflake TPC-H Explorer")
try:
    connection_options = dict(st.secrets["snowflake"])
except (FileNotFoundError, KeyError):
    st.info("Add a [snowflake] table to .streamlit/secrets.toml and use the environments/snowflake uv project.")
    st.stop()

from snowflake.connector.errors import Error as SnowflakeError

sql_query = """
    SELECT l_returnflag, sum(l_quantity) AS sum_qty,
           sum(l_extendedprice) AS sum_base_price
    FROM snowflake_sample_data.tpch_sf1.lineitem
    WHERE l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
    GROUP BY 1
"""

# st.connection owns the connection cache; query's TTL bounds result staleness.
try:
    connection = st.connection("snowflake", type="snowflake", **connection_options)
    df = connection.query(sql_query, ttl=600)
except SnowflakeError:
    st.error("Snowflake query failed. Check credentials, warehouse, sample-data access and connectivity.")
    st.stop()

col_to_graph = st.selectbox("Select a column to graph", ["Order Quantity", "Base Price"])
df["SUM_QTY"] = df["SUM_QTY"].astype(float)
df["SUM_BASE_PRICE"] = df["SUM_BASE_PRICE"].astype(float)
st.bar_chart(df, x="L_RETURNFLAG", y="SUM_QTY" if col_to_graph == "Order Quantity" else "SUM_BASE_PRICE")
