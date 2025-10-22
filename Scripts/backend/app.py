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

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os

# explicitly set paths for ffmpeg and ffprobe
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe   = r"C:\ffmpeg\bin\ffprobe.exe"

load_dotenv()

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



app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Allow CORS preflight requests
        if request.method == "OPTIONS":
            return jsonify({"message": "Preflight OK"}), 200

        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, email, password = data['username'], data['email'], data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Force PBKDF2 (standard, stable)
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/verify-token', methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({
        'valid': True,
        'username': current_user.username,
        'email': current_user.email
    }), 200


@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'username': current_user.username,
        'email': current_user.email
    }), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data['email'], data['password']
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token, 'username': user.username})

@app.route("/generate", methods=["POST", "OPTIONS"])
@token_required
def generate_tts(current_user):
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
@token_required
def detect_audio(current_user):
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
    print("Starting Flask backend...")
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
