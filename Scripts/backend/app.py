from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:8888"])  # allow Vue on port 8888

progress = {"value": 0, "running": False}

from audioseal import AudioSeal


def watermark_generated_audio(audio, sample_rate=16000, payload=None, strength=0.2):
    if isinstance(audio, np.ndarray):
        audio_tensor = torch.tensor(audio, dtype=torch.float32).unsqueeze(0)
    else:
        audio_tensor = audio.unsqueeze(0) if audio.ndim == 1 else audio


    if payload is None:
        payload = np.random.randint(0, 2, 16, dtype=np.int32)
    payload_tensor = torch.tensor(payload, dtype=torch.int32)


    model = AudioSeal.load_model("audiocaps_base")

    # Encode watermark
    encoded_audio, _ = model.encode(audio_tensor, payload_tensor)


    if strength < 1.0:
        encoded_audio = audio_tensor + strength * (encoded_audio - audio_tensor)


    encoded_audio = torch.clamp(encoded_audio, -1.0, 1.0).squeeze().numpy()



    return encoded_audio


@app.route("/audio", methods=["GET"])
def generate_and_send_audio():

    text = request.get_json()

    bark_audio = generate_audio(text, history_prompt="v2/en_speaker_6")

    watermarked_audio = watermark_generated_audio(
        bark_audio,
        model=audio_seal_model,
        sample_rate=SAMPLE_RATE,
        strength=0.25
    )


    buffer = io.BytesIO()
    wav_write(buffer, SAMPLE_RATE, (watermarked_audio * 32767).astype(np.int16))
    buffer.seek(0)

    return send_file(buffer, mimetype="audio/wav", as_attachment=False)


def run_progress():
    progress["running"] = True
    progress["value"] = 0
    while progress["value"] < 95:
        progress["value"] += 1
        time.sleep(0.01)
    progress["running"] = False

@app.route("/start", methods=["POST"])
def start_progress():
    if not progress["running"]:
        Thread(target=run_progress, daemon=True).start()
    return jsonify({"message": "started"})

@app.route("/progress", methods=["GET"])
def get_progress():
    return jsonify({"value": progress["value"]})

if __name__ == "__main__":
    app.run(debug=True)
    model = AudioSeal.load_model("audiocaps_base")