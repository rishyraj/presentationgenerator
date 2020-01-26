from __future__ import print_function
#import pickle
import os.path
import os
import io
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename



SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']
PRESENTATION_ID = '1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc'


# Instantiate google cloud speech client
client = speech.SpeechClient()


UPLOAD_FOLDER = './temp_storage/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():        # render the html to page
  print('in the index function')
  return render_template('page.html')
  # return "Hello World"

@app.route('/', methods=['POST'])   # 
def upload_file():
  creds = None
  if request.method == 'POST':
    try:
      f = request.files['file']
    except:
      f = request.form["rawtext"]
      print(f)
    if (isinstance(f,str)):
      textfile = open(UPLOAD_FOLDER + 'raw_text_file.txt', 'w');
      textfile.write(f);
      textfile.close()
      return redirect('/')
    elif (allowed_file(f.filename)):
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
        file = open(UPLOAD_FOLDER + f.filename.split('.')[0] + '.txt', 'w')
        for result in response.results:
          # print('Transcript: {}'.format(result.alternatives[0].transcript))
          file.write(result.alternatives[0].transcript + '\n')
        file.close()
        
      # if os.path.exists('token.pickle'):
      #   with open('token.pickle', 'rb') as token:
      #     creds = pickle.load(token)
      # if not creds or not creds.valid:
      #   if creds and creds.expired and creds.refresh_token:
      #     creds.refresh(Request())
      #   else:
      #     flow = InstalledAppFlow.from_client_secrets_file(
      #       'credentials.json', SCOPES
      #     )
      #     creds = flow.run_local_server(port=0)
      #   with open('token.pickle', 'wb') as token:
      #     pickle.dump(creds, token)
        
      #   service = build('slides', 'v1', credentials=creds)

      #   presentation = service.presentations().get(
      #     presentationId=PRESENTATION_ID
      #   ).set_execute()
      #   slides = presentation.get('slides')
      return redirect('/')
    else:
      return 'invalid file extension'

def allowed_file(filename): 
  return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')
