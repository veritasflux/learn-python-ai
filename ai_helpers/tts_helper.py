# ai_helpers/tts_fairseq.py

import os
import streamlit as st
import torch
import soundfile as sf
from pathlib import Path
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface

@st.cache_resource
def load_fairseq_model():
    models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
        "facebook/fastspeech2-en-ljspeech",
        arg_overrides={"vocoder": "hifigan", "fp16": False}
    )
    model = models[0]
    TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
    generator = task.build_generator(model, cfg)
    return model, cfg, task, generator

def text_to_speech_fairseq(text: str, filename: str = "speech.wav") -> str:
    model, cfg, task, generator = load_fairseq_model()
    sample = TTSHubInterface.get_model_input(task, text)
    wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)

    output_path = Path(__file__).parent / filename
    sf.write(str(output_path), wav, rate)
    return str(output_path)
