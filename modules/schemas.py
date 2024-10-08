from pydantic import BaseModel, Field
from typing import List


general_guidelines = """

- Strictly follow the template provided to you so that it renders properly on the slides
- Generate presentation title, slide title and bullet points in markdown format
- For each slide, just generate the slide title, bullet points and notes. DO NOT GENERATE SLIDE # IN THE SLIDE TITLE
- Bullet points in a slide highlight the most important information or takeaways from the content. Make the bullet points short and concise
- Ensure that bullet points in each slide are returned in markdown format as follows:
    - Bullet point 1
    - Bullet point 2
    - Bullet point 3
- Provide notes for the presenter below the bullet points to expand on the key concepts and offer additional 
context for the speaker
- For the slide notes, don't say "In this slide" or "In this presentation" at all, keep the script flow smooth from 
one slide to the next 
- The presentation should be clear, concise, and well-structured for easy understanding by the audience.

"""

# Prompt template
PROMPT_TEMPLATE_SLIDES = """
You are an expert for creating powerpoint presentations.

Please generate a presentation with {number_of_slides} slides based on given text below.  There should be 
{number_of_bullet_points} bullet points in each slide.  To help you out, follow the general guidelines given below 
very strictly. 

general guidelines: {general_guidelines}
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


# Structure the response schema using Pydantic
class CreateSlides(BaseModel):
    """Create slides and notes about the given paper"""
    slide_title: str = Field(description="Slide Title. Use markdown (`## Slide Title`) for the slide title.")
    bullet_points: List[str] = Field(
        description="Bullet points list. Bullet point in each slide should be in markdown format as follows:  (`- "
                    "Bullet Point 1`). Make sure each bullet point follows markdown format strictly.")
    slide_notes: str = Field(description="Slide Notes")


class CreatePresentation(BaseModel):
    """Create multiple slides with bullet points and notes"""
    presentation_title: str = Field(
        description="Presentation Title. Use markdown (`# Presentation Title`) for the presentation title.")
    slides: List[CreateSlides] = Field(description="Slides list")


# Structure the response schema using Pydantic
class PodcastSection(BaseModel):
    """Sections of the Podcast. It includes section title and host commentary by single or multiple hosts"""
    section_title: str = Field(description="Title of the podcast section")
    host_commentary: List[str] = Field(description="List of host commentary")


class CreatePodcast(BaseModel):
    """Create podcast episode"""
    podcast_title: str = Field(description="Title of the podcast episode")
    introduction: str = Field(description="Podcast episode Introduction")
    sections: List[PodcastSection] = Field(
        description="Podcast sections along with single or multiple host commentary")
    closing_remarks: str = Field(description="Podcast closing remarks")
