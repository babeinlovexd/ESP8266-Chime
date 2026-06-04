from pydub import AudioSegment
from pydub.silence import split_on_silence
import glob

def trim_silence(filepath):
    audio = AudioSegment.from_wav(filepath)
    # simple heuristic for leading/trailing silence
    def trim(sound):
        start_trim = 0
        end_trim = len(sound)

        for ms in range(len(sound)):
            chunk = sound[ms:ms+1]
            if chunk.dBFS > -45.0:
                start_trim = max(0, ms - 100) # Keep 100ms before
                break

        for ms in range(len(sound)-1, -1, -1):
            chunk = sound[ms-1:ms]
            if chunk.dBFS > -45.0:
                end_trim = min(len(sound), ms + 100) # Keep 100ms after
                break

        if start_trim >= end_trim:
            return sound # fallback

        return sound[start_trim:end_trim]

    trimmed = trim(audio)
    print(f"{filepath}: {len(audio)}ms -> {len(trimmed)}ms")
    trimmed.export(filepath, format="wav")

for f in glob.glob("sound_tts_*.wav"):
    trim_silence(f)
