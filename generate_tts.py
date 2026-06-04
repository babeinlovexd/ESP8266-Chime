from gtts import gTTS
from pydub import AudioSegment
import os

tts_de = {
    'sound_tts_essen_de': 'Essen ist fertig',
    'sound_tts_waschmaschine_de': 'Waschmaschine ist fertig',
    'sound_tts_trockner_de': 'Trockner ist fertig',
    'sound_tts_post_de': 'Post ist da',
    'sound_tts_muell_schwarz_de': 'Schwarze Mülltonne muss raus',
    'sound_tts_muell_gruen_de': 'Grüne Mülltonne muss raus',
    'sound_tts_muell_gelb_de': 'Gelbe Mülltonne muss raus',
    'sound_tts_glas_de': 'Glas muss raus'
}

tts_en = {
    'sound_tts_essen_en': 'Food is ready',
    'sound_tts_waschmaschine_en': 'Washing machine is done',
    'sound_tts_trockner_en': 'Dryer is done',
    'sound_tts_post_en': 'Mail has arrived',
    'sound_tts_muell_schwarz_en': 'Black bin needs to go out',
    'sound_tts_muell_gruen_en': 'Green bin needs to go out',
    'sound_tts_muell_gelb_en': 'Yellow bin needs to go out',
    'sound_tts_glas_en': 'Glass needs to go out'
}

def generate_tts(texts, lang):
    for filename, text in texts.items():
        print(f"Generating {filename} ({lang}): {text}")
        tts = gTTS(text=text, lang=lang)
        mp3_file = f"{filename}.mp3"
        tts.save(mp3_file)

        # Convert to 8000Hz 16-bit mono wav
        audio = AudioSegment.from_mp3(mp3_file)
        audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(2)

        # We replace _de or _en for the actual file if it was named something else,
        # but wait, let's keep the name as is.
        wav_file = f"{filename}.wav"
        audio.export(wav_file, format="wav")
        os.remove(mp3_file)

generate_tts(tts_de, 'de')
generate_tts(tts_en, 'en')
