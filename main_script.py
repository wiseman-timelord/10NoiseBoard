# .\main_script.py

# Imports Froms
import os
import yaml
import gradio as gr
from scripts.gradio_interface import create_interface
from scripts.utility_misc import get_soundcard_list, load_settings, save_settings, unload_samples

# Global variables
samples = [''] * 8
selected_soundcard = ""
volume = 100

def load_globals(settings_path='./data/settings_general.yaml'):
    global samples, selected_soundcard, volume
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

def save_globals(settings_path='./data/settings_general.yaml'):
    global samples, selected_soundcard, volume
    with open(settings_path, 'w') as f:
        yaml.safe_dump({'samples': samples, 'selected_soundcard': selected_soundcard, 'volume': volume}, f)

def main():
    global samples, selected_soundcard, volume
    
    # Load settings and initialize globals
    load_globals()
    
    # Get list of soundcards
    soundcards = get_soundcard_list()
    
    # Create and launch Gradio interface
    iface = create_interface(samples, soundcards, selected_soundcard, volume, 
                             update_samples=lambda x: globals().update({'samples': x}),
                             update_soundcard=lambda x: globals().update({'selected_soundcard': x}),
                             update_volume=lambda x: globals().update({'volume': x}),
                             save_settings=save_globals)
    iface.launch(inbrowser=True)  # Open in default browser

if __name__ == "__main__":
    main()
