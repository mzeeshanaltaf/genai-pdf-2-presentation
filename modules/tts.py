from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from modules.display import *


def text_to_speech_stream(text: str) -> IO[bytes]:
    client = ElevenLabs(api_key=st.session_state.elevenlabs_api_key)

    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id="CwhRBWXzGAHq8TQ4Fs17",  # Roger pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream


# Convert podcast text into Audio
def generate_podcast_audio(podcast_data):
    sentence = extract_sentences_from_podcast(podcast_data)
    audio_stream = text_to_speech_stream(sentence)
    return audio_stream


