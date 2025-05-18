from flask import Flask, render_template, request, send_file
from openai import OpenAI
import openai
from pydub import AudioSegment
import numpy as np
import wave
import os

audio_data = None
sample_rate = 44100

os.environ['OPENAI_API_KEY'] = ''
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcriber', methods=['POST', 'GET'])
def transcriber():

    if 'file' not in request.files:
        return render_template('transcriber.html', message='Upload file')

    file = request.files['file']
    if file.filename == '':
        return render_template('transcriber.html', message='No file found')

    # Save the uploaded file to a desired location
    file.save('uploads/' + file.filename)
    convert_audio_to_wav('uploads/' + file.filename, 'uploads/data.wav')
    audio_file_path = 'uploads/data.wav'

    # Process the audio file
    with open(audio_file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    response = openai.Completion.create( engine = 'gpt-3.5-turbo-instruct',
                                     prompt = message_summary(transcript.text),
                                     temperature = 0.5,
                                     max_tokens = 600)
    
    return render_template('transcriber.html', message=transcript.text, filename=file.filename)

def convert_audio_to_wav(input_audio_file, output_wav_file):
     # Load the audio file using pydub
      audio = AudioSegment.from_file(input_audio_file)      
     # Convert the audio to WAV format
      audio.export(output_wav_file, format="wav")

# Generate message summary
def message_summary(message):
    prompt = f"Generate the summary of the {message}"
    return prompt
response = openai.Completion.create( engine = 'gpt-3.5-turbo-instruct',
                                     prompt = message_summary(message),
                                     temperature = 0.5,
                                     max_tokens = 600)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
