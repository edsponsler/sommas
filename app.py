import os
import vertexai
from dotenv import load_dotenv
import streamlit as st

# ADK and Agent Engine Imports
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp

# Import the client library for Vertex AI Search and client options
from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION (loaded from .env) ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")
MODEL = os.getenv("FAST_MODEL")
DATA_STORE_ID = os.getenv("DATA_STORE_ID")
# ---------------------------------------

# Initialize the Vertex AI SDK
# This is cached by Streamlit to avoid re-initializing on every interaction
@st.cache_resource
def load_agent():
    vertexai.init(
        project=GCP_PROJECT_ID,
        location=GCP_LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

    # Define the REAL search tool using the Discovery Engine client
    def search_knowledge_base(query: str) -> str:
        client_options = ClientOptions(
            api_endpoint="discoveryengine.googleapis.com"
        )
        client = discoveryengine.SearchServiceClient(client_options=client_options)

        serving_config = client.serving_config_path(
            project=GCP_PROJECT_ID,
            location="global",
            data_store=DATA_STORE_ID,
            serving_config="default_config",
        )

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=5,
        )

        response = client.search(request)

        results_str = ""
        for i, result in enumerate(response.results):
            doc = result.document
            content = doc.struct_data.get("content", "No content found.")
            source = doc.struct_data.get("source", "Unknown source.")
            results_str += f"Result {i+1}:\nSource: {source}\nContent: {content}\n\n"

        return results_str if results_str else "No relevant information found in the knowledge base."

    # Create the Agent with the real tool
    agent = Agent(
        model=MODEL,
        tools=[search_knowledge_base],
        name="asrr_agent"
    )

    app = AdkApp(agent=agent)
    return app

# --- Streamlit UI ---

st.title("ASRR: The Conversational Analyst")

# Load the agent and app
app = load_agent()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Define a generator function to stream the response
        def response_generator():
            system_prompt = "You are the ASRR, an expert research assistant. Your purpose is to provide clear, synthesized answers based ONLY on the context provided by the search_knowledge_base tool. Do not use any external knowledge. Cite the source for your claims."
            full_message = f"SYSTEM PROMPT: {system_prompt}\n\nUSER QUESTION: {prompt}"
            
            # Stream the response from the AdkApp
            for event in app.stream_query(message=full_message, user_id="test_user"):
                if "content" in event and "parts" in event["content"]:
                    for part in event["content"]["parts"]:
                        if "text" in part:
                            yield part["text"]
        
        response = st.write_stream(response_generator)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})