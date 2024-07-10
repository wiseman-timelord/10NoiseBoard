import gradio as gr
import os
from pydub import AudioSegment
from pydub.playback import play
import yaml

def load_sample(column):
    filepath = gr.File.update()
    samples[column] = filepath
    return os.path.basename(filepath)

def play_sample(column):
    if samples[column]:
        audio = AudioSegment.from_wav(samples[column])
        play(audio)

def save_settings():
    with open('.\\data\\settings_general.yaml', 'w') as f:
        yaml.safe_dump({'samples': samples, 'selected_soundcard': selected_soundcard}, f)

def unload_samples():
    global samples
    samples = [''] * 10
    return [''] * 10

def create_interface(samples, soundcards, selected_soundcard):
    with gr.Blocks() as iface:
        with gr.Row():
            soundcard_select = gr.Dropdown(label="Output Soundcard", choices=soundcards, value=selected_soundcard)
        
        columns = []
        for i in range(10):
            with gr.Column():
                sample_name = gr.Textbox(label="Filename", value=os.path.basename(samples[i]))
                sample_length = gr.Textbox(label="Length", value="")
                play_button = gr.Button(f"Play Sample {i+1}")
                load_button = gr.Button(f"Load Sample {i+1}")
                
                columns.append((sample_name, sample_length, play_button, load_button))

        with gr.Row():
            save_button = gr.Button("Save Settings")
            unload_button = gr.Button("Unload Samples")
            exit_button = gr.Button("Exit Program")

        def update_soundcard(selected):
            global selected_soundcard
            selected_soundcard = selected

        soundcard_select.change(fn=update_soundcard, inputs=soundcard_select, outputs=None)

        for i, (sample_name, sample_length, play_button, load_button) in enumerate(columns):
            load_button.click(fn=load_sample, inputs=i, outputs=sample_name)
            play_button.click(fn=play_sample, inputs=i, outputs=None)

        save_button.click(fn=save_settings, inputs=None, outputs=None)
        unload_button.click(fn=unload_samples, inputs=None, outputs=[c[0] for c in columns])
        exit_button.click(fn=lambda: os._exit(0), inputs=None, outputs=None)

    return iface
