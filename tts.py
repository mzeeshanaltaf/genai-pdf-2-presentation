from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from display import *

if "audio_data" not in st.session_state:
    st.session_state.audio_data = None
if "audio_scope" not in st.session_state:
    st.session_state.audio_scope = False


def text_to_speech_stream(text: str) -> IO[bytes]:
    client = ElevenLabs(api_key=st.secrets['ELEVENLABS_API_KEY'])

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
def podcast_audio(podcast_data):
    st.subheader('Podcast Audio 🔊:')
    sentence = extract_sentences_from_podcast(podcast_data)

    # Generate audio button
    generate_audio = st.button('Generate Audio', type='primary', icon=':material/audio_file:')

    if generate_audio or st.session_state.audio_scope:
        st.session_state.audio_scope = True
        with st.spinner('Generating Audio ...'):
            st.session_state.audio_data = text_to_speech_stream(sentence)
            st.audio(st.session_state.audio_data)

