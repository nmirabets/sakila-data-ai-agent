import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from ai.tools import get_data_df_local, get_data_df_cloud
from ai.tools import TOOLS


load_dotenv()

def agent(messages):

    client = OpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1",
    )

    completion = client.chat.completions.create(
        model="grok-3-mini",
        tools=TOOLS, # here we pass the tools to the LLM
        messages=messages,
    )

    # Get the response from the LLM
    response = completion.choices[0].message

    # Parse the response to get the tool call arguments
    if response.tool_calls:
        # Process each tool call
        for tool_call in response.tool_calls:
            # Get the tool call arguments
            tool_call_arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "get_data_df":
                return get_data_df_local(tool_call_arguments["sql_query"])
    else:
        # If there are no tool calls, return the response content
        return response.content