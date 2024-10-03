from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st


# Function to configure presentation parameter
def configure_presentation_parameter():
    # Configuration for presentation parameters
    st.subheader('Presentation Parameters:')
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            number_of_slides = st.slider('Number of Slides:', min_value=1, max_value=10, value=4, step=1)
    with col2:
        with st.container(border=True):
            number_of_bullet_points = st.slider('Number of Bullet Points:', min_value=1, max_value=5, value=3, step=1)

    podcast = st.toggle('Generate Podcast', value=True)
    return number_of_slides, number_of_bullet_points, podcast


# Function to configure LLM options for user selection
def configure_llm_selection():
    st.subheader('Model Selection:')
    llm_selection = st.radio('Select the LLM', ["Groq", "OpenAI"], horizontal=True,
                             captions=['model: llama-3.2-90b-text-preview', 'model: gpt-4o-mini'],
                             label_visibility='collapsed')
    return llm_selection


# Function to configure llm based on user selection
def configure_llm(llm_selection):
    llm = None  # Initialize to null to get away with warning
    if llm_selection == 'Groq':
        llm = ChatGroq(model="llama-3.2-90b-text-preview", api_key=st.secrets['GROQ_API_KEY'], temperature=0.0)
    elif llm_selection == 'OpenAI':
        llm = ChatOpenAI(model='gpt-4o-mini', api_key=st.secrets['OPENAI_API_KEY'])
    return llm
