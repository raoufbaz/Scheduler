from flask import Flask, render_template, request
from helpers import data_scraper

app = Flask(__name__)


@app.route('/')
def get_page_index():
    return render_template('index.html'), 200


@app.route('/cours')
def get_page_cours():
    return render_template('choix_cours_template.html'), 200


@app.route('/programme', methods=['GET'])
def get_programme():
    session = request.args.get('btnradio')  # get inputs from form
    query = request.args.get('query')
    # if not session or not query:
    # return jsonify({"error": "Donnée manquante, 2 parametres sont attendu"
    #                     }), 400
    list = data_scraper.get_program_courses(query)
    print(session)
    print(query)
    return render_template('index.html', courses=list), 200
