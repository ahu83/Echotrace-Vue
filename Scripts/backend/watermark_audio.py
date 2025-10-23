import numpy as np
import soundfile
import torch
import os
import io
import torch
import torchaudio
from audioseal import AudioSeal


def watermark_audio(model, audio, sr, payload=None ):
    """Embeds a watermark in an audioclip. The watermark itself is a 16 bit payload"""
    if payload == None:
        payload = torch.randint(0, 2, (1, 16), dtype=torch.int32)
    audios = audio.unsqueeze(0).unsqueeze(0)  # b=1 c=1 t

    watermark = model(audios, sample_rate=sr, message=payload, alpha=1)
    watermarked_audio = audios + watermark

    watermarked_audio = model(audios, sample_rate=sr, alpha=1)

    return watermarked_audio

def decode_watermark(detector, watermarked_audio, sample_rate, message_threshold=0.5):
    """decodes the watermarks from a watermarked audio clip"""
    result, message = detector.detect_watermark(watermarked_audio, sample_rate, message_threshold=0.5)

    return result, message

def calculate_error(decoded_payloads, payload):
    """calculates the error between the decoded payload and the actual payload"""
    BER_list = []
    for decoded_payload in decoded_payloads:
        BER = (payload != decoded_payload).mean() * 100
        BER_list.append(BER)

    return BER


def read_uploaded_audio(uploaded_file):
    """Reads a WAV file uploaded via Streamlit"""
    audio_bytes = uploaded_file.read()
    audio_buffer = io.BytesIO(audio_bytes)
    signal, sample_rate = soundfile.read(audio_buffer, dtype="float32")
    return signal, sample_rate


