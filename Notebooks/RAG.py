# %% BLOCK 1: Imports and Environment Setup
import os
import requests
import logging
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_community.vectorstores import FAISS
import faiss
import numpy as np

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the LLM instance for use in parameter determination
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)



# %% BLOCK 2: Tool Definitions

@tool
def query_wolfram_alpha(query: str) -> str:
    """Use Wolfram Alpha to compute mathematical expressions or retrieve information."""
    try:
        # Replace with actual Wolfram Alpha API call if needed
        return f"Wolfram Alpha result for: {query}"
    except Exception as e:
        logging.error(f"Error querying Wolfram Alpha: {e}")
        return f"Error: {str(e)}"

@tool
def trigger_zapier_webhook(webhook_url: str, data: dict = None) -> str:
    """Trigger a Zapier webhook to execute predefined automated workflows."""
    try:
        response = requests.post(webhook_url, json=data or {})
        return f"Webhook triggered successfully: {response.status_code}"
    except Exception as e:
        logging.error(f"Error triggering Zapier webhook: {e}")
        return f"Error: {str(e)}"

@tool
def send_slack_message(channel: str, message: str) -> str:
    """Send messages to specific Slack channels to communicate with team members."""
    try:
        # Replace with actual Slack API call if needed
        return f"Message sent to {channel}: {message}"
    except Exception as e:
        logging.error(f"Error sending Slack message: {e}")
        return f"Error: {str(e)}"



# %% BLOCK 3: Embeddings and Vector Store Setup

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# Tool descriptions
tool_descriptions = {
"query_wolfram_alpha": '''Use Wolfram Alpha to compute mathematical
expressions or retrieve information.''',
"trigger_zapier_webhook": '''Trigger a Zapier webhook to execute
predefined automated workflows.''',
"send_slack_message": '''Send messages to specific Slack channels to
communicate with team members.'''
}



# %% BLOCK 4: Create Embeddings and Build FAISS Index

# Create embeddings for each tool description
tool_embeddings = []
tool_names = []

for tool_name, description in tool_descriptions.items():
    embedding = embeddings.embed_query(description)
    tool_embeddings.append(embedding)
    tool_names.append(tool_name)

# Initialize FAISS vector store
dimension = len(tool_embeddings[0])
index = faiss.IndexFlatL2(dimension)

# Normalize embeddings for cosine similarity
faiss.normalize_L2(np.array(tool_embeddings).astype('float32'))

# Convert list to FAISS-compatible format
tool_embeddings_np = np.array(tool_embeddings).astype('float32')
index.add(tool_embeddings_np)

# Map index to tool functions
index_to_tool = {
    0: query_wolfram_alpha,
    1: trigger_zapier_webhook,
    2: send_slack_message
}



# %% BLOCK 5: Function to Retrieve Relevant Tools Based on User Query

def select_tool(query: str, top_k: int = 1) -> list:
    """
    Select the most relevant tool(s) based on the user's query using
    vector-based retrieval.
    Args:
    query (str): The user's input query.
    top_k (int): Number of top tools to retrieve.
    Returns:
    list: List of selected tool functions.
    """
    query_embedding = embeddings.embed_query(query)
    query_embedding = np.array(query_embedding).astype('float32')
    faiss.normalize_L2(query_embedding.reshape(1, -1))
    D, I = index.search(query_embedding.reshape(1, -1), top_k)
    selected_tools = [index_to_tool[idx] for idx in I[0] if idx in index_to_tool]
    return selected_tools



# %% BLOCK 6: Function to Determine Parameters for Selected Tool

def determine_parameters(query: str, tool_name: str) -> dict:
    """
    Use the LLM to analyze the query and determine the parameters for the tool
    to be invoked.
    Args:
    query (str): The user's input query.
    tool_name (str): The selected tool name.
    Returns:
    dict: Parameters for the tool.
    """
    messages = [
    HumanMessage(content=f'''Based on the user's query: '{query}', what
    parameters should be used for the tool '{tool_name}'?''')
    ]
    # Call the LLM to extract parameters
    response = llm(messages)
    # Example logic to parse response from LLM
    parameters = {}
    if tool_name == "query_wolfram_alpha":
        parameters["expression"] = response['expression']
    # Extract mathematical expression
    elif tool_name == "trigger_zapier_webhook":
        parameters["zap_id"] = response.get('zap_id', "123456")
        parameters["payload"] = response.get('payload', {"data": query})
    elif tool_name == "send_slack_message":
        parameters["channel"] = response.get('channel', "#general")
        parameters["message"] = response.get('message', query)
    return parameters




# %% BLOCK 7: Example Usage

# Example user query
user_query = "Solve this equation: 2x + 3 = 7"
# Select the top tool
selected_tools = select_tool(user_query, top_k=1)
tool_name = selected_tools[0] if selected_tools else None

if tool_name:
# Use LLM to determine the parameters based on the query and the selected tool
    args = determine_parameters(user_query, tool_name)

# Invoke the selected tool
    try:

        # Assuming each tool has an `invoke` method to execute it
        tool_result = globals()[tool_name].invoke(args)
        print(f"Tool '{tool_name}' Result: {tool_result}")
    except ValueError as e:
        print(f"Error invoking tool '{tool_name}': {e}")
else:
    print("No tool was selected.")

