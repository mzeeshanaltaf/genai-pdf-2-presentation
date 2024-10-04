import streamlit as st


@st.dialog("Slide Notes", width='large')
def slide_notes_dialog(slide_notes):
    st.write(slide_notes)


# Function to display presentation in a structured way
def display_presentation(presentation_data, file_name):
    st.subheader('Presentation🖥️:')
    with st.expander('Generated Presentation', icon=':material/jamboard_kiosk:', expanded=True):
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
                            if st.button('Slide Notes', key=f'notes_{slide_idx}'):
                                slide_notes_dialog(slide['slide_notes'])
                            # with st.expander('Slide Notes'):
                            #     st.write(slide['slide_notes'])
                else:
                    cols[col_idx].empty()  # Leave empty for alignment

        # Download button for downloading presentation
        st.download_button(
            label="Download Presentation",
            data=st.session_state.pptx_file,
            file_name=f"{file_name}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            type='primary'
        )


# Function to extract podcast text so that it could be downloaded
def extract_podcast_text(podcast_data):
    # Extract text
    extracted_text = ""

    # Add podcast title and introduction
    extracted_text += f"{podcast_data['podcast_title']}\n\n"
    extracted_text += f"{podcast_data['introduction']}\n\n"

    # Add sections
    for section in podcast_data['sections']:
        extracted_text += f"{section['section_title']}\n"
        for commentary in section['host_commentary']:
            extracted_text += f"{commentary}\n"
        extracted_text += "\n"

    # Add closing remarks
    extracted_text += f"{podcast_data['closing_remarks']}"
    return extracted_text


# This function extract few sentences from the podcast data
def extract_sentences_from_podcast(podcast_data):
    paragraph = podcast_data['introduction']
    # Split the paragraph into sentences using period, exclamation mark, and question mark as delimiters
    sentences = [sentence.strip() for sentence in paragraph.split('.') if sentence.strip()]

    # Extract the first two sentences
    extracted_text = ". ".join(sentences[:2]) + "."

    return extracted_text


# Function to display podcast data in a structured way
def display_podcast(podcast_data, file_name):
    st.subheader('Podcast Script📝️:')

    # Display podcast script
    with st.expander('Podcast Script', icon=':material/podcasts:', expanded=True):
        st.markdown(f"#### Podcast Title: :blue[{podcast_data['podcast_title']}]")
        st.markdown(f"#### Introduction:")
        st.write(podcast_data['introduction'])
        for section in podcast_data['sections']:
            st.write(f"**{section['section_title']}**")
            for host in section['host_commentary']:
                st.write(host)
        st.markdown(f"#### Closing Remarks:")
        st.write(podcast_data['closing_remarks'])

        # Extract text from podcast data
        extracted_text = extract_podcast_text(podcast_data)

        # Download button for downloading podcast script
        st.download_button(
            label="Download Podcast Script",
            data=extracted_text,
            file_name=f"{file_name}.txt",
            mime=None,
            type='primary'
        )


def display_podcast_audio(audio_stream):
    st.subheader('Podcast Audio 🔊:')
    audio_stream.seek(0)
    st.audio(audio_stream)


# Function to display pdf extracted text
def display_pdf_text(extracted_text):
    with st.expander("***Extracted text***"):
        if extracted_text:
            st.text(extracted_text)
        else:
            st.error("No text found in this PDF.")


# Function to display footer
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
