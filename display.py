import streamlit as st


# Function to display presentation day in a structured way
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


# Function to display podcast data in a structured way
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
