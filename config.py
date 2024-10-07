import streamlit as st


def configure_content_generation_options():
    st.subheader('Content Generation:')
    content_selection = st.radio('What would you like to generate?', ['Presentation', 'Podcast', 'Both'],
                                 captions=['Generate Presentation only', 'Generate Podcast only', 'Generate Both'],
                                 label_visibility='collapsed', index=2, horizontal=True)
    return content_selection


# Function to configure presentation parameters
def configure_presentation_parameters():
    st.subheader('Presentation Parameters:')
    with st.expander('Configure Presentation parameters', icon=':material/tune:', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                number_of_slides = st.slider('Number of Slides:', min_value=1, max_value=10, value=4, step=1, key='slides')
        with col2:
            with st.container(border=True):
                number_of_bullet_points = st.slider('Number of Bullet Points:', min_value=1, max_value=5, value=3, step=1,
                                                    key='bullets')

    return number_of_slides, number_of_bullet_points,


# Function to configure presentation parameters
def configure_podcast_parameters():
    st.subheader('Podcast Parameters:')
    placeholder_names = ['Zeeshan', 'Einstein', 'Newton', 'Elon', 'Misbah']
    with st.expander('Configure Podcast parameters', icon=':material/tune:', expanded=True):
        with st.container(border=True):
            # Configuration for audio toggle and number of hosts
            audio = st.toggle('Generate Audio', value=False)
            number_of_hosts = st.number_input('Number of Host(s):', min_value=1, max_value=5, value=3, step=1)

            # Configuration for host names
            st.write('Host Name(s):')
            host_names = []
            cols = st.columns(number_of_hosts)

            for idx, col in enumerate(cols):
                host_name = col.text_input(f'Name of Host {idx + 1}:', value=placeholder_names[idx], key=f'host_name_{idx}')
                host_names.append(host_name)
    return number_of_hosts, host_names, audio


# Function to configure LLM options for user selection
def configure_llm_selection():
    st.subheader('LLM Selection:')
    llm_selection = st.radio('Select the LLM', ["Groq", "OpenAI"], horizontal=True,
                             captions=['model: llama-3.2-90b-text-preview', 'model: gpt-4o'],
                             label_visibility='collapsed')
    return llm_selection


