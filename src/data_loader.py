from snowflake.connector import SnowflakeConnection
import snowflake
import pandas as pd


def load(conn: SnowflakeConnection = None) -> pd.DataFrame:
    # Create connection if none was passed
    if conn is None:
        conn = snowflake.connector.connect()

    # retrieve and return data
    with conn as ctx:
        df = ctx.cursor().fetch_pandas_all("SELECT * FROM TABLE")

    # Use pythonic naming convention for column names
    df.columns = df.columns.str.lower()
    return df
