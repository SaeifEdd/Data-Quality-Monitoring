import duckdb
import streamlit as st
import plotly_express as px

# create database connexion
con = duckdb.connect(database="data/filtered_data.duckdb", read_only=False)

# create table
data_path = "data/filtered/filtered_data.parquet"
con.execute(
    f"create or replace table store_data as select * from read_parquet('{data_path}')"
)

st.write(
    """
    Store Sensor Data Show
    """
)

# select your store and sensor
stores_query = "select store_id, sensor_id from store_data"
stores_ids = con.execute(stores_query).df()
with st.sidebar:

    # stores menu
    selected_store = st.selectbox(
        "What sensor you want to check?",
        sorted(stores_ids["store_id"].unique()),
        index=1,
        placeholder="Select your store",
    )
    st.write("You selected:", selected_store)

    # sensors menu
    selected_sensor = st.selectbox(
        "What sensor you want to check?",
        sorted(stores_ids["sensor_id"].unique()),
        index=1,
        placeholder="Select your sensor",
    )

    st.write("You selected:", selected_sensor)


# display data of selected store and sensor
# unique date
query = (
    f"select distinct on (date) date, nb_visitors, daily_store_sensor_traffic, last_4_day_avg, pct_change "
    f"from store_data where store_id = '{selected_store}' and sensor_id = {selected_sensor}"
    f"order by date"
)
df = con.execute(query).df()
st.dataframe(df)

# display daily sensor visitors
x_col = "date"
y_col = "daily_store_sensor_traffic"
plot = px.line(df, x=x_col, y=y_col)
st.plotly_chart(plot)

# display last 4 same day average number of visitors
x_col = "date"
y_col = "last_4_day_avg"
plot = px.line(df, x=x_col, y=y_col)
st.plotly_chart(plot)
