# .\scripts\gradio_interface.py

import gradio as gr
import os
import tempfile
from pydub import AudioSegment
import simpleaudio as sa
import threading
from scripts.utility_misc import get_sample_length, set_volume, manage_settings

# Global dictionaries to store play objects and their associated threads
play_objects = {}
play_threads = {}

def load_sample(samples, column, update_samples):
    def inner(file):
        if file:
            samples[column] = file.name
            update_samples(samples)
            length = get_sample_length(file.name)
            return os.path.basename(file.name), length
        return "", ""
    return inner

def play_sample(samples, volume, column, action="-load"):
    global play_objects, play_threads
    
    if samples[column]:
        # Stop any currently playing sound for this column
        if column in play_objects and play_objects[column] is not None:
            play_objects[column].stop()
            if column in play_threads and play_threads[column] is not None:
                play_threads[column].join()  # Wait for the thread to finish

        audio = AudioSegment.from_wav(samples[column])
        audio = set_volume(audio, volume)
        
        # Convert the audio to raw PCM data
        raw_data = audio.raw_data
        
        # Get audio parameters
        num_channels = audio.channels
        bytes_per_sample = audio.sample_width
        sample_rate = audio.frame_rate
        
        # Play the audio using simpleaudio
        play_obj = sa.play_buffer(raw_data, num_channels, bytes_per_sample, sample_rate)
        
        # Store the play object
        play_objects[column] = play_obj

        # Start a new thread to wait for playback to finish
        def wait_for_playback():
            play_obj.wait_done()
            play_objects[column] = None
            play_threads[column] = None

        thread = threading.Thread(target=wait_for_playback, daemon=True)
        thread.start()
        play_threads[column] = thread

def create_interface(samples, soundcards, selected_soundcard, volume, update_samples, update_soundcard, update_volume, save_settings):
    with gr.Blocks(css=".file-box {height: 45px;}") as iface:
        # Top bar
        with gr.Row(variant="compact"):
            default_soundcard = selected_soundcard if selected_soundcard in soundcards else (soundcards[0] if soundcards else None)
            soundcard_select = gr.Dropdown(label="Output Soundcard", choices=soundcards, value=default_soundcard)
            volume_slider = gr.Slider(minimum=0, maximum=100, value=volume, step=1, label="Volume")
        
        # Main content area with 8 columns
        with gr.Row():
            columns = []
            for i in range(8):
                with gr.Column(scale=1, min_width=100):
                    sample_name = gr.Textbox(label=f"Sample {i+1}", value=os.path.basename(samples[i]), interactive=False, lines=3)
                    sample_length = gr.Textbox(label="Length", value=get_sample_length(samples[i]) if samples[i] else "", interactive=False)
                    play_button = gr.Button("Play")
                    load_button = gr.File(label="Load", type="filepath", interactive=True, elem_classes="file-box")
                    columns.append((sample_name, sample_length, play_button, load_button))
        
        # Bottom bar
        with gr.Row(variant="compact"):
            save_button = gr.Button("Save Settings")
            unload_button = gr.Button("Unload All")
            exit_button = gr.Button("Exit Program")

        def update_soundcard_and_save(selected):
            update_soundcard(selected)
            save_settings()

        def update_volume_and_save(new_volume):
            update_volume(new_volume)
            save_settings()

        soundcard_select.change(fn=update_soundcard_and_save, inputs=soundcard_select, outputs=None)
        volume_slider.change(fn=update_volume_and_save, inputs=volume_slider, outputs=None)

        for i, (sample_name, sample_length, play_button, load_button) in enumerate(columns):
            load_button.change(fn=load_sample(samples, i, update_samples), inputs=load_button, outputs=[sample_name, sample_length])
            play_button.click(fn=lambda i=i: play_sample(samples, volume, i, "-load"), inputs=None, outputs=None)

        # Update this line to directly call save_settings
        save_button.click(fn=save_settings, inputs=None, outputs=None)
        
        def unload_all_samples():
            global play_objects, play_threads
            empty_samples = [''] * 8
            update_samples(empty_samples)
            # Stop all playing sounds and wait for threads to finish
            for column, play_obj in play_objects.items():
                if play_obj is not None:
                    play_obj.stop()
                if column in play_threads and play_threads[column] is not None:
                    play_threads[column].join()
            play_objects.clear()
            play_threads.clear()
            return [""] * 8 + [""] * 8  # Return empty values for both filename and length
        
        unload_button.click(fn=unload_all_samples, inputs=None, outputs=[c[0] for c in columns] + [c[1] for c in columns])
        exit_button.click(fn=lambda: os._exit(0), inputs=None, outputs=None)

    return iface