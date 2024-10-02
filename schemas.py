from pydantic import BaseModel, Field
from typing import List

# Prompt template
PROMPT_TEMPLATE_SLIDES = """
You are an assistant for creating powerpoint presentations.

Please generate a presentation with {number_of_slides} slides based on given text below. First generate the 
presentation title and then generate below for each slide:
1- Provide a suitable slide title summarizing the key concept or idea.
2- Generate exactly {number_of_bullet_points} bullet points in a slide that highlight the most important information 
or takeaways from the content. Make the bullet points short and concise
3- Provide notes for the presenter below the bullet points to expand on the key concepts and offer additional context 
for the speaker.*

The presentation should be clear, concise, and well-structured for easy understanding by the audience. Please follow 
the instructions strictly and generate slides and bullet points as mentioned. Not more nor less.

Given text: {text}

"""

# Prompt template
PROMPT_TEMPLATE_PODCAST = """
You are an expert for creating podcast episodes.

For the given text, create a podcast episode from it. Structure it in a podcast format with the following elements:

1- Introduction: Start with a brief, engaging introduction summarizing the theme of the podcast.
2- Main Content: Break down the provided text into sections, each covering a specific topic or point. 
Add transitions between sections to maintain a smooth flow.
3- Host's Commentary: Include occasional commentary or questions from the podcast host to make the content conversational.
4- Closing Remarks: Conclude with a summary of the key points discussed and encourage listeners to engage with the podcast.
5- Tone: Make the tone friendly, informative, and engaging, suitable for a general audience.

Given text: {text}

"""


# Structure the presentation schema using Pydantic
class CreateSlides(BaseModel):
    """Create slides and notes about the given paper"""
    slide_title: str = Field(description="Title of the slide")
    bullet_points: List[str] = Field(description="List of bullet points")
    slide_notes: str = Field(description="Slide Notes")


class CreatePresentation(BaseModel):
    """Create multiple slides with bullet points and notes"""
    presentation_title: str = Field(description="Title of the presentation")
    slides: List[CreateSlides] = Field(description="List of slides")


# Structure the podcast schema using Pydantic
class PodcastSection(BaseModel):
    """Sections of the Podcast. It includes section title and host commentary"""
    section_title: str = Field(description="Title of the podcast section")
    host_commentary: str = Field(description="Podcast host commentary")


class CreatePodcast(BaseModel):
    """Create podcast episode"""
    podcast_title: str = Field(description="Title of the podcast episode")
    introduction: str = Field(description="Podcast episode Introduction")
    sections: List[PodcastSection] = Field(description="Podcast sections along with host commentary")
    closing_remarks: str = Field(description="Podcast closing remarks")

