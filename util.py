import pdfplumber
import streamlit as st
from pptx import Presentation
from pydantic import BaseModel, Field
from io import BytesIO


# Prompt template
PROMPT_TEMPLATE_SLIDES = """
You are an assistant for creating powerpoint presentations.

Please generate a presentation with a three slides based on given text below. First generate the presentation title 
and then generate below for each slide:
1- Provide a suitable slide title summarizing the key concept or idea.
2- Include 3 bullet points that highlight the most important information or takeaways from the content. 
Make the bullet points short and concise
3- Provide notes for the presenter below the bullet points to expand on the key concepts and offer additional 
context for the speaker.*

The presentation should be clear, concise, and well-structured for easy understanding by the audience.

Given text: {text}

"""


# Structure the response schema using Pydantic
class CreateSlides(BaseModel):
    """Create slides and notes about the given paper"""
    slide_title: str = Field(description="Title of the slide")
    bullet_point_1: str = Field(description="Bullet Point number 1")
    bullet_point_2: str = Field(description="Bullet Point number 2")
    bullet_point_3: str = Field(description="Bullet Point number 3")
    slide_notes: str = Field(description="Slide Notes")


class CreatePresentation(BaseModel):
    """Create multiple slides with bullet points and notes"""
    presentation_title: str = Field(description="Title of the presentation")
    slide_1: CreateSlides
    slide_2: CreateSlides
    slide_3: CreateSlides


def extract_text_from_pdf(pdf_file_path):
    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_file_path) as pdf:
        # Initialize an empty string to store extracted text
        extracted_text = ""

        # Loop through all the pages and extract text
        for page in pdf.pages:
            extracted_text += page.extract_text()

    return extracted_text


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


# Generate presentation title, slide contents and notes
def extract_presentation_contents(response):
    # Presentation title
    presentation_title = f"{response['presentation_title']}"

    # Slides contents
    slide_contents = f"""
    {response['slide_1']['slide_title']}
     {response['slide_1']['bullet_point_1']}
     {response['slide_1']['bullet_point_2']}
     {response['slide_1']['bullet_point_3']}

    {response['slide_2']['slide_title']}
     {response['slide_2']['bullet_point_1']}
     {response['slide_2']['bullet_point_2']}
     {response['slide_2']['bullet_point_3']}

    {response['slide_3']['slide_title']}
     {response['slide_3']['bullet_point_1']}
     {response['slide_3']['bullet_point_2']}
     {response['slide_3']['bullet_point_3']}
    """

    # Example slide notes (note that the first note is for the title slide)
    slide_notes = [
        "This is the title slide.",
        f"{response['slide_1']['slide_notes']}",
        f"{response['slide_2']['slide_notes']}",
        f"{response['slide_3']['slide_notes']}",
    ]

    return presentation_title, slide_contents, slide_notes


def display_presentation(response):
    st.subheader('Generated Presentation:')
    st.markdown(f"#### Presentation Title: :blue[{response['presentation_title']}]")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.subheader(f":green[{response['slide_1']['slide_title']}]")
            st.markdown(f"- {response['slide_1']['bullet_point_1']}")
            st.markdown(f"- {response['slide_1']['bullet_point_2']}")
            st.markdown(f"- {response['slide_1']['bullet_point_3']}")
            with st.expander('Slide Notes'):
                st.write(response['slide_1']['slide_notes'])
    with col2:
        with st.container(border=True):
            st.subheader(f":green[{response['slide_2']['slide_title']}]")
            st.markdown(f"- {response['slide_2']['bullet_point_1']}")
            st.markdown(f"- {response['slide_2']['bullet_point_2']}")
            st.markdown(f"- {response['slide_2']['bullet_point_3']}")
            with st.expander('Slide Notes'):
                st.write(response['slide_2']['slide_notes'])
    with col3:
        with st.container(border=True):
            st.subheader(f":green[{response['slide_3']['slide_title']}]")
            st.markdown(f"- {response['slide_3']['bullet_point_1']}")
            st.markdown(f"- {response['slide_3']['bullet_point_2']}")
            st.markdown(f"- {response['slide_3']['bullet_point_3']}")
            with st.expander('Slide Notes'):
                st.write(response['slide_3']['slide_notes'])


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