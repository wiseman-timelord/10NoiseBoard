# .\main_script.py

# Imports Froms
import os
import gradio as gr
from scripts.gradio_interface import create_interface
from scripts.utility_misc import get_soundcard_list, manage_settings

# Global variables
samples = [''] * 8
selected_soundcard = ""
volume = 100

def manage_globals(action):
    global samples, selected_soundcard, volume
    if action == 'load':
        samples, selected_soundcard, volume = manage_settings('load')
    elif action == 'save':
        manage_settings('save', samples, selected_soundcard, volume)

def main():
    manage_globals('load')
    soundcards = get_soundcard_list()
    
    iface = create_interface(
        samples, soundcards, selected_soundcard, volume,
        update_samples=lambda x: globals().update({'samples': x}),
        update_soundcard=lambda x: globals().update({'selected_soundcard': x}),
        update_volume=lambda x: globals().update({'volume': x}),
        save_settings=lambda: manage_globals('save')
    )
    iface.launch(inbrowser=True)
    
    # Add this line to keep the script running
    iface.block_thread()

if __name__ == "__main__":
    main()