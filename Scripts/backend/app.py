from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import time
from audioseal import AudioSeal
from bark import generate_audio, SAMPLE_RATE, preload_models

from watermark_audio import watermark_audio
import numpy as np
import io, base64, soundfile as sf
import torch
from pydub import AudioSegment
from pydub.utils import which

# explicitly set paths for ffmpeg and ffprobe
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe   = r"C:\ffmpeg\bin\ffprobe.exe"


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

progress = {"value": 0, "running": False}

# Load AudioSeal model ONCE
print("Loading AudioSeal model")
model = AudioSeal.load_generator("audioseal_wm_16bits")
print("AudioSeal model ready")
preload_models()
detector = AudioSeal.load_detector(("audioseal_detector_16bits"))
print("AudioSeal detector ready")



@app.route("/generate", methods=["POST", "OPTIONS"])
def generate_tts():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS OK"}), 200

    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Missing text"}), 400

    print(f"Generating Bark audio for: {text}")

    #Bark generation
    with torch.no_grad():
        bark_audio = generate_audio(text)

    #Convert to float32 + normalize
    bark_audio = np.array(bark_audio, dtype=np.float32)
    bark_audio = bark_audio / np.max(np.abs(bark_audio) + 1e-9)

    #max 10s  generated audio
    max_len = SAMPLE_RATE * 10
    if len(bark_audio) > max_len:
        bark_audio = bark_audio[:max_len]

    #Watermark with audioSeal
    audio_tensor = torch.tensor(bark_audio, dtype=torch.float32)
    with torch.no_grad():
        watermarked = watermark_audio(model, audio_tensor, SAMPLE_RATE)

    watermarked_np = watermarked.squeeze().detach().cpu().numpy()
    watermarked_np = watermarked_np / np.max(np.abs(watermarked_np) + 1e-9)

    #Encode WAVs to Base64
    def to_base64(np_audio):
        buf = io.BytesIO()
        sf.write(buf, np_audio, SAMPLE_RATE, format="WAV")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    return jsonify({
        "unwatermarked": to_base64(bark_audio),
        "watermarked": to_base64(watermarked_np)
    })




@app.route("/detect", methods=["POST", "OPTIONS"])
def detect_audio():
    try:
        if request.method == "OPTIONS":
            return jsonify({"message": "CORS OK"}), 200

        data = request.get_json()
        if not data or "audio" not in data:
            return jsonify({"error": "Missing audio"}), 400

        audio_base64 = data["audio"]
        audio_bytes = base64.b64decode(audio_base64)
        audio_buf = io.BytesIO(audio_bytes)

        try:
            audio = AudioSegment.from_file(audio_buf, format="webm")
        except Exception:
            audio_buf.seek(0)
            audio = AudioSegment.from_file(audio_buf, format="wav")


        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples /= np.iinfo(audio.array_type).max
        sr = audio.frame_rate

        # Convert to tensor
        audio_tensor = torch.tensor(samples, dtype=torch.float32)
        if audio_tensor.ndim == 1:
            audio_tensor = audio_tensor.unsqueeze(0).unsqueeze(0)

        # Run detection
        with torch.no_grad():
            result, message = detector.detect_watermark(
                audio_tensor, sr, message_threshold=0.5
            )

        print("Detection result:", result)
        print("Decoded message:", message)

        score = (
            float(result.get("score", 0)) * 100
            if isinstance(result, dict)
            else float(result) * 100
        )

        return jsonify({"score": round(score, 2)}), 200

    except Exception as e:
        print("Detection error:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------------------------
# Run Flask
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
