# .\scripts\utility_misc.py

# Imports Froms
import sounddevice as sd
import yaml
import os
from pydub import AudioSegment

def get_soundcard_list():
    devices = sd.query_devices()
    soundcards = [device['name'] for device in devices if device['max_output_channels'] > 0]
    return soundcards

def load_settings(settings_path='.\data\settings_general.yaml'):
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = yaml.safe_load(f)
            samples = settings.get('samples', [''] * 8)
            selected_soundcard = settings.get('selected_soundcard', '')
            volume = settings.get('volume', 100)
    else:
        samples = [''] * 8
        selected_soundcard = ""
        volume = 100
    return samples, selected_soundcard, volume

def unload_samples():
    return [''] * 8, [""] * 8 + [""] * 8  # Return empty samples and empty values for both filename and length

def save_settings(samples, selected_soundcard, volume, settings_path='.\data\settings_general.yaml'):
    with open(settings_path, 'w') as f:
        yaml.safe_dump({'samples': samples, 'selected_soundcard': selected_soundcard, 'volume': volume}, f)

def get_sample_length(file_path):
    try:
        audio = AudioSegment.from_wav(file_path)
        return f"Length: {int(audio.duration_seconds // 60):02}:{int(audio.duration_seconds % 60):02}"
    except:
        return "Length: Unknown"

def set_volume(audio, volume_percent):
    return audio + (volume_percent - 100)  # pydub uses dB, so we need to convert percentage to dB
