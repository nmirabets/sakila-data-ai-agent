########################################################
# This is a starter template to develop the Sakila Data AI Agent. Use the concepts learned in the Developer Guide to build the full application.
########################################################

import streamlit as st
from dotenv import load_dotenv
from ai.agent import agent
from ai.prompts import SYSTEM_PROMPT
import pandas as pd
from ai.utils import upload_data, drop_all_tables, get_database_schema

load_dotenv()

st.title("📊 Data Agent")
st.caption("🚀 A Streamlit Data Analytics Agent")

if "file" not in st.session_state:

    drop_all_tables()

    # File uploader (this will persist the uploaded file in session state)
    uploaded_file = st.file_uploader("Upload a file to analyze", type=["csv"])

    if uploaded_file is not None:
        # Store the file in session state
        st.session_state["file"] = uploaded_file
        
        # Read the file and convert it to a pandas dataframe
        df = pd.read_csv(uploaded_file)
        # Add a spinner to the page
        with st.spinner("Creating table..."):
            # Upload the file to the database   
            result = upload_data(df)
            st.success(result)
            st.button("Continue to talk to the agent")
else:
    if "messages" not in st.session_state:
        # Get the database schema
        database_schema = get_database_schema()
        SYSTEM_PROMPT = SYSTEM_PROMPT.format(database_schema=database_schema)
        st.session_state["messages"] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state["messages"][1:]:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        # Add the user's message to the conversation & display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = agent(st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)