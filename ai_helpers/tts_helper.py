# ai_helpers/tts_helper.py
import os
from pathlib import Path
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def text_to_speech(text: str, voice: str = "Angelo-PlayAI", filename: str = "speech.wav") -> str:
    """
    Generate TTS audio using Groq and save it locally.
    
    Args:
        text (str): The text to convert to speech.
        voice (str): The voice model to use.
        filename (str): The output filename.

    Returns:
        str: The path to the saved audio file.
    """
    speech_file_path = Path(__file__).parent / filename

    response = client.audio.speech.create(
        model="playai-tts",
        voice=voice,
        response_format="wav",
        input=text,
    )

    with open(speech_file_path, "wb") as f:
        f.write(response.content)

    return str(speech_file_path)
