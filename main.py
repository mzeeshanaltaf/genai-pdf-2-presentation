from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from util import *

# Configure the model
llm = ChatOpenAI(model='gpt-4o-mini', api_key=st.secrets['OPENAI_API_KEY'])

# Set the application title and description
page_title = "SlideGenie ✨🧙‍♂️"
page_icon = "✨"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout='wide')
st.title(f'📊 {page_title}')
st.write(':blue[***Turn PDFs into Powerful Presentations with a Touch of Magic!📄➡️📊***]')
st.write("SlideGenie is an AI-powered web app that transforms your PDF files into clear, concise, "
         "and well-structured presentations in just a few clicks. 🎯✨ Upload any PDF, let the "
         "AI work its magic, and receive a professional slideshow with titles, bullet points, "
         "and presenter notes — all done for you! 📝⚡ Perfect for creating impactful "
         "presentations effortlessly.")

# display_check()

# File uploader
st.subheader("Upload a PDF file")
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed")

if uploaded_pdf is not None:
    file_name = uploaded_pdf.name.split('.')[0]  # Get the filename without extension

    # Extract text from pdf file
    extracted_text = extract_text_from_pdf(uploaded_pdf)

    # Generate button
    generate = st.button('Generate Presentation', type='primary')

    if generate:
        with st.spinner('Generating Presentation ...'):
            # Create prompt
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_SLIDES)
            prompt = prompt_template.format(text=extracted_text)

            # Get structured output from LLM
            structured_llm = llm.with_structured_output(CreatePresentation)
            structured_response = structured_llm.invoke(prompt)
            response = structured_response.dict()

            # Generate presentation title, slide contents and notes
            presentation_title, slide_contents, slide_notes = extract_presentation_contents(response)

            # Convert text to presentation
            pptx_file = text_to_presentation(slide_contents, presentation_title, slide_notes)
            st.success('Presentation Generated Successfully')

            # Display the presentation
            display_presentation(response)

            # Create a download button for the PowerPoint presentation
            st.subheader('Download Presentation:')
            ppt_name = f"{file_name}.pptx"
            st.download_button(
                label="Download Presentation",
                data=pptx_file,
                file_name=ppt_name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                type='primary'
            )

# Display footer
display_footer()









