# ai_helpers/tts_opentts.py

import requests
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner="🔊 Generating speech...")
def text_to_speech_opentts(text: str, lang: str = "en", voice: str = "en-us", filename: str = "speech.wav") -> str:
    """
    Convert text to speech using OpenTTS API and save the result.

    Args:
        text (str): The input text to convert.
        lang (str): Language code (e.g., "en").
        voice (str): Voice identifier (depends on server setup).
        filename (str): File name to save the audio.

    Returns:
        str: Path to the saved audio file.
    """
    # Change this to your own OpenTTS server or a public instance
    TTS_API_URL = "https://api.opentts.com/tts"  # Replace if needed

    params = {
        "lang": lang,
        "voice": voice,
        "text": text,
    }

    response = requests.get(TTS_API_URL, params=params)
    response.raise_for_status()

    output_path = Path(__file__).parent / filename
    with open(output_path, "wb") as f:
        f.write(response.content)

    return str(output_path)
