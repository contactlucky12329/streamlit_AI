import pyodbc

import pandas as pd

# Connection strings
# cn = "DRIVER=SQL Server;SERVER=DESKTOP-DIPRBHN\\MSSQLSERVER1;DATABASE=fyersAlgo;Trusted_Connection=yes;"
# cn1 = "DRIVER=SQL Server;SERVER=DESKTOP-DIPRBHN\\MSSQLSERVER1;DATABASE=dhanAlgo;Trusted_Connection=yes;"
# cn2 = 'DRIVER={SQL Server};SERVER=DESKTOP-DIPRBHN\\MSSQLSERVER1;DATABASE=algoMaster;UID=sa;PWD=Lucky;MARS_Connection=Yes'
cn = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LKV07EB;DATABASE=fyersAlgo;Trusted_Connection=yes;MARS_Connection=Yes'
cn1 = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LKV07EB;DATABASE=dhanAlgo;Trusted_Connection=yes;MARS_Connection=Yes'
cn2 = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LKV07EB;DATABASE=algoMaster;Trusted_Connection=yes;MARS_Connection=Yes'

# Functions

def insert_query(sql_query):
    try:
        with pyodbc.connect(cn) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
    except Exception as e:
        print("Error:", e)


def insert_query_algoMaster(sql_query):
    try:
        with pyodbc.connect(cn2) as conn2:
            cursor2 = conn2.cursor()
            response = cursor2.execute(sql_query)
            conn2.commit()
            return response
    except Exception as e:
        print("Error:", e)


def insert_query_for_dhan(sql_query):
    try:
        with pyodbc.connect(cn1) as conn1:
            cursor1 = conn1.cursor()
            cursor1.execute(sql_query)
            conn1.commit()
    except Exception as e:
        print("Error:", e)


def get_data(sql_query):
    try:
        with pyodbc.connect(cn) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            records = cursor.fetchall()
            return records
    except Exception as e:
        print("Error:", e)


def get_data_read_sql(sql_query):
    try:
        with pyodbc.connect(cn1) as conn1:
            df_db = pd.read_sql(sql_query, conn1)
            return df_db
    except Exception as e:
        print("Error:", e)



def get_data_read_sql_algo(sql_query):
    try:
        with pyodbc.connect(cn2) as conn2:
            df_db = pd.read_sql(sql_query, conn2)
            return df_db
    except Exception as e:
        print("Error:", e)



def get_data_algoMaster(sql_query):
    try:
        with pyodbc.connect(cn2) as conn2:
            cursor2 = conn2.cursor()
            cursor2.execute(sql_query)
            records = cursor2.fetchall()
            return records
    except Exception as e:
        print("Error:", e)


def get_data_algoMaster1(sql_query):
    try:
        with pyodbc.connect(cn2) as conn2:
            cursor = conn2.cursor()
            cursor.execute(sql_query)
            records = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return records, columns
    except Exception as e:
        print("Error:", e)


def get_dhan_data(sql_query):
    try:
        with pyodbc.connect(cn1) as conn1:
            cursor = conn1.cursor()
            cursor.execute(sql_query)
            records = cursor.fetchall()
            return records
    except Exception as e:
        print("Error:", e)


def delete_table_records(sql_query):
    try:
        with pyodbc.connect(cn) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
            print("Data deleted successfully")
    except Exception as e:
        print("Error:", e)


def update_table(sql_query):
    try:
        with pyodbc.connect(cn) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
    except Exception as e:
        print("Error:", e)


def pcr_form_data(sql_qr):
    try:
        with pyodbc.connect(cn) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_qr)
            records = cursor.fetchall()
            records_list = [record for record in records]  # Convert to list of tuples
            return records_list
    except Exception as e:
        print("Error:", e)


def get_sno(query):
    sno = 0
    data = get_data(query)
    if data:
        sno = data[0][0]
    else:
        sno = 0
    sno += 1
    return sno


def insert_data_with_parameters(query, params=None):
    try:
        with pyodbc.connect(cn2) as conn2:
            cursor = conn2.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn2.commit()
    except Exception as e:
        print("Error:", e)


def get_data_with_parameters(query, params=None):
    try:
        with pyodbc.connect(cn2) as conn2:
            cursor = conn2.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print("Error:", e)


def insert_live_data_using_pandas(insert_query, row):
    """
    Function to insert the DataFrame into SQL Server using pyodbc.
    """
    try:
        if row.empty:
            print("The DataFrame is empty. No data to insert.")
            return

        row_tuple = tuple(row)
        with pyodbc.connect(cn2) as conn2:
            cursor = conn2.cursor()
            cursor.execute(insert_query, row_tuple)
            conn2.commit()
    except Exception as e:
        print("Error:", e)
