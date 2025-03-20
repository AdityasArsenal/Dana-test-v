import streamlit as st
import requests
from streamlit.components.v1 import html
import json

# Backend URL
WEBHOOK_URL = "http://localhost:8000/chat"

# Initialize session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "received_question" not in st.session_state:
    st.session_state.received_question = None

st.title("AI Chat Interface")

# JavaScript to listen for postMessage events and store in session state
js_code = """
<script>
// Function to send data back to Streamlit
function sendToStreamlit(data) {
    // Use the Streamlit-js-eval component to communicate
    window.parent.postMessage(
        {type: "streamlit:setComponentValue", value: data}, "*"
    );
}

// Listen for messages from parent iframe
window.addEventListener('message', function(event) {
    // Check if the message is from our parent and has the expected format
    if (event.data && event.data.type === 'streamlit:message' && event.data.question) {
        // Get the question from the message
        const question = event.data.question;
        
        // Send it back to Streamlit to handle
        sendToStreamlit({action: "new_question", question: question});
    }
});
</script>
"""

# Custom component to handle messages from JavaScript
def custom_component():
    from streamlit.components.v1 import components
    
    # Create a placeholder for our component
    component_value = components.declare_component(
        "message_receiver", 
        url="http://localhost:3000"  # Replace with your actual frontend URL
    )

    
    # Check if we received a message
    if component_value and isinstance(component_value, dict):
        if component_value.get("action") == "new_question":
            # Store the question in session state
            st.session_state.received_question = component_value.get("question")
            # Force a rerun to process the question
            st.rerun()
    
    # Return the HTML with our JavaScript
    return html(js_code)

# Add the custom component to the page
custom_component()

# Process any received questions from parent iframe
if st.session_state.received_question:
    question = st.session_state.received_question
    st.session_state.received_question = None  # Clear the question
    process_message(question)

def process_message(user_input):
    """Process a message and update the chat interface"""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Build payload including conversation_id if available
    payload = {"user_prompt": user_input}
    if st.session_state.conversation_id:
        payload["conversation_id"] = st.session_state.conversation_id
    
    # Send request to backend
    with st.spinner("Looking for relevant stuff..."):
        response = requests.post(WEBHOOK_URL, json=payload)
    
    if response.status_code == 200:
        json_response = response.json()
        ai_message = json_response.get("response", "Sorry, no response was generated.")
        # Save conversation_id from backend for persistent conversation
        st.session_state.conversation_id = json_response.get("conversation_id", st.session_state.conversation_id)
        st.session_state.messages.append({"role": "assistant", "content": ai_message})
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

def display_chat():
    """Display chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Display chat history
display_chat()

# Get user input
user_input = st.chat_input("Enter your message here")
if user_input:
    process_message(user_input)
    st.rerun()