# ai_helpers/tts_helper.py
import os
from pathlib import Path
import torch
from transformers import AutoModelForSeq2SeqLM
import soundfile as sf

# Initialize model and tokenizer
device = "cpu"  # Use CPU for inference
# Load model directly

model = AutoModelForSeq2SeqLM.from_pretrained("parler-tts/parler-tts-mini-expresso")
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-expresso")

def text_to_speech(text: str, voice: str = "Thomas", filename: str = "speech.wav") -> str:
    """
    Generate TTS audio using Parler-TTS Mini and save it locally.
    
    Args:
        text (str): The text to convert to speech.
        voice (str): The voice model to use.
        filename (str): The output filename.

    Returns:
        str: The path to the saved audio file.
    """
    # Path where the audio will be saved
    speech_file_path = Path(__file__).parent / filename

    # Prepare inputs for Parler TTS
    description = f"{voice} speaks in a neutral tone."
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)

    # Generate speech
    set_seed(42)
    with torch.no_grad():
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()

    # Save to WAV file
    sf.write(speech_file_path, audio_arr, model.config.sampling_rate)

    return str(speech_file_path)
