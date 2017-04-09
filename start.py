from tkinter import Image

from flask import Flask, render_template, request, url_for, redirect, current_app
import sqlite3
from flask import g
import os.path
from os import listdir, getcwd

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        return redirect(url_for('question'))

    return render_template('question.html')

@app.route('/sample', methods=['GET', 'POST'])
def sample():
    if request.method == 'POST':
        return redirect(url_for('sample'))
    return render_template('sample.html')

@app.route('/outfit', methods=['GET', 'POST'])
def outfit():
    if request.method == 'POST':
        return redirect(url_for('outfit'))
    return render_template('outfit.html')

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)