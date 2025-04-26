# ai_helpers/tts_gtts.py

from gtts import gTTS
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner="🔊 Generating speech...")
def text_to_speech(text: str, lang: str = "en", filename: str = "speech.mp3") -> str:
    """
    Convert text to speech using gTTS and save the result.

    Args:
        text (str): Text to convert to speech.
        lang (str): Language code (default is English).
        filename (str): Output filename.

    Returns:
        str: Path to the saved audio file.
    """
    tts = gTTS(text=text, lang=lang)
    output_path = Path(__file__).parent / filename
    tts.save(output_path)
    return str(output_path)
