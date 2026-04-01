import wave
import struct
import math
import array

def generate_wav(filename, samples, sample_rate=8000):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        # buffer all samples using array for efficiency
        clamped_samples = array.array('h', (max(-32768, min(32767, int(s * 32767))) for s in samples))
        wav_file.writeframesraw(clamped_samples.tobytes())

def gen_dingdong():
    # Ding: 659.25 Hz (E5), Dong: 523.25 Hz (C5)
    sr = 8000
    samples = []
    # Ding
    for i in range(int(sr * 0.5)):
        env = math.exp(-i / (sr * 0.2))
        samples.append(env * math.sin(2 * math.pi * 659.25 * i / sr))
    # Dong
    for i in range(int(sr * 0.8)):
        env = math.exp(-i / (sr * 0.3))
        samples.append(env * math.sin(2 * math.pi * 523.25 * i / sr))
    generate_wav('sound_dingdong.wav', samples)

def gen_trill():
    sr = 8000
    samples = []
    for i in range(int(sr * 1.0)):
        freq = 1000 if (i // (sr // 20)) % 2 == 0 else 1200
        samples.append(0.5 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_trill.wav', samples)

def gen_sweep():
    sr = 8000
    samples = []
    for i in range(int(sr * 1.0)):
        freq = 400 + 600 * (i / (sr * 1.0))
        samples.append(0.5 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_sweep.wav', samples)

def gen_beep():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.5)):
        samples.append(0.5 * math.sin(2 * math.pi * 800 * i / sr))
    generate_wav('sound_beep.wav', samples)

def gen_chime():
    # G5 (783.99 Hz)
    sr = 8000
    samples = []
    for i in range(int(sr * 1.5)):
        env = math.exp(-i / (sr * 0.4))
        samples.append(env * math.sin(2 * math.pi * 783.99 * i / sr))
    generate_wav('sound_chime.wav', samples)

def gen_siren():
    sr = 8000
    samples = []
    for i in range(int(sr * 2.0)):
        freq = 600 + 200 * math.sin(2 * math.pi * 2 * i / sr)
        samples.append(0.5 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_siren.wav', samples)

def gen_doorbell():
    sr = 8000
    samples = []
    # Note 1
    for i in range(int(sr * 0.4)):
        env = math.exp(-i / (sr * 0.2))
        samples.append(env * math.sin(2 * math.pi * 700 * i / sr))
    # Note 2
    for i in range(int(sr * 0.8)):
        env = math.exp(-i / (sr * 0.3))
        samples.append(env * math.sin(2 * math.pi * 550 * i / sr))
    generate_wav('sound_doorbell.wav', samples)

def gen_notification():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.2)):
        env = math.exp(-i / (sr * 0.1))
        samples.append(env * math.sin(2 * math.pi * 880 * i / sr))
    for i in range(int(sr * 0.4)):
        env = math.exp(-i / (sr * 0.2))
        samples.append(env * math.sin(2 * math.pi * 1100 * i / sr))
    generate_wav('sound_notification.wav', samples)

def gen_error():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.3)):
        samples.append(0.5 * math.sin(2 * math.pi * 300 * i / sr))
    for i in range(int(sr * 0.1)):
        samples.append(0.0)
    for i in range(int(sr * 0.6)):
        samples.append(0.5 * math.sin(2 * math.pi * 250 * i / sr))
    generate_wav('sound_error.wav', samples)

def gen_success():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.2)):
        env = math.exp(-i / (sr * 0.1))
        samples.append(env * math.sin(2 * math.pi * 500 * i / sr))
    for i in range(int(sr * 0.2)):
        env = math.exp(-i / (sr * 0.1))
        samples.append(env * math.sin(2 * math.pi * 700 * i / sr))
    for i in range(int(sr * 0.5)):
        env = math.exp(-i / (sr * 0.2))
        samples.append(env * math.sin(2 * math.pi * 1000 * i / sr))
    generate_wav('sound_success.wav', samples)

gen_dingdong()
gen_trill()
gen_sweep()
gen_beep()
gen_chime()
gen_siren()
gen_doorbell()
gen_notification()
gen_error()
gen_success()

import os
def wav_to_h():
    files = [
        'sound_dingdong.wav', 'sound_trill.wav', 'sound_sweep.wav', 'sound_beep.wav', 'sound_chime.wav',
        'sound_siren.wav', 'sound_doorbell.wav', 'sound_notification.wav', 'sound_error.wav', 'sound_success.wav'
    ]
    out = "#pragma once\n#include <pgmspace.h>\n\n"
    for f in files:
        with open(f, 'rb') as w:
            data = w.read()
        name = f.replace('.wav', '')
        out += f"const unsigned char {name}[] PROGMEM = {{\n"
        out += ", ".join([f"0x{b:02x}" for b in data])
        out += f"\n}};\nconst unsigned int {name}_len = {len(data)};\n\n"
    with open('sounds.h', 'w') as out_f:
        out_f.write(out)

wav_to_h()
