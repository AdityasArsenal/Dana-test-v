import streamlit as st
import requests

# Backend URL
import os
WEBHOOK_URL = "http://localhost:8000/chat"

# Initialize session state if not already presenft
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

st.title("AI Chat Interface")

def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Display chat history
display_chat()

# Get user input
user_input = st.chat_input("Enter your message here")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Build payload including conversation_id if available
    payload = {"user_prompt": user_input}
    if st.session_state.conversation_id:
        payload["conversation_id"] = st.session_state.conversation_id
    
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
    
    st.rerun()


#Auth

# from streamlit_supabase_auth_ui.widgets import __login__

# __login__obj = __login__(auth_token = st.secrets["courier_auth_token"],
#                     company_name = "Shims",
#                     width = 200, height = 250,
#                     logout_button_name = 'Logout', hide_menu_bool = False,
#                     hide_footer_bool = False,
#                     lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

# LOGGED_IN = __login__obj.build_login_ui()

# if LOGGED_IN == True:

#    st.markdown("### Your Streamlit Application Begins here!")