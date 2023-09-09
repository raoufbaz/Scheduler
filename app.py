from flask import Flask, json, render_template, request, jsonify, make_response
from helpers import data_scraper, combinations_generator, schedule_generator
import unicodedata
import base64

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
                           title=program_title,
                           program_id=program_id), 200


# responds to ajax request. makes combinations and returns success or error
@app.route('/agendas', methods=['POST', 'GET'])
def get_combinations():
    courses = json.loads(request.args.get('courses'))
    semester_raw = json.loads(request.args.get('semester'))

    # convert semester to variables to achieve 'A24' format
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


# receives combinations and renders schedules page
@app.route('/schedules', methods=['POST'])
def display_schedules():
    combinations = request.form.get('combinations')
    print(combinations)
    return render_template('schedules_page.html'), 200


# placeholder for schedules_page
@app.route('/cours')
def placeholder_schedules():
    return render_template('schedules_page.html'), 200


@app.route('/generate_schedule_image')
def generate_schedule_image():
    courses = [
        # classes temporaire
        ("lun", "GTI525 (C)", "18:00", "21:30", "red"),
        ("mer", "GTI525 (TP)", "18:00", "20:00", "red"),

        ("mar", "GTI611 (TP)", "8:30", "11:30", "purple"),
        ("ven", "GTI611 (C)", "8:30", "12:00", "purple"),

        ("mer", "LOG635 (TP)", "8:30", "10:30", "blue"),
        ("mer", "LOG635 (TP)", "10:30", "12:30", "blue"),
        ("ven", "LOG635 (C)", "13:30", "17:00", "blue"),

        # Work
        ("lun", "Desjardins", "8:00", "12:00", "green"),
        ("lun", "Desjardins", "13:00", "17:00", "green"),
        ("jeu", "Desjardins", "8:00", "12:00", "green"),
        ("jeu", "Desjardins", "13:00", "17:00", "green"),
        ("mer", "Desjardins", "13:00", "17:00", "green"),
    ]
    # Generate the schedule image
    schedule_image_base64 = schedule_generator.generate_for_frontend(courses)

    # Return the image as a response with the appropriate content type
    response = make_response(base64.b64decode(schedule_image_base64))
    response.headers['Content-Type'] = 'image/png'
    return response
