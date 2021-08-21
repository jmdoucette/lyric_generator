from flask import Flask, request, render_template, redirect
from model_class import LyricGenerationModel
import config

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    return redirect('/display')
  else:
    return render_template('index.html')
  
@app.route('/display', methods=['GET', 'POST'])
def display():
  if request.method == 'POST':
    return redirect('/display')
  else:
    model = LyricGenerationModel()
    model.load(config.current_model)
    words_generated = model.generate_text()    
    
    #prettifying
    lyrics = ' '.join(words_generated)
    lyrics = lyrics.replace('newline', '<br>')
    lyrics = lyrics.replace('songstart', '')
    lyrics = lyrics.replace('songend', '')
    lyrics = lyrics.replace('[chorus]', '<br> [chorus]')
    lyrics = lyrics.replace('[verse]', '<br> [verse]')
    lyrics = lyrics.replace('[bridge]', '<br> [bridge]')

    return render_template('display.html', lyrics=lyrics)
  
