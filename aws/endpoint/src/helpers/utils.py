"""Utility functions for the scoring script"""
import base64
import tempfile

import torch
from audiocraft.data.audio import audio_write
from audiocraft.models import musicgen


def set_generation_parameters(input_data: dict, model: musicgen.MusicGen) -> None:
    """
    Sets the model generation parameters

    Parameters
    ----------
    input_data : dict
        The request input data, converted from json
    model : musicgen.MusicGen
        The musicgen loaded model
    """
    duration = input_data.get("duration", 8.0)
    temperature = input_data.get("temperature", 1.0)
    top_p = input_data.get("top_p", 0.0)
    top_k = input_data.get("top_k", 250.0)
    cfg_coefficient = input_data.get("cfg_coefficient", 3.0)

    model.set_generation_params(
        duration=duration,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        cfg_coef=cfg_coefficient,
    )


def audio_to_base64(audio: torch.Tensor, sample_rate: int, format: str = "mp3") -> str:
    """
    Converts the output audio file from the pipeline to base64

    Parameters
    ----------
    audio : torch.Tensor
        The output audio from the model
    sample_rate : int
        The output file sample rate
    format : str , optional
        The output file format

        Defaults to `mp3`

    Returns
    -------
    str
        The audio file in base64-encoded string
    """
    with tempfile.NamedTemporaryFile() as temp_file:
        audio_write(
            wav=audio.cpu(),
            sample_rate=sample_rate,
            stem_name=temp_file.name,
            format=format,
            strategy="loudness",
            make_parent_dir=False,
        )

        with open(f"{temp_file.name}.{format}", "rb") as written_temp_file:
            audio_base64 = base64.b64encode(written_temp_file.read()).decode()

    return audio_base64
