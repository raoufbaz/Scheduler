from flask import Flask, json, render_template, request
from helpers import data_scraper

app = Flask(__name__)


@app.route('/')
def get_page_index():
    return render_template('index.html'), 200


@app.route('/cours')
def get_page_cours():
    return render_template('choix_cours_template.html'), 200


#  Recherche par programme, redirige vers liste des cours
@app.route('/programme', methods=['GET'])
def get_programme():
    semester = request.args.get('session')  # get inputs from form
    id = request.args.get('id')
    title = request.args.get('titre')
    title = "Genie logiciel test"
    # if not session or not query:
    # return jsonify({"error": "Donnée manquante, 2 parametres sont attendu"
    #                     }), 400
    # if fonction de validation des champs
    list = data_scraper.get_program_courses(id)
    list = json.loads(list)
    return render_template('choix_cours.html', courses=list, title=title,
                           semester=semester), 200
