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


def gen_chime():
    # G5 (783.99 Hz)
    sr = 8000
    samples = []
    for i in range(int(sr * 1.5)):
        env = math.exp(-i / (sr * 0.4))
        samples.append(env * math.sin(2 * math.pi * 783.99 * i / sr))
    generate_wav('sound_chime.wav', samples)


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





def gen_pre_alarm():
    sr = 8000
    samples = []
    for _ in range(4):
        for i in range(int(sr * 0.1)):
            freq = 400 + 400 * (i / (sr * 0.1))
            samples.append(0.5 * math.sin(2 * math.pi * freq * i / sr))
        for i in range(int(sr * 0.1)):
            samples.append(0.0)
    generate_wav('sound_pre_alarm.wav', samples)


def gen_level_up():
    sr = 8000
    samples = []
    notes = [440, 554.37, 659.25, 880, 1108.73, 1318.51]
    for n in notes:
        for i in range(int(sr * 0.1)):
            samples.append(0.4 * math.sin(2 * math.pi * n * i / sr))
    generate_wav('sound_level_up.wav', samples)


def gen_coin():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.1)):
        samples.append(0.3 * math.sin(2 * math.pi * 987.77 * i / sr))
    for i in range(int(sr * 0.3)):
        env = math.exp(-i / (sr * 0.1))
        samples.append(env * math.sin(2 * math.pi * 1318.51 * i / sr))
    generate_wav('sound_coin.wav', samples)

def gen_glass_ping():
    sr = 8000
    samples = []
    for i in range(int(sr * 1.5)):
        env = math.exp(-i / (sr * 0.3))
        samples.append(env * 0.4 * math.sin(2 * math.pi * 2000 * i / sr))
    generate_wav('sound_glass_ping.wav', samples)

def gen_elevator_ding():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.4)):
        env = math.exp(-i / (sr * 0.2))
        samples.append(env * math.sin(2 * math.pi * 880 * i / sr))
    for i in range(int(sr * 0.6)):
        env = math.exp(-i / (sr * 0.3))
        samples.append(env * math.sin(2 * math.pi * 659.25 * i / sr))
    generate_wav('sound_elevator_ding.wav', samples)



def gen_soft_bell():
    sr = 8000
    samples = []
    for i in range(int(sr * 1.2)):
        env = math.exp(-i / (sr * 0.4))
        samples.append(env * 0.5 * math.sin(2 * math.pi * 600 * i / sr))
    generate_wav('sound_soft_bell.wav', samples)

def gen_magic_sparkle():
    sr = 8000
    samples = []
    notes = [1000, 1500, 1200, 1800, 1400, 2000, 1600, 2200]
    for n in notes:
        for i in range(int(sr * 0.08)):
            env = math.exp(-i / (sr * 0.04))
            samples.append(env * 0.3 * math.sin(2 * math.pi * n * i / sr))
    generate_wav('sound_magic_sparkle.wav', samples)



def gen_noti_chime():
    sr = 8000
    samples = []
    notes = [1046.50, 1318.51] # C6, E6
    for n in notes:
        for i in range(int(sr * 0.2)):
            env = math.exp(-i / (sr * 0.1))
            samples.append(env * 0.7 * math.sin(2 * math.pi * n * i / sr))
    generate_wav('sound_noti_chime.wav', samples)

def gen_noti_bloop():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.15)):
        freq = 300 + 800 * (i / (sr * 0.15))
        env = math.exp(-i / (sr * 0.05))
        samples.append(env * 0.8 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_noti_bloop.wav', samples)




def wav_to_h():
    files = [
        'sound_dingdong.wav', 'sound_trill.wav', 'sound_sweep.wav', 'sound_chime.wav',
        'sound_doorbell.wav',
        'sound_pre_alarm.wav',
        'sound_noti_chime.wav', 'sound_noti_bloop.wav', 'sound_level_up.wav',
        'sound_coin.wav', 'sound_glass_ping.wav', 'sound_elevator_ding.wav',
        'sound_soft_bell.wav', 'sound_magic_sparkle.wav',
        'sound_tts_essen.wav', 'sound_tts_waschmaschine.wav', 'sound_tts_trockner.wav',
        'sound_tts_post.wav', 'sound_tts_muell_schwarz.wav',
        'sound_tts_muell_gruen.wav', 'sound_tts_muell_gelb.wav', 'sound_tts_glas.wav',

    ]

    fragments = ["#pragma once\n#include <pgmspace.h>\n\n"]
    for f in files:
        with open(f, 'rb') as w:
            data = w.read()
        name = f.replace('.wav', '')
        fragments.append(f"const unsigned char {name}[] PROGMEM = {{\n")
        fragments.append(", ".join([f"0x{b:02x}" for b in data]))
        fragments.append(f"\n}};\nconst unsigned int {name}_len = {len(data)};\n\n")
    with open('sounds.h', 'w') as out_f:
        out_f.write("".join(fragments))

if __name__ == "__main__":
    gen_dingdong()
    gen_trill()
    gen_sweep()
    gen_chime()
    gen_doorbell()
    gen_pre_alarm()
    gen_level_up()
    gen_coin()
    gen_glass_ping()
    gen_elevator_ding()
    gen_soft_bell()
    gen_magic_sparkle()
    gen_noti_chime()
    gen_noti_bloop()
    wav_to_h()
