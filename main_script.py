import os
import yaml
import gradio as gr
from scripts.gradio_interface import create_interface
from scripts.utility_misc import get_soundcard_list, load_samples, unload_samples, save_settings

# Load settings
with open('.\\data\\settings_general.yaml', 'r') as f:
    settings = yaml.safe_load(f)

# Globals
samples = settings.get('samples', [''] * 10)
selected_soundcard = settings.get('selected_soundcard', '')

def main():
    global selected_soundcard
    # Get list of soundcards
    soundcards = get_soundcard_list()
    
    # Create and launch Gradio interface
    iface = create_interface(samples, soundcards, selected_soundcard)
    iface.launch()

if __name__ == "__main__":
    main()
