import wave
import struct
import math
import os

SAMPLE_RATE = 8000
DURATION = 2 # 2 seconds to keep size small for ESP8266 Flash

def generate_tone(filename, frequency1, frequency2=None, pattern="solid"):
    filepath = os.path.join("Sounds", filename + ".wav")
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1) # mono
        wav_file.setsampwidth(1) # 8-bit unsigned
        wav_file.setframerate(SAMPLE_RATE)

        for i in range(int(SAMPLE_RATE * DURATION)):
            t = float(i) / SAMPLE_RATE

            # Simple patterns
            if pattern == "dingdong":
                freq = frequency1 if t < DURATION/2 else frequency2
                vol = 1.0 - (t % (DURATION/2)) / (DURATION/2) # fade out
            elif pattern == "trill":
                freq = frequency1 if (i // 500) % 2 == 0 else frequency2
                vol = 1.0
            elif pattern == "sweep":
                freq = frequency1 + (frequency2 - frequency1) * t / DURATION
                vol = 1.0
            else:
                freq = frequency1
                vol = 1.0 - (t / DURATION)

            # Sine wave
            value = math.sin(2.0 * math.pi * freq * t) * vol

            # Convert to 8-bit unsigned (0-255)
            sample = int((value + 1.0) * 127.5)
            sample = max(0, min(255, sample))

            data = struct.pack('<B', sample)
            wav_file.writeframesraw(data)

def generate_header(filename, varname):
    wav_path = os.path.join("Sounds", filename + ".wav")
    h_path = os.path.join("Sounds", filename + ".h")

    with open(wav_path, "rb") as f:
        data = f.read()

    with open(h_path, "w") as f:
        f.write(f"#pragma once\n\n")
        f.write(f"#include <pgmspace.h>\n\n")
        f.write(f"const uint8_t {varname}[] PROGMEM = {{\n")
        for i in range(0, len(data), 12):
            chunk = data[i:i+12]
            f.write("  " + ", ".join([f"0x{b:02x}" for b in chunk]) + ",\n")
        f.write("};\n\n")
        f.write(f"const size_t {varname}_len = sizeof({varname});\n")

print("Generating sounds...")
generate_tone("sound_dingdong", 659.25, 523.25, "dingdong") # E5 to C5
generate_header("sound_dingdong", "sound_1_data")

generate_tone("sound_trill", 880.0, 1046.50, "trill") # A5 and C6
generate_header("sound_trill", "sound_2_data")

generate_tone("sound_sweep", 440.0, 880.0, "sweep") # A4 to A5
generate_header("sound_sweep", "sound_3_data")

generate_tone("sound_beep", 1000.0, None, "solid")
generate_header("sound_beep", "sound_4_data")

generate_tone("sound_chime", 783.99, None, "solid") # G5
generate_header("sound_chime", "sound_5_data")

print("Done.")
