import sounddevice as sd
import numpy as np

fs = 24000  # Sample rate
duration = 2  # seconds
f = 440.0  # Sine frequency, Hz

samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
sd.play(samples, fs)
sd.wait() 