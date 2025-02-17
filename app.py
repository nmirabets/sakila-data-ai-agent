########################################################
# Import libraries
########################################################
import streamlit as st
from agent.agent import agent
from agent.prompts import SYSTEM_PROMPT

########################################################
# Streamlit app Title
########################################################
st.title("💬 Sakila Data Agent")

########################################################
# Initialize session state
########################################################
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", 
         "content": SYSTEM_PROMPT},
        {"role": "assistant", 
         "content": "How can I help you?"}
    ]

########################################################
# Display messages
########################################################
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

########################################################
# Get user input
########################################################
if prompt := st.chat_input():

    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    st.chat_message("user").write(prompt)
    
    # Get agent response
    msg = agent(st.session_state.messages)

    # Add agent response to session state
    st.session_state.messages.append({"role": "assistant", "content": msg})
    # Display agent response
    st.chat_message("assistant").write(msg)