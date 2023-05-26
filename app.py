from flask import Flask, render_template
# from helpers import data_scraper

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html'), 200


@app.route('/page2')
def hello1():
    return render_template('layout.html'), 200
