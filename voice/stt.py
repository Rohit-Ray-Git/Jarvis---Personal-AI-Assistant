# stt.py
# Placeholder for speech-to-text logic using Vosk 

import vosk
import sounddevice as sd
import queue
import json
from config import VOSK_MODEL_PATH

q = queue.Queue()

# Callback to put audio data in queue
def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_and_transcribe():
    model = vosk.Model(VOSK_MODEL_PATH)
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