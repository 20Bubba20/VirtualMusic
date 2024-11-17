import pyaudio
import numpy as np

p = pyaudio.PyAudio()

# Parameters
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 5.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# Generate samples
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# Open stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Play. May repeat with different volume values (if done interactively) 
# stream.write(volume*samples)

# stream.stop_stream()
notes = {
    'C3': 130.81,
    'C3#': 138.59,
    'D3': 146.83,
    'D3#': 155.56,
    'E3': 164.81,
    'F3': 174.61,
    'F3#': 185,
    'G3': 196,
    'G3#': 207.65,
    'A3': 220,
    'A3#': 233.08,
    'B3': 249.94,
    'C4': 261.63,
    'C4#': 277.18,
    'D4': 293.66,
    'D4#': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F4#': 369.99,
    'G4': 392,
    'G4#': 415.30,
    'A4': 440,
    'A4#': 466.16,
    'B4': 493.88
}

duration = 2
for note, frequency in notes.items():
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*(frequency)/fs)).astype(np.float32)
    # stream.start_stream()
    stream.write(volume*samples)
    # stream.stop_stream()
    
stream.close()

p.terminate()