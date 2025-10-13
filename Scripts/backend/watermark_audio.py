import numpy as np
import soundfile
import torch
import wavmark
import os
import io
import io
import ffmpeg
import IPython.display as ipd


from base64 import b64decode
from scipy.io.wavfile import read as wav_read
import numpy as np
import matplotlib.pyplot as plt

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

    # Alternatively, you can also call forward() function directly with different tune-down / tune-up rate
    watermarked_audio = model(audios, sample_rate=sr, alpha=1)

    return watermarked_audio

def decode_watermark(model, audio_clips):
    """decodes the watermarks from a watermarked audio clip"""
    decoded_payloads = []

    for audio_clip in audio_clips:
        processed_clip, _ = wavmark.decode_watermark(model, audio_clip, show_progress=True)
        decoded_payloads.append(processed_clip)

    return decoded_payloads

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


