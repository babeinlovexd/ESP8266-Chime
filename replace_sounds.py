import re

with open("generate_sounds.py", "r") as f:
    content = f.read()

# Replace gen_cyberpunk
new_cyberpunk = """def gen_cyberpunk():
    sr = 8000
    samples = []
    # Glitchy synth sweep
    for i in range(int(sr * 1.5)):
        freq = 100 + 1500 * (1 - (i / (sr * 1.5))**2)
        if (i // 100) % 2 == 0:
            samples.append(0.6 * math.sin(2 * math.pi * freq * i / sr))
        else:
            samples.append(-0.6 * math.sin(2 * math.pi * (freq * 1.5) * i / sr))
    generate_wav('sound_cyberpunk.wav', samples)"""
content = re.sub(r'def gen_cyberpunk\(\):.*?generate_wav\(\'sound_cyberpunk\.wav\', samples\)', new_cyberpunk, content, flags=re.DOTALL)

# Replace gen_ui_click1 (Sharp futuristic tick)
new_ui_click1 = """def gen_ui_click1():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.1)):
        env = math.exp(-i / (sr * 0.02))
        samples.append(env * 0.8 * math.sin(2 * math.pi * 2000 * i / sr))
    generate_wav('sound_ui_click1.wav', samples)"""
content = re.sub(r'def gen_ui_click1\(\):.*?generate_wav\(\'sound_ui_click1\.wav\', samples\)', new_ui_click1, content, flags=re.DOTALL)

# Replace gen_ui_click2 (Double soft blip)
new_ui_click2 = """def gen_ui_click2():
    sr = 8000
    samples = []
    for _ in range(2):
        for i in range(int(sr * 0.05)):
            env = math.exp(-i / (sr * 0.015))
            samples.append(env * 0.7 * math.sin(2 * math.pi * 1200 * i / sr))
        for i in range(int(sr * 0.02)):
            samples.append(0.0)
    generate_wav('sound_ui_click2.wav', samples)"""
content = re.sub(r'def gen_ui_click2\(\):.*?generate_wav\(\'sound_ui_click2\.wav\', samples\)', new_ui_click2, content, flags=re.DOTALL)

# Replace gen_ui_click3 (Confirmation chirp)
new_ui_click3 = """def gen_ui_click3():
    sr = 8000
    samples = []
    for i in range(int(sr * 0.15)):
        freq = 800 + 1000 * (i / (sr * 0.15))
        env = math.exp(-i / (sr * 0.05))
        samples.append(env * 0.8 * math.sin(2 * math.pi * freq * i / sr))
    generate_wav('sound_ui_click3.wav', samples)"""
content = re.sub(r'def gen_ui_click3\(\):.*?generate_wav\(\'sound_ui_click3\.wav\', samples\)', new_ui_click3, content, flags=re.DOTALL)

# Replace gen_wood_knock (Deep resonant knock)
new_wood_knock = """def gen_wood_knock():
    sr = 8000
    samples = []
    for _ in range(2):
        for i in range(int(sr * 0.1)):
            env = math.exp(-i / (sr * 0.02))
            noise = random.random() * 0.3
            samples.append(env * (0.8 * math.sin(2 * math.pi * 200 * i / sr) + noise))
        for i in range(int(sr * 0.15)):
            samples.append(0.0)
    generate_wav('sound_wood_knock.wav', samples)"""
content = re.sub(r'def gen_wood_knock\(\):.*?generate_wav\(\'sound_wood_knock\.wav\', samples\)', new_wood_knock, content, flags=re.DOTALL)

with open("generate_sounds.py", "w") as f:
    f.write(content)
