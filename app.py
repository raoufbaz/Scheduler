from flask import Flask, json, render_template, request, jsonify
from helpers import data_scraper, combinations_generator
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
    semesters = data_scraper.get_current_semesters(program_id)
    return render_template('choix_cours.html', courses=list,
                           title=program_title,
                           semesters=semesters,
                           program_id=program_id), 200


# makes combinations and redirect to Schedules page
@app.route('/agendas', methods=['POST', 'GET'])
def get_combinations():
    courses = json.loads(request.args.get('courses'))
    semester_raw = json.loads(request.args.get('semester'))

    # convert semester to variables
    season_map = {
        'A': 'fall',
        'E': 'summer',
        'H': 'winter'
    }
    semester = season_map[semester_raw[0]]
    year = "20" + semester_raw[1:]

    # scrape courses data and generate combinations
    courses = data_scraper.scrape_courses_from_list(courses, semester, year)
    combinations = combinations_generator.generate_combinations(courses)
    jsonlist = []
    for comb in combinations:
        jsonlist.append(comb.agenda)
    if len(jsonlist) == 0:
        return jsonify("no combination possible"), 400
    return jsonify(jsonlist)
