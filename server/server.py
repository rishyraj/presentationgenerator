import os
import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# Instantiate google cloud speech client
client = speech.SpeechClient()


UPLOAD_FOLDER = './temp_storage/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():        # render the html to page
  print('in the index function')
  return render_template('index.html')
  # return "Hello World"

@app.route('/', methods=['POST'])   # 
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    if (allowed_file(f.filename)):
      extension = f.filename.split('.')[-1]
      if (extension == 'txt'):
        f.save(UPLOAD_FOLDER + f.filename)
      elif (extension == 'pdf'):
        print("hi")
      elif (extension == 'mp3'):
        f.save(UPLOAD_FOLDER + f.filename)
        audio_name = UPLOAD_FOLDER + f.filename
        # Load audio to memory
        with io.open(audio_name, 'rb') as audio_file:
          content = audio_file.read()
          audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
          encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
          sample_rate_hertz=16000,
          language_code='en-US',
          enable_automatic_punctuation=True
        )

        # Detects speech in the audio file
        response = client.recognize(config, audio)
        f = open(UPLOAD_FOLDER + f.filename.split('.')[0] + '.txt', 'w')
        for result in response.results:
          # print('Transcript: {}'.format(result.alternatives[0].transcript))
          f.write(result.alternatives[0].transcript + '\n')
        f.close()
        
      return redirect('/')
    else:
      return 'invalid file extension'

def allowed_file(filename): 
  return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')
