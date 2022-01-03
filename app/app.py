from flask import Flask, request, render_template, redirect

import os,sys
parentdir = os.path.dirname(__file__)[:-3]
sys.path.insert(0,parentdir)
import config
sys.path.pop(0)
sys.path.insert(0,parentdir + 'model')
from model_class import LyricGenerationModel
sys.path.pop(0)




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
        lyrics = model.generate_text()  
        return render_template('display.html', lyrics=lyrics)
  
