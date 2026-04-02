import re

with open("generate_sounds.py", "r") as f:
    content = f.read()

new_functions = """
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

def gen_cyberpunk():
    sr = 8000
    samples = []
    random.seed(42)
    for i in range(int(sr * 1.0)):
        freq = random.randint(200, 2000) if i % 200 < 100 else 0
        samples.append(0.3 * math.sin(2 * math.pi * freq * i / sr) * random.random())
    generate_wav('sound_cyberpunk.wav', samples)

def gen_ui_click1():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.05)):
        env = math.exp(-i / (sr * 0.01))
        samples.append(env * math.sin(2 * math.pi * 1500 * i / sr))
    generate_wav('sound_ui_click1.wav', samples)

def gen_ui_click2():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.05)):
        env = math.exp(-i / (sr * 0.01))
        samples.append(env * math.sin(2 * math.pi * 400 * i / sr))
    generate_wav('sound_ui_click2.wav', samples)

def gen_ui_click3():
    sr = 8000
    samples = []
    for _ in range(2):
        for i in range(int(sr * 0.03)):
            env = math.exp(-i / (sr * 0.01))
            samples.append(env * math.sin(2 * math.pi * 1000 * i / sr))
        for i in range(int(sr * 0.02)):
            samples.append(0.0)
    generate_wav('sound_ui_click3.wav', samples)

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

def gen_wood_knock():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.08)):
        env = math.exp(-i / (sr * 0.015))
        noise = random.random() * 0.5
        samples.append(env * (0.5 * math.sin(2 * math.pi * 150 * i / sr) + noise))
    generate_wav('sound_wood_knock.wav', samples)

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

"""

# Insert new functions before wav_to_h
content = content.replace("def wav_to_h():", new_functions + "def wav_to_h():")

# Update wav_to_h files list
old_files_list = """    files = [
        'sound_dingdong.wav', 'sound_trill.wav', 'sound_sweep.wav', 'sound_beep.wav', 'sound_chime.wav',
        'sound_siren.wav', 'sound_doorbell.wav', 'sound_notification.wav', 'sound_error.wav', 'sound_success.wav'
    ]"""
new_files_list = """    files = [
        'sound_dingdong.wav', 'sound_trill.wav', 'sound_sweep.wav', 'sound_beep.wav', 'sound_chime.wav',
        'sound_siren.wav', 'sound_doorbell.wav', 'sound_notification.wav', 'sound_error.wav', 'sound_success.wav',
        'sound_washing_machine.wav', 'sound_mail_delivered.wav', 'sound_window_open.wav', 'sound_pre_alarm.wav', 'sound_access_granted.wav',
        'sound_cyberpunk.wav', 'sound_ui_click1.wav', 'sound_ui_click2.wav', 'sound_ui_click3.wav', 'sound_level_up.wav',
        'sound_game_over.wav', 'sound_coin.wav', 'sound_wood_knock.wav', 'sound_glass_ping.wav', 'sound_elevator_ding.wav',
        'sound_arcade_start.wav', 'sound_sci_fi_alert.wav', 'sound_soft_bell.wav', 'sound_magic_sparkle.wav', 'sound_bass_drop.wav'
    ]"""
content = content.replace(old_files_list, new_files_list)

# Update main execution block
main_block = """    gen_success()
    wav_to_h()"""
new_main_block = """    gen_success()
    gen_washing_machine()
    gen_mail_delivered()
    gen_window_open()
    gen_pre_alarm()
    gen_access_granted()
    gen_cyberpunk()
    gen_ui_click1()
    gen_ui_click2()
    gen_ui_click3()
    gen_level_up()
    gen_game_over()
    gen_coin()
    gen_wood_knock()
    gen_glass_ping()
    gen_elevator_ding()
    gen_arcade_start()
    gen_sci_fi_alert()
    gen_soft_bell()
    gen_magic_sparkle()
    gen_bass_drop()
    wav_to_h()"""
content = content.replace(main_block, new_main_block)

with open("generate_sounds.py", "w") as f:
    f.write(content)
