import io
import math
import struct
import wave


def generate_tone_wav(frequency=880.0, duration_seconds=0.6, sample_rate=44100, volume=0.4):
    """Synthesizes a short sine-wave tone as WAV bytes.

    Used as a dependency-free, license-free stand-in for real audio assets
    (alarm alert, placeholder music track) - no files to ship or download.
    """
    n_samples = int(sample_rate * duration_seconds)
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            sample = volume * math.sin(2 * math.pi * frequency * (i / sample_rate))
            frames += struct.pack("<h", int(sample * 32767))

        wav_file.writeframes(bytes(frames))

    return buffer.getvalue()
