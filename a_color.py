import time
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import database_master as db_mast
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(layout="wide")  # Set wide layout

# user_input = st.text_input("Enter your name:")  # Request user input with a label
# if user_input:
#     st.write(f"Hello, {user_input}!")
# color_choice = st.selectbox("Choose a color:", ("Red", "Green", "Blue"))
# if color_choice:  # Check if a color is selected
#     st.write(f"You selected the color: {color_choice}")
# agree_checkbox1 = st.checkbox("Option 1 (more descriptive label)")
# agree_checkbox2 = st.checkbox("Option 2 (more descriptive label)")
# if agree_checkbox1:
#     st.write("You agreed to Option 1")
# if agree_checkbox2:
#     st.write("You agreed to Option 2")

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

    query = f""" 
    WITH RankedData AS (
        SELECT 
            [symbol],
            [ltp],
            [sno],
            [rank],
            [rank]-[sno] as 'rank-sno',
            [low_price],
            [high_price],
            [open_price],
            [prev_close_price],
            [chp],
            [vol_traded_today],
            [inserted_at],
            ROW_NUMBER() OVER (PARTITION BY [symbol] ORDER BY ABS(chp) DESC) AS rn
        FROM [algoMaster].[dbo].[stock_live_data]
        WHERE CAST(inserted_at AS DATE) = '2024-12-26'
          AND batch = {batch_counter} AND ltp > 30
    )
    SELECT TOP (20)
        [symbol],
        [ltp],
        [sno],
        [rank],
        [rank-sno],
        [low_price],
        [high_price],
        [open_price],
        [prev_close_price],
        [chp],
        [vol_traded_today],
        [inserted_at]
    FROM RankedData
    WHERE rn = 1
    ORDER BY [rank-sno] DESC
    """
    print(query)

    # Fetch data from the database
    data, columns = db_mast.get_data_algoMaster1(query)

    if not data or not columns:
        print("No data found, maybe date changed (inserted_at not matching with given date)")
        return pd.DataFrame()  # Return empty DataFrame

    try:
        df = pd.DataFrame.from_records(data, columns=columns)
        # df['Open Chart'] = df['symbol'].apply(lambda x: make_clickable(x))
        return df

    except Exception as e:
        print(f"Error loading data into DataFrame: {e}")
        return pd.DataFrame()

def make_clickable(symbol):
    chart_url = f"https://trade.fyers.in/?funcName=openChart&symbolName={symbol.replace(':', '%3A')}"
    return chart_url

data = fetch_data_from_database()
if not data.empty:
    # st.dataframe(data, use_container_width=True, height=800)
    df = pd.DataFrame(data)
    df["Open Chart"] = df["symbol"].apply(lambda x: make_clickable(x))

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("Open Chart", cellRenderer="function(params){ return "
                                                   "`<a href='${params.value}' target='_blank'>Open Chart</a>` }")
    grid_options = gb.build()

    AgGrid(df, gridOptions=grid_options, height=800, width="100%")
else:
    st.error("No data found.")

# with st.spinner('Fetching data...'):
#     st_autorefresh(interval=3000, key="my_component_key")
#
# st.write(data)