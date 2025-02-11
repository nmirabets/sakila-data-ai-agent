import os
import uuid
import streamlit as st
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

# Define the tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                    },
                    "required": ["location"]
                },
            },
    },
    {
        "type": "function",
        "function": {
            "name": "get_data_df",
            "description": "Get data from the database and return a pandas dataframe",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"}
                },
                "required": ["sql_query"]
            },
        },
    },
]

# Define the weather tool python function
def get_weather(location):
    # Here we simulate the weather function with hardcoded values, just for testing
    return f"The weather in {location} is sunny and 22°C"

# Define the get_data_df tool python function
def get_data_df(sql_query):
    # Create SQL engine
    password = os.getenv("DB_PASSWORD")
    connection_string = 'mysql+pymysql://root:' + password + '@localhost/sakila'
    engine = create_engine(connection_string)
    # Execute query and create dataframe
    with engine.connect() as connection:    
        sql_query = text(sql_query)
        result = connection.execute(sql_query)
        df = pd.DataFrame(result.all())
        # Show the SQL query
        expander = st.expander("SQL Query")
        expander.write(sql_query)
        # Show the dataframe
        st.dataframe(df)
    return "Found the data you were looking for."

