import sounddevice as sd
import os

def get_soundcard_list():
    devices = sd.query_devices()
    soundcards = [device['name'] for device in devices if device['max_output_channels'] > 0]
    return soundcards

def load_samples():
    pass

def unload_samples():
    global samples
    samples = [''] * 10

def save_settings():
    pass
