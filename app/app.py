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
    print(words_generated)
    #removing leading, trailing and repeated newlines
    words_generated = [word for word in words_generated if word != 'songstart' and word != 'songend']
    first_non_newline = 0
    for i,word in enumerate(words_generated):
        if word != 'newline':
            first_non_newline = i
            break
    last_non_newline = len(words_generated)
    for i,word in reversed(list(enumerate(words_generated))):
        if word != 'newline':
            last_non_newline = i
            break
    words_generated = words_generated[first_non_newline:last_non_newline+1]
    words_generated = [words_generated[i] for i in range(len(words_generated)) if words_generated[i] != 'newline' or (i > 0 and words_generated[i-1] != 'newline')]
    print(words_generated)
 
    
    #prettifying
    lyrics = ' '.join(words_generated)
    lyrics = lyrics.replace('songstart', '')
    lyrics = lyrics.replace('songend', '')


    lyrics = lyrics.replace('newline', '<br>')
    lyrics = lyrics.replace('[chorus]', '<br> [chorus]')
    lyrics = lyrics.replace('[verse]', '<br> [verse]')
    lyrics = lyrics.replace('[bridge]', '<br> [bridge]')
    lyrics = lyrics.replace('[intro]', '<br> [intro]')
    lyrics = lyrics.replace('[instrumental]', '<br> [instrumental]')

    return render_template('display.html', lyrics=lyrics)
  
