import streamlit as st
import pandas as pd
import database_master as db_mast
st.title("Lakhwinder")


response = st.sidebar.selectbox("Take your position",("BUY","SELL" ))

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


def fetch_data_from_database():
    batch_counter = fetch_batch_counter("batch_counter_websocket.txt")
    print(f"Batch counter running = {batch_counter}")
    query = f"""  WITH RankedData AS (
        SELECT
            [symbol],
            [ltp],
                [sno],
                [rank],
            [low_price],
            [high_price],
            [upper_ckt],
            [lower_ckt],
            [open_price],
            [prev_close_price],
            [chp],
            [vol_traded_today],
            [last_traded_time],
            [exch_feed_time],
            [inserted_at],
            [batch],
            ROW_NUMBER() OVER (PARTITION BY [symbol] ORDER BY ABS(chp) DESC) AS rn
        FROM [algoMaster].[dbo].[stock_live_data]
        WHERE CAST(inserted_at AS DATE) = '2024-12-26'
          AND batch = 1 and ltp > 30
        )
            SELECT TOP (20)
                [symbol],
                [ltp],
                        [sno],
                        [rank],
                [low_price],
                [high_price],
                [upper_ckt],
                [lower_ckt],
                [open_price],
                [prev_close_price],
                [chp],
                [vol_traded_today],
                [last_traded_time],
                [exch_feed_time],
                [inserted_at],
                [batch]
            FROM RankedData
            WHERE rn = 1
            ORDER BY  ABS(chp) DESC
          """
    print(query)
    data, columns = db_mast.get_data_algoMaster1(query)
    # print(data)
    if not data or not columns:
        print("No data found, may be date changed (inserted_at not matching with given date)")
        return []

    try:
        df = pd.DataFrame.from_records(data, columns=columns)
        df['sno'] = range(1, len(df) + 1)  # Reset 'sno'
        df = df.sort_values(by='sno', ascending=True)
        stock_data1 = df.to_dict(orient='records')
        # st.write(stock_data1)
        return stock_data1
    except Exception as e:
        print(f"Error loading data into DataFrame: {e}")
        return []
def make_clickable(link):
    # Target="_blank" opens the link in a new tab
    return f'<a target="_blank" href="{link}">Open Chart</a>'

#
if st.button("Fetch Data"):
    data = fetch_data_from_database()
    if data is not None:
        # data['Open_Chart'] = data['Chart_Link_Column'].apply(make_clickable)

        st.table(data)
