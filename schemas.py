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
For a given text, create a podcast episode. The number of host(s) is/are {number_of_hosts}. Use the name of host(s) 
from the following list: {host_names}.

Please structure the podcast with these elements:

Introduction: Start with an engaging introduction where the host(s) introduce themselves and briefly outline the topic. 
If there is more than one host, ensure they each introduce themselves and provide a brief overview of what 
they'll discuss.
Host Dialogue: For a single host, structure the content in a monologue format, but for multiple hosts, distribute the 
content so each host covers different sections of the text, alternating in a natural conversation.
Main Content: Break down the provided text into sections, each covering a specific topic or point. Host(s) should 
explain and discuss each section in a way that flows naturally.
Closing Remarks: The host(s) should summarize the key points or insights from the discussion and wrap up the podcast. 
If there are multiple hosts, each one can share their final thoughts.
Tone: The podcast should be conversational, informative, and engaging, suitable for a general audience.

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
    """Sections of the Podcast. It includes section title and host commentary by single or multiple hosts"""
    section_title: str = Field(description="Title of the podcast section")
    host_commentary: List[str] = Field(description="List of host commentary")


class CreatePodcast(BaseModel):
    """Create podcast episode"""
    podcast_title: str = Field(description="Title of the podcast episode")
    introduction: str = Field(description="Podcast episode Introduction")
    sections: List[PodcastSection] = Field(description="Podcast sections along with single or multiple host commentary")
    closing_remarks: str = Field(description="Podcast closing remarks")


