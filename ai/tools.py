import os
import uuid
import streamlit as st
import json 
import pandas as pd
from dotenv import load_dotenv
from .utils import connect_to_local_database, connect_to_cloud_database
from sqlalchemy import create_engine, text


load_dotenv()

# Define the tools
TOOLS = [
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

def get_data_df_local(query):
    # Connect to database using the utils function
    conn = connect_to_local_database()
    query = text(query)
    result = conn.execute(query)
    df = pd.DataFrame(result.all())
    st.expander("SQL Query").write(query)
    st.dataframe(df)
    conn.close()
    return "✅ Found the data you were looking for."


# Define the get_data_df tool python function
def get_data_df_cloud(sql_query):
    # Connect to database using the utils function
    conn = connect_to_cloud_database()
    
    if conn is None:
        st.error("❌ Failed to connect to the database")
        return "Failed to connect to the database"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
            
            # Get column names
            column_names = [desc[0] for desc in cur.description]
            
            # Create DataFrame
            df = pd.DataFrame(results, columns=column_names)
            
            # Show the SQL query
            expander = st.expander("SQL Query")
            expander.write(sql_query)
            
            # Show the dataframe
            st.dataframe(df)
            
        return "Found the data you were looking for."
        
    except Exception as e:
        st.error(f"❌ Error executing query: {e}")
        return f"Error executing query: {e}"
    
    finally:
        conn.close()

