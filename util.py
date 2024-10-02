import pdfplumber
import streamlit as st
from pptx import Presentation
from io import BytesIO
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import *


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

    generate_podcast = st.toggle('Generate Podcast', value=True)
    return number_of_slides, number_of_bullet_points, generate_podcast


# Function to configure LLM options for user selection
def configure_llm_selection():
    st.subheader('Model Selection:')
    llm_selection = st.radio('Select the LLM', ["Groq", "OpenAI"], horizontal=True,
                             captions=['model: llama-3.2-90b-text-preview', 'model: gpt-4o-mini'],
                             label_visibility='collapsed')
    return llm_selection


# Function to configure llm based on user selection
def configure_llm(llm_selection):
    if llm_selection == 'Groq':
        llm = ChatGroq(model="llama-3.2-90b-text-preview", api_key=st.secrets['GROQ_API_KEY'], temperature=0.0)
    elif llm_selection == 'OpenAI':
        llm = ChatOpenAI(model='gpt-4o-mini', api_key=st.secrets['OPENAI_API_KEY'])
    return llm


def extract_text_from_pdf(pdf_file_path):
    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_file_path) as pdf:
        # Initialize an empty string to store extracted text
        extracted_text = ""

        # Loop through all the pages and extract text
        for page in pdf.pages:
            extracted_text += page.extract_text()

    return extracted_text


def generate_presentation(number_of_slides, number_of_bullet_points, extracted_text, llm):
    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_SLIDES)
    prompt = prompt_template.format(number_of_slides=number_of_slides,
                                    number_of_bullet_points=number_of_bullet_points,
                                    text=extracted_text)

    # Get structured output from LLM
    structured_llm = llm.with_structured_output(CreatePresentation)
    structured_response = structured_llm.invoke(prompt)
    presentation_data = structured_response.dict()
    return presentation_data


def generate_podcast(extracted_text, llm):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_PODCAST)
    prompt_podcast = prompt_template.format(text=extracted_text)

    # Get structured output from llm
    structured_llm = llm.with_structured_output(CreatePodcast)
    structured_response = structured_llm.invoke(prompt_podcast)
    podcast_data = structured_response.dict()
    return podcast_data


def display_pdf_text(extracted_text):
    with st.expander("***Extracted text***"):
        if extracted_text:
            st.text(extracted_text)
        else:
            st.error("No text found in this PDF.")


def text_to_presentation(slide_contents, presentation_title, slide_notes):
    # Split the text by slides (assuming each slide's content is separated by two newlines)
    slides_content = slide_contents.strip().split("\n\n")

    # Create a new PowerPoint presentation object
    prs = Presentation()

    # Create the first slide with the presentation title
    title_slide_layout = prs.slide_layouts[0]  # Use slide layout 0 (Title Slide)
    title_slide = prs.slides.add_slide(title_slide_layout)
    title_slide.shapes.title.text = presentation_title

    # Add notes to the first slide
    notes_slide = title_slide.notes_slide
    notes_slide.notes_text_frame.text = slide_notes[0]

    # Create the remaining slides with content
    for idx, slide_content in enumerate(slides_content):
        # Split the content into title and bullet points
        lines = slide_content.split("\n")
        slide_title = lines[0]  # First line is the title
        bullet_points = lines[1:]  # Remaining lines are bullet points

        # Add a new slide (using the layout with a title and content)
        slide_layout = prs.slide_layouts[1]  # Use slide layout 1 (Title and Content)
        slide = prs.slides.add_slide(slide_layout)

        # Set the title for the slide
        slide.shapes.title.text = slide_title

        # Set the bullet points for the slide
        content_shape = slide.shapes.placeholders[1]
        text_frame = content_shape.text_frame

        for point in bullet_points:
            p = text_frame.add_paragraph()
            p.text = point

        # Add notes to the slide
        if idx + 1 < len(slide_notes):
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = slide_notes[idx + 1]

    # Save the presentation to a BytesIO object instead of a file
    pptx_io = BytesIO()
    prs.save(pptx_io)
    pptx_io.seek(0)  # Move the cursor to the start of the BytesIO object
    return pptx_io


# This function extracts presentation data from structured LLM response
def extract_presentation_data(presentation_data):
    # Extract presentation title
    presentation_title = presentation_data['presentation_title']

    # Extract slide content
    slide_contents = ""
    for slide in presentation_data['slides']:
        slide_contents += f"{slide['slide_title']}\n"
        for bullet in slide['bullet_points']:
            slide_contents += f"    {bullet}\n"
        slide_contents += "\n"  # For separating each slide

    # Extract slide notes
    slide_notes = ["This is the title slide."]  # Default first note
    for slide in presentation_data['slides']:
        slide_notes.append(f"'{slide['slide_notes']}'")

    return presentation_title, slide_contents, slide_notes


def display_presentation(presentation_data):
    st.subheader('Generated Presentation🖥️:')
    st.markdown(f"#### Presentation Title: :blue[{presentation_data['presentation_title']}]")
    num_columns = len(presentation_data['slides'])  # Total number of columns equal to the number of slides
    max_columns_per_row = 3  # Maximum columns per row is 3

    # Calculate the number of rows needed
    rows_needed = (num_columns + max_columns_per_row - 1) // max_columns_per_row  # Ceiling division

    # Loop to create the rows of columns
    for row_idx in range(rows_needed):

        # Determine the number of columns for this row (either 3 or fewer if remaining)
        columns_in_row = min(max_columns_per_row, num_columns - row_idx * max_columns_per_row)

        # Create columns for this row
        cols = st.columns(max_columns_per_row)  # Always create 3 columns

        # Fill each column with slide_title and bullet points
        for col_idx in range(columns_in_row):
            # Calculate the actual column index in the presentation data
            slide_idx = row_idx * max_columns_per_row + col_idx

            # Check if the current slide index is within the valid range
            if slide_idx < len(presentation_data['slides']):
                slide = presentation_data['slides'][slide_idx]

                with cols[col_idx]:
                    with st.container(border=True):
                        # Display the slide title
                        st.subheader(slide['slide_title'])

                        # Display the bullet points
                        for bullet in slide['bullet_points']:
                            st.write(f"- {bullet}")
                        with st.expander('Slide Notes'):
                            st.write(slide['slide_notes'])
            else:
                cols[col_idx].empty()  # Leave empty for alignment


def display_podcast(podcast_data):
    st.subheader('Podcast Script🎙️:')
    with st.expander('Podcast Script', icon=':material/podcasts:'):
        st.markdown(f"#### Podcast Title: :blue[{podcast_data['podcast_title']}]")
        st.markdown(f"#### Introduction:")
        st.write(podcast_data['introduction'])
        for section in podcast_data['sections']:
            st.write(f"**{section['section_title']}**")
            st.write(section['host_commentary'])
        st.markdown(f"#### Closing Remarks:")
        st.write(podcast_data['closing_remarks'])


def display_footer():
    footer = """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            text-align: center;
            color: grey;
            padding: 10px 0;
        }
        </style>
        <div class="footer">
            Made with ❤️ by <a href="mailto:zeeshan.altaf@92labs.ai">Zeeshan</a>. 
        </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
