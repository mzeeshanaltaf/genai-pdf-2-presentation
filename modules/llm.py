from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st
from modules.schemas import *


# Function to initialize llm based on user selection
def initialize_llm(llm_selection):
    llm = None  # Initialize to null to get away with warning
    if llm_selection == 'Groq':
        llm = ChatGroq(model="llama-3.2-90b-text-preview", api_key=st.session_state.groq_api_key, temperature=0.0)
    elif llm_selection == 'OpenAI':
        llm = ChatOpenAI(model='gpt-4o', api_key=st.session_state.openai_api_key)
    return llm


# This function uses an LLM to create well-structured slides with key points based on provided text
def generate_presentation(number_of_slides, number_of_bullet_points, extracted_text, llm_selection):

    # Initialize LLM
    llm = initialize_llm(llm_selection)

    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_SLIDES)
    prompt = prompt_template.format(number_of_slides=number_of_slides,
                                    number_of_bullet_points=number_of_bullet_points,
                                    text=extracted_text,
                                    general_guidelines=general_guidelines)

    # Get structured output from LLM
    structured_llm = llm.with_structured_output(CreatePresentation)
    structured_response = structured_llm.invoke(prompt)
    presentation_data = structured_response.dict()
    return presentation_data


# This function uses an LLM to create podcast script based on provided text
def generate_podcast(extracted_text, number_of_hosts, host_names, llm_selection):

    # Initialize LLM
    llm = initialize_llm(llm_selection)

    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_PODCAST)
    prompt_podcast = prompt_template.format(number_of_hosts=number_of_hosts,
                                            host_names=host_names,
                                            text=extracted_text)

    # Get structured output from llm
    structured_llm = llm.with_structured_output(CreatePodcast)
    structured_response = structured_llm.invoke(prompt_podcast)
    podcast_data = structured_response.dict()

    return podcast_data
