#!/usr/bin/env python3

from flask import Flask, render_template 
import json, os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    with open('../files/helloshiyanlou.json', 'r') as file:
        shiyanlou_file = json.loads(file.read())

    with open('../files/helloworld.json', 'r') as file:
        helloworld_json = json.loads(file.read())

    files = (shiyanlou_file, helloworld_json)

    return render_template('index.html', files=files)

@app.route('/files/<filename>')
def file(filename):
    path = '../files/' + filename + '.json'
    if os.path.exists(path) == False:
        return render_template('404.html')
    with open(path, 'r') as file:
        file_content = json.loads(file.read())
    return render_template('file.html', file_content=file_content)

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html'), 404
