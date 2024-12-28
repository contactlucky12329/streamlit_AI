import time
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import database_master as db_mast
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def fetch_batch_counter(filename="default_name_batch_counter.txt"):
    try:
        with open(filename, 'r') as file:
            counter = file.read().strip()
            return int(counter) if counter else 1
    except FileNotFoundError:
        print(f"{filename} not found. Starting from batch 1.")
        return 1
    except ValueError:
        print(f"Nothing in {filename}. Starting from batch 1.")
        return 1

# Fetch data from the database and create the DataFrame with the "Open Chart" link
def fetch_data_from_database():
    batch_counter = fetch_batch_counter("batch_counter_websocket.txt")
    print(f"Batch counter running = {batch_counter}")

    query = f""" SELECT [symbol],[currentDate]
      ,[sno]
      ,[rank]
      ,[ltp]
      ,[chp]
      ,[vol_traded_today]
      ,[low_price]
      ,[high_price]
      ,[open_price]
      ,[prev_close_price] FROM [algoMaster].[dbo].[stock_rank_master]
    where stocks_type='VOLATILE' AND [vol_traded_today]>0
"""
    print(query)

    # Fetch data from the database
    data, columns = db_mast.get_data_algoMaster1(query)

    if not data or not columns:
        print("No data found, maybe date changed (inserted_at not matching with given date)")
        return pd.DataFrame()  # Return empty DataFrame

    try:
        df = pd.DataFrame.from_records(data, columns=columns)
        return df

    except Exception as e:
        print(f"Error loading data into DataFrame: {e}")
        return pd.DataFrame()


data = fetch_data_from_database()
if not data.empty:
    # st.dataframe(data, use_container_width=True, height=800)
    df = pd.DataFrame(data)
    AgGrid(df, height=800, width="100%")
else:
    st.error("No data found.")

# with st.spinner('Fetching data...'):
#     st_autorefresh(interval=3000, key="my_component_key")
#
# st.write(data)