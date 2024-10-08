import streamlit as st
from modules.display import *

st.title("Configuration")

st.session_state.openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password",
                                                value=st.session_state.openai_api_key,
                                                help='Get API Key from: https://platform.openai.com/api-keys')

st.session_state.groq_api_key = st.text_input("Enter your Groq API Key:", type="password",
                                              value=st.session_state.groq_api_key,
                                              help='Get Groq API Key from: https://console.groq.com/keys')

st.session_state.elevenlabs_api_key = st.text_input("Enter your ElevenLabs API Key:", type="password",
                                                    value=st.session_state.elevenlabs_api_key,
                                                    help='Get ElevenLabs API Key from: https://elevenlabs.io/')

# Display footer
display_footer()
