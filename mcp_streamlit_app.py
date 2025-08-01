# mcp_streamlit_app.py

import streamlit as st
import asyncio
import os
import json
from mcp_use import MCPAgent, MCPClient
from langchain_openai import ChatOpenAI
import warnings

# --- NEW: Import our robust configuration loader ---
from config import get_mcp_config

# Suppress warnings
warnings.filterwarnings("ignore")
# mcp_use.set_debug(0)

# Page configuration
st.set_page_config(
    page_title="Ultimate AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "config_loaded" not in st.session_state:
    st.session_state.config_loaded = False

def reset_chat():
    st.session_state.messages = []
    st.session_state.agent = None
    st.session_state.config_loaded = False

async def run_agent_query(agent, query):
    """Run a query through the MCP agent."""
    try:
        # --- THE FIX ---
        # Use agent.run() to get the final answer directly, just like in server.py
        result = await agent.run(query)
        return result
    except Exception as e:
        st.error(f"Error during agent execution: {e}")
        return f"An error occurred: {str(e)}"

# --- UI Sidebar ---
with st.sidebar:
    st.header("MCP Configuration")

    # --- SIMPLIFIED: Replaced the text box with a single button ---
    if st.button("Activate Configuration", type="primary", use_container_width=True):
        with st.spinner("Loading configuration from config.py..."):
            # Get the config from our new, reliable function
            config_dict = get_mcp_config()
            if not config_dict:
                st.error("Failed to load configuration from config.py.")
            else:
                try:
                    client = MCPClient.from_dict(config_dict)
                    llm = ChatOpenAI(model="gpt-4o")
                    st.session_state.agent = MCPAgent(llm=llm, client=client, max_steps=100)
                    st.session_state.config_loaded = True
                    st.success("✅ Configuration Activated!")
                except Exception as e:
                    st.error(f"Failed to create agent: {e}")
    
    if st.button("Clear Chat & Config", use_container_width=True):
        reset_chat()
        st.rerun()

    st.divider()
    st.subheader("Status")
    if st.session_state.agent and st.session_state.config_loaded:
        st.success("✅ Agent Ready")
        # Display the loaded configuration for transparency
        st.json(get_mcp_config())
    else:
        st.warning("⚠️ Configuration not activated")

# --- Main Page Content ---
st.markdown("## 100% local Ultimate AI Assistant using mcp-use")
st.markdown("Configure your MCP servers from the sidebar and chat with them using natural language!")
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("Ask your AI assistant..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.agent:
        with st.chat_message("assistant"):
            with st.spinner("Assistant is thinking..."):
                # Run the async function correctly in Streamlit
                result = asyncio.run(run_agent_query(st.session_state.agent, prompt))
                st.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
    else:
        st.warning("Please activate the configuration in the sidebar first.")