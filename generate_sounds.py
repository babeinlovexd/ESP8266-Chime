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


import random

def gen_washing_machine():
    sr = 8000
    samples = []
    for _ in range(3):
        for i in range(int(sr * 0.15)):
            env = math.exp(-i / (sr * 0.05))
            samples.append(env * math.sin(2 * math.pi * 400 * i / sr))
        for i in range(int(sr * 0.1)):
            samples.append(0.0)
    generate_wav('sound_washing_machine.wav', samples)

def gen_mail_delivered():
    sr = 8000
    samples = []
    notes = [523.25, 659.25, 783.99, 1046.50]
    for n in notes:
        for i in range(int(sr * 0.15)):
            env = math.exp(-i / (sr * 0.1))
            samples.append(env * math.sin(2 * math.pi * n * i / sr))
    generate_wav('sound_mail_delivered.wav', samples)

def gen_window_open():
    sr = 8000
    samples = []
    for _ in range(2):
        for i in range(int(sr * 0.2)):
            env = math.exp(-i / (sr * 0.1))
            samples.append(env * math.sin(2 * math.pi * 1200 * i / sr))
        for i in range(int(sr * 0.2)):
            samples.append(0.0)
    generate_wav('sound_window_open.wav', samples)

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

def gen_access_granted():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.2)):
        env = math.exp(-i / (sr * 0.1))
        samples.append(env * math.sin(2 * math.pi * 880 * i / sr))
    for i in range(int(sr * 0.4)):
        env = math.exp(-i / (sr * 0.2))
        samples.append(env * math.sin(2 * math.pi * 1318.51 * i / sr))
    generate_wav('sound_access_granted.wav', samples)

def gen_level_up():
    sr = 8000
    samples = []
    notes = [440, 554.37, 659.25, 880, 1108.73, 1318.51]
    for n in notes:
        for i in range(int(sr * 0.1)):
            samples.append(0.4 * math.sin(2 * math.pi * n * i / sr))
    generate_wav('sound_level_up.wav', samples)

def gen_game_over():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.8)):
        freq = max(100, 800 - 800 * (i / (sr * 0.8)))
        samples.append(0.4 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_game_over.wav', samples)

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

def gen_arcade_start():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.5)):
        freq = 400 + 400 * math.sin(2 * math.pi * 10 * i / sr)
        samples.append(0.4 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_arcade_start.wav', samples)

def gen_sci_fi_alert():
    sr = 8000
    samples = []
    for _ in range(3):
        for i in range(int(sr * 0.3)):
            freq = 1000 + 500 * math.sin(2 * math.pi * 15 * i / sr)
            samples.append(0.4 * math.sin(2 * math.pi * freq * i / sr))
        for i in range(int(sr * 0.1)):
            samples.append(0.0)
    generate_wav('sound_sci_fi_alert.wav', samples)

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

def gen_bass_drop():
    sr = 8000
    samples = []
    for i in range(int(sr * 1.5)):
        freq = max(30, 200 - 170 * (i / (sr * 1.5)))
        samples.append(0.6 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_bass_drop.wav', samples)


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

def gen_noti_pop():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.08)):
        freq = 1500 - 1000 * (i / (sr * 0.08))
        env = math.exp(-i / (sr * 0.02))
        samples.append(env * 0.9 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_noti_pop.wav', samples)

def gen_noti_sparkle():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.3)):
        freq1 = 2000 + 500 * math.sin(2 * math.pi * 10 * i / sr)
        freq2 = 2500 + 500 * math.cos(2 * math.pi * 12 * i / sr)
        env = math.exp(-i / (sr * 0.15))
        samples.append(env * 0.5 * (math.sin(2 * math.pi * freq1 * i / sr) + math.sin(2 * math.pi * freq2 * i / sr)))
    generate_wav('sound_noti_sparkle.wav', samples)

def gen_noti_alert():
    sr = 8000
    samples = []
    for _ in range(2):
        for i in range(int(sr * 0.1)):
            env = math.exp(-i / (sr * 0.05))
            samples.append(env * 0.8 * math.sin(2 * math.pi * 880 * i / sr))
        for i in range(int(sr * 0.05)):
            samples.append(0.0)
    generate_wav('sound_noti_alert.wav', samples)

def wav_to_h():
    files = [
        'sound_dingdong.wav', 'sound_trill.wav', 'sound_sweep.wav', 'sound_beep.wav', 'sound_chime.wav',
        'sound_siren.wav', 'sound_doorbell.wav', 'sound_notification.wav', 'sound_error.wav', 'sound_success.wav',
        'sound_washing_machine.wav', 'sound_mail_delivered.wav', 'sound_window_open.wav', 'sound_pre_alarm.wav', 'sound_access_granted.wav',
        'sound_noti_chime.wav', 'sound_noti_bloop.wav', 'sound_noti_pop.wav', 'sound_noti_sparkle.wav', 'sound_level_up.wav',
        'sound_game_over.wav', 'sound_coin.wav', 'sound_noti_alert.wav', 'sound_glass_ping.wav', 'sound_elevator_ding.wav',
        'sound_arcade_start.wav', 'sound_sci_fi_alert.wav', 'sound_soft_bell.wav', 'sound_magic_sparkle.wav', 'sound_bass_drop.wav',

        'sound_tts_essen.wav', 'sound_tts_waschmaschine.wav', 'sound_tts_trockner.wav',
        'sound_tts_post.wav', 'sound_tts_runter.wav', 'sound_tts_muell_schwarz.wav',
        'sound_tts_muell_gruen.wav', 'sound_tts_muell_gelb.wav', 'sound_tts_glas.wav',
        'sound_tts_zaehne.wav'
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

if __name__ == "__main__":
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
    gen_washing_machine()
    gen_mail_delivered()
    gen_window_open()
    gen_pre_alarm()
    gen_access_granted()
    gen_level_up()
    gen_game_over()
    gen_coin()
    gen_glass_ping()
    gen_elevator_ding()
    gen_arcade_start()
    gen_sci_fi_alert()
    gen_soft_bell()
    gen_magic_sparkle()
    gen_bass_drop()
    gen_noti_chime()
    gen_noti_bloop()
    gen_noti_pop()
    gen_noti_sparkle()
    gen_noti_alert()
    wav_to_h()
