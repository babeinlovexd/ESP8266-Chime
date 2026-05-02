import wave
import struct
import os
import pytest
from unittest.mock import patch
from generate_sounds import generate_wav, gen_doorbell

def test_generate_wav(tmp_path):
    filename = str(tmp_path / "test.wav")
    # Samples: 0.0, 0.5, 1.0 (clamped), -0.5, -1.0 (clamped), 2.0 (clamped), -2.0 (clamped)
    samples = [0.0, 0.5, 1.0, -0.5, -1.0, 2.0, -2.0]
    sample_rate = 8000

    generate_wav(filename, samples, sample_rate)

    assert os.path.exists(filename)

    with wave.open(filename, 'r') as wav_file:
        assert wav_file.getnchannels() == 1
        assert wav_file.getsampwidth() == 2
        assert wav_file.getframerate() == sample_rate
        assert wav_file.getnframes() == len(samples)

        frames = wav_file.readframes(len(samples))
        # Expected values after clamping and conversion to 16-bit signed int
        # s = max(-32768, min(32767, int(s * 32767)))
        expected_values = [
            0,
            int(0.5 * 32767),
            32767,
            int(-0.5 * 32767),
            -32767, # int(-1.0 * 32767)
            32767,  # clamped
            -32768  # clamped
        ]

        actual_values = struct.unpack(f'<{len(samples)}h', frames)
        assert actual_values == tuple(expected_values)

def test_generate_wav_custom_rate(tmp_path):
    filename = str(tmp_path / "test_rate.wav")
    samples = [0.0] * 100
    sample_rate = 44100

    generate_wav(filename, samples, sample_rate)

    with wave.open(filename, 'r') as wav_file:
        assert wav_file.getframerate() == sample_rate

def test_gen_doorbell():
    with patch('generate_sounds.generate_wav') as mock_generate_wav:
        gen_doorbell()
        mock_generate_wav.assert_called_once()
        args, _ = mock_generate_wav.call_args
        assert args[0] == 'sound_doorbell.wav'
        # int(8000 * 0.4) + int(8000 * 0.8) = 3200 + 6400 = 9600
        assert len(args[1]) == 9600
