import os
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import soundfile as sf

# Load model and tokenizer from Hugging Face
model_name = "facebook/fastspeech2-en-ljspeech"
model = AutoModelForCausalLM.from_pretrained(model_name).to("cpu")
tokenizer = AutoTokenizer.from_pretrained(model_name)

def text_to_speech(text: str, voice: str = "default", filename: str = "speech.wav") -> str:
    """
    Generate TTS audio using FastSpeech2 and save it locally.
    
    Args:
        text (str): The text to convert to speech.
        voice (str): The voice model to use (if applicable).
        filename (str): The output filename.

    Returns:
        str: The path to the saved audio file.
    """
    # Path where the audio will be saved
    speech_file_path = Path(__file__).parent / filename

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs.input_ids.to("cpu")

    # Generate speech
    with torch.no_grad():
        output = model.generate(input_ids)
        audio_arr = output.cpu().numpy().squeeze()

    # Save to WAV file
    sf.write(speech_file_path, audio_arr, model.config.sampling_rate)

    return str(speech_file_path)
