from flask import Flask, json, render_template, request, jsonify
from helpers import data_scraper
import unicodedata

app = Flask(__name__)
liste_programmes = []


# Landing page
@app.route('/')
def get_page_index():
    global liste_programmes
    if not liste_programmes:
        liste_programmes = data_scraper.get_programs()

    return render_template('index.html'), 200


# Autocompletion for landing page's search bar
@app.route('/autocomplete')
def autocomplete():
    input_text = (unicodedata.normalize('NFKD', request.args.get('input_text'))
                  .encode('ASCII', 'ignore').decode('utf-8')).lower()
    niveau = (unicodedata.normalize('NFKD', request.args.get('niveau')).encode(
        'ASCII', 'ignore').decode('utf-8')).lower()
    if len(input_text) < 3:
        return jsonify([])

    programs_list = json.loads(liste_programmes)
    suggestions = [
        {
            'title': program['title'],
            'code': program['code']
        }
        for program in programs_list[niveau]
        if input_text in (unicodedata.normalize('NFKD', program['title'])
                          .encode('ASCII', 'ignore').decode('utf-8')).lower()
    ][:5]  # Limit the suggestions to 5 items

    return jsonify(suggestions)


# Search by program ID, redirects to list of courses, else back
# to page with error message
@app.route('/programme', methods=['GET'])
def get_programme():
    program_id = request.args.get('program_id')
    program_title = request.args.get('program_title')

    # Empty parameters validation
    if not program_id or not program_title:
        error = "Le champs ne peut pas etre vide."
        return render_template("index.html", error=error), 400
    list = data_scraper.get_program_courses(program_id)
    # empty list validation
    if list == "[]":
        error = "Entrez un nom de programme valide."
        return render_template("index.html", error=error), 400
    list = json.loads(list)
    return render_template('choix_cours.html', courses=list,
                           title=program_title), 200


# makes combinations and redirect to Schedules page
@app.route('/agendas', methods=['POST', 'GET'])
def get_combinations():
    courses = request.args.get('courses')
    print(courses)  # contains ["INF1070","INF1120"] json
    return jsonify("reussi ")
    # cours1 = data_scraper.scrape_class_info("INF5151", "2023", "3", "7416")
    # cours2 = data_scraper.scrape_class_info("INF2120", "2023", "3", "7416")
    # cours3 = data_scraper.scrape_class_info("INF2050", "2023", "3", "7416")
    # print(cours1[0].titre)
    # print(cours1[0].horaires["type"])
    # agendas = combinations_generator.generate_agendas(cours1)
    # return render_template('index.html', agendas=agendas), 200
