from display import *
from config import *
from util import *
from llm import *
from tts import *

if "scope" not in st.session_state:
    st.session_state.scope = False
if "presentation_data" not in st.session_state:
    st.session_state.presentation_data = None
if "pptx_file" not in st.session_state:
    st.session_state.pptx_file = None
if "podcast_data" not in st.session_state:
    st.session_state.podcast_data = None
if "audio_stream" not in st.session_state:
    st.session_state.audio_stream = None

# Set the application title and description
page_title = "SlideGenie 🎤📊"
page_icon = "✨"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout='wide')
st.title(f'{page_title}')
st.write(':blue[***Transform PDFs into Engaging Presentations and Compelling Podcast Scripts!" 📄➡️✨***]')
st.write("SlideGenie is your all-in-one solution for turning PDF documents into clear, concise, and well-structured "
         "presentations and engaging podcast scripts. 🚀✨ Upload any PDF, let our AI work its magic, and receive "
         "professional-grade slides and a captivating narrative ready to go! Perfect for educators, business "
         "professionals, and content creators looking to enhance their communication effortlessly. 📝🎧")

col1, col2 = st.columns(2)
with col1:
    # Configuration option for content generation
    content_selection = configure_content_generation_options()
with col2:
    # Select the LLM
    llm_selection = configure_llm_selection()

if content_selection == 'Presentation':
    # Configure presentation parameters
    number_of_slides, number_of_bullet_points = configure_presentation_parameters()
    button_text = 'Generate Presentation'
    button_icon = icon = ':material/jamboard_kiosk:'
    success_text = "Presentation Generated Successfully!"

if content_selection == 'Podcast':
    # Configure podcast parameters
    number_of_hosts, host_names, podcast_audio = configure_podcast_parameters()
    button_text = "Generate Podcast"
    button_icon = icon = ':material/podcasts:'
    success_text = "Podcast Generated Successfully!"

if content_selection == 'Both':
    col1, col2 = st.columns(2)
    with col1:
        # Configure presentation parameters
        number_of_slides, number_of_bullet_points = configure_presentation_parameters()

    with col2:
        # Configure podcast parameters
        number_of_hosts, host_names, podcast_audio = configure_podcast_parameters()

    button_text = "Generate Presentation & Podcast"
    button_icon = icon = ':material/play_arrow:'
    success_text = "Presentation & Podcast Generated Successfully!"

# File uploader
st.subheader("Upload a PDF file:")
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed")

if uploaded_pdf is not None:
    file_name = uploaded_pdf.name.split('.')[0]  # Get the filename without extension

    # Extract text from pdf file
    extracted_text = extract_text_from_pdf(uploaded_pdf)

    # Generate button
    generate = st.button(button_text, type='primary', icon=button_icon)

    # This condition will be true if Generate button is clicked or code has been run at least once
    if generate or st.session_state.scope:
        st.session_state.scope = True
        if generate:  # This will ensure content is generated only when button is clicked.
            status = st.status('Generating Content ...', expanded=True)  # Status to keep track of content generation
            if content_selection in ['Presentation', 'Both']:

                # Container to display text temporarily
                placeholder = status.empty()
                placeholder.write('*Generating Presentation ...*')

                # Generate presentation from llm
                st.session_state.presentation_data = generate_presentation(number_of_slides, number_of_bullet_points,
                                                                           extracted_text, llm_selection)
                # Extract  presentation title, slide contents and notes
                presentation_title, slide_contents, slide_notes = extract_presentation_data(
                    st.session_state.presentation_data)

                # Convert text to presentation
                st.session_state.pptx_file = text_to_presentation(slide_contents, presentation_title, slide_notes)

                # Remove the previously displayed text
                placeholder.empty()

                # Display success status
                status.write('*Presentation Generated* ✅ ')

            # Generate podcast from llm if enabled
            if content_selection in ['Podcast', 'Both']:
                # Container to display text temporarily
                placeholder = status.empty()
                placeholder.write('*Generating Podcast ...*')

                # Generate podcast from LLM
                st.session_state.podcast_data = generate_podcast(extracted_text, number_of_hosts, host_names,
                                                                 llm_selection)
                # Remove previously displayed text
                placeholder.empty()

                # Display success status
                status.write('*Podcast Generated* ✅ ')

                if podcast_audio:
                    # Container to display text temporarily
                    placeholder = status.empty()
                    placeholder.write('*Generating Podcast Audio ...*')

                    # Generate podcast audio using TTS APIs
                    st.session_state.audio_stream = generate_podcast_audio(st.session_state.podcast_data)

                    # Remove previously displayed text
                    placeholder.empty()

                    # Display success status
                    status.write('*Podcast Audio Generated* ✅ ')

            status.update(label="Content Generated", state="complete", expanded=True)

            # Display success text and draw celebratory balloons
            # st.success(success_text)
            # st.balloons()

        if content_selection in ['Presentation', 'Both'] and st.session_state.presentation_data is not None:
            # Display the presentation
            display_presentation(st.session_state.presentation_data, file_name)

        if content_selection in ['Podcast', 'Both'] and st.session_state.podcast_data is not None:
            display_podcast(st.session_state.podcast_data, file_name)
            if podcast_audio:
                display_podcast_audio(st.session_state.audio_stream)

# Display footer
display_footer()
