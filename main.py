from util import *

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

# Select the LLM
llm_selection = configure_llm_selection()

# Configure the model based on user selection
llm = configure_llm(llm_selection)

# Configure presentation parameters
number_of_slides, number_of_bullet_points, podcast = configure_presentation_parameter()

# File uploader
st.subheader("Upload a PDF file:")
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed")

if uploaded_pdf is not None:
    file_name = uploaded_pdf.name.split('.')[0]  # Get the filename without extension

    # Extract text from pdf file
    extracted_text = extract_text_from_pdf(uploaded_pdf)

    # Generate button
    button_text = "Generate Presentation & Podcast" if podcast else "Generate Presentation"
    generate = st.button(button_text, type='primary')

    if generate:
        with st.spinner('Generating ...'):

            # Generate presentation from llm
            presentation_data = generate_presentation(number_of_slides, number_of_bullet_points, extracted_text, llm)

            if podcast:
                podcast_data = generate_podcast(extracted_text, llm)

            # Extract  presentation title, slide contents and notes
            presentation_title, slide_contents, slide_notes = extract_presentation_data(presentation_data)

            # Convert text to presentation
            pptx_file = text_to_presentation(slide_contents, presentation_title, slide_notes)
            success_text = "Presentation & Podcast Generated Successfully" if podcast else ("Presentation "
                                                                                            "Generated "
                                                                                            "Successfully")
            # Display success text and draw celebratory balloons
            st.success(success_text)
            st.balloons()

            # Display the presentation
            display_presentation(presentation_data)

            if podcast:
                display_podcast(podcast_data)

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
