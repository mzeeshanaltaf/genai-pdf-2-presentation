import streamlit as st
from modules.display import *

st.subheader('About')
with st.expander('Application'):
    st.markdown(''' Transform PDFs into Engaging Presentations and Compelling Podcast Scripts!" 📄➡️✨ ''')
with st.expander('Technologies Used'):
    st.markdown(''' 
    * Langchain -- Orchestration framework for the development of applications using large language models 
    * Supported LLMs:
        * gpt-4o from OpenAI
        * llama-3.2-90b-text-preview from Groq
    * Streamlit -- For application Front End
    ''')
with st.expander('Contact'):
    st.markdown(''' Any Queries: Contact [Zeeshan Altaf](mailto:zeeshan.altaf@92labs.ai)''')
with st.expander('Source Code'):
    st.markdown(''' Source code: [GitHub](https://github.com/mzeeshanaltaf/genai-pdf-2-presentation)''')

display_footer()