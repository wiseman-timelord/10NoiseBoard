# .\scripts\utility_misc.py

import sounddevice as sd
import yaml
import os
from pydub import AudioSegment

def get_soundcard_list():
    return [device['name'] for device in sd.query_devices() if device['max_output_channels'] > 0]

def manage_settings(action='load', samples=None, selected_soundcard=None, volume=None, settings_path='./data/settings_general.yaml'):
    if action == 'load':
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings = yaml.safe_load(f)
                return (settings.get('samples', [''] * 8),
                        settings.get('selected_soundcard', ''),
                        settings.get('volume', 100))
        return [''] * 8, "", 100
    elif action == 'save':
        with open(settings_path, 'w') as f:
            yaml.safe_dump({'samples': samples, 'selected_soundcard': selected_soundcard, 'volume': volume}, f)

def get_sample_length(file_path):
    try:
        audio = AudioSegment.from_wav(file_path)
        return f"{int(audio.duration_seconds // 60):02}:{int(audio.duration_seconds % 60):02}"
    except:
        return "Length: Unknown"

def set_volume(audio, volume_percent):
    return audio + (volume_percent - 100)  # pydub uses dB, so we need to convert percentage to dB