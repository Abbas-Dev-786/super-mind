import streamlit as st
from flow_runner import run_flow
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
CONFIG = {
    "ENDPOINT": "2520f246-749c-468d-b715-747e436afdf2",
    "APP_TOKEN": "AstraCS:zPlTkOcRoljPUdOlbZAWskwi:2bf1ee1e6d548c12cfcc7b8cbb0c1ed90c7cb8b1de7824293d4b541b4b1c645e",
    "OUTPUT_TYPE": "chat",
    "INPUT_TYPE": "chat"
}

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your social media analytics assistant. How can I help you today?"}
        ]

def parse_response(response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Parse the API response and return structured data."""
    try:
        text_response = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
        visualization_data = None
        
        if "visualization" in response["outputs"][0]["outputs"][0]["results"]:
            visualization_data = response["outputs"][0]["outputs"][0]["results"]["visualization"]
        
        return {
            "text": text_response,
            "visualization": visualization_data
        }
    except KeyError as e:
        logger.error(f"Error parsing response: {str(e)}")
        return None

def setup_sidebar():
    """Setup the sidebar with configuration options and information."""
    with st.sidebar:
        st.title("Configuration")
        st.markdown("### About")
        st.markdown(
            "Made by [Abbas Bhanpura wala](https://abbas-bhanpura-wala.vercel.app/)"
        )
        
        if st.button("Clear Chat History"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your social media analytics assistant. How can I help you today?"}
            ]
            st.success("Chat history cleared!")
        
        st.markdown("---")
        st.markdown("### Visualization Settings")
        st.checkbox("Show Analytics Visualizations", value=True, key="show_viz")

def display_chat_messages():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # If message is from assistant and contains visualization data
            if message.get("visualization") and st.session_state.show_viz:
                with st.expander("📊 View Analytics", expanded=False):
                    st.json(message["visualization"])

def main():
    st.title("💬 Social Media Analytics Chatbot")
    
    # Initialize session state
    initialize_session_state()
    
    # Setup sidebar
    setup_sidebar()
    
    # Display chat messages
    display_chat_messages()
    
    # Chat input
    if prompt := st.chat_input("Ask me about social media analytics..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    # Make API call
                    response = run_flow(
                        message=prompt,
                        endpoint=CONFIG["ENDPOINT"],
                        output_type=CONFIG["OUTPUT_TYPE"],
                        input_type=CONFIG["INPUT_TYPE"],
                        application_token=CONFIG["APP_TOKEN"],
                    )
                    
                    # Handle response
                    if isinstance(response, dict):
                        parsed_data = parse_response(response)
                        if parsed_data:
                            st.markdown(parsed_data["text"])
                            
                            # Store response in session state
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": parsed_data["text"],
                                "visualization": parsed_data.get("visualization")
                            })
                            
                            # Show visualization if available
                            if parsed_data.get("visualization") and st.session_state.show_viz:
                                with st.expander("📊 View Analytics", expanded=False):
                                    st.json(parsed_data["visualization"])
                        else:
                            error_msg = "I couldn't process that properly. Could you rephrase your question?"
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
                    elif isinstance(response, str):
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    else:
                        error_msg = "I encountered an unexpected error. Please try again."
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    logger.error(error_msg)
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()