import re

with open("generate_sounds.py", "r") as f:
    content = f.read()

# Remove the old functions
for func in ['gen_cyberpunk', 'gen_ui_click1', 'gen_ui_click2', 'gen_ui_click3', 'gen_wood_knock']:
    content = re.sub(f'def {func}\(\):.*?generate_wav\(\'.*?\.wav\', samples\)\n\n', '', content, flags=re.DOTALL)

# Also remove from bottom
content = content.replace("    gen_cyberpunk()\n", "")
content = content.replace("    gen_ui_click1()\n", "")
content = content.replace("    gen_ui_click2()\n", "")
content = content.replace("    gen_ui_click3()\n", "")
content = content.replace("    gen_wood_knock()\n", "")

# Remove from files list
for file in ['sound_cyberpunk.wav', 'sound_ui_click1.wav', 'sound_ui_click2.wav', 'sound_ui_click3.wav', 'sound_wood_knock.wav']:
    content = content.replace(f"'{file}', ", "")
    content = content.replace(f"'{file}'", "")

# Add the new notification functions
new_functions = """
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
"""

content = content.replace("def wav_to_h():", new_functions + "\ndef wav_to_h():")

# Add to main block
main_addition = """    gen_noti_chime()
    gen_noti_bloop()
    gen_noti_pop()
    gen_noti_sparkle()
    gen_noti_alert()
"""
content = content.replace("    wav_to_h()", main_addition + "    wav_to_h()")

# Add to files list - reconstruct it cleanly to avoid mess
import re
files_pattern = re.compile(r"files = \[\n.*?\]", re.DOTALL)
new_files_list = """files = [
        'sound_dingdong.wav', 'sound_trill.wav', 'sound_sweep.wav', 'sound_beep.wav', 'sound_chime.wav',
        'sound_siren.wav', 'sound_doorbell.wav', 'sound_notification.wav', 'sound_error.wav', 'sound_success.wav',
        'sound_washing_machine.wav', 'sound_mail_delivered.wav', 'sound_window_open.wav', 'sound_pre_alarm.wav', 'sound_access_granted.wav',
        'sound_noti_chime.wav', 'sound_noti_bloop.wav', 'sound_noti_pop.wav', 'sound_noti_sparkle.wav', 'sound_level_up.wav',
        'sound_game_over.wav', 'sound_coin.wav', 'sound_noti_alert.wav', 'sound_glass_ping.wav', 'sound_elevator_ding.wav',
        'sound_arcade_start.wav', 'sound_sci_fi_alert.wav', 'sound_soft_bell.wav', 'sound_magic_sparkle.wav', 'sound_bass_drop.wav'
    ]"""
content = files_pattern.sub(new_files_list, content)

with open("generate_sounds.py", "w") as f:
    f.write(content)
