# stt.py
# Placeholder for speech-to-text logic using Vosk 

import vosk
import sounddevice as sd
import queue
import json
from config import VOSK_MODEL_PATH
import os

q = queue.Queue()

# Callback to put audio data in queue
def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_and_transcribe():
    if not os.path.exists(VOSK_MODEL_PATH):
        print(f"Vosk model not found at {VOSK_MODEL_PATH}. Please download it from https://alphacephei.com/vosk/models and place it in the correct directory.")
        return None
    try:
        model = vosk.Model(VOSK_MODEL_PATH)
    except Exception as e:
        print(f"Failed to load Vosk model: {e}")
        return None

    samplerate = 16000
    device = None  # Use default input device
    rec = vosk.KaldiRecognizer(model, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16', channels=1, callback=callback):
        print("Listening... Speak now!")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                text = json.loads(result).get('text', '')
                if text:
                    print(f"Recognized: {text}")
                    return text 