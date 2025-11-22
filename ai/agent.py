import json
from dotenv import load_dotenv
from openai import OpenAI
from ai.tools import get_data_df
from ai.tools import TOOLS


load_dotenv()

def agent(messages):

    # Initialize the OpenAI client
    client = OpenAI()

    # Make a ChatGPT API call with tool calling
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
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
                return get_data_df(tool_call_arguments["sql_query"])
    else:
        # If there are no tool calls, return the response content
        return response.content