from bs4 import BeautifulSoup
# from datetime import date, datetime
import requests
import json
import os
import unicodedata
from models.course import Course
SEMESTER_ID = {
    "not_found": "0",
    "winter": "1",
    "summer": "2",
    "fall": "3",
}
# DATE_TIME_FORMAT = "%m-%d-%Y"
# URL_LINK_EXAMPLE =
# f"https://etudier.uqam.ca/wshoraire/cours/INF1120/20233/7316"


# Scrapes all available info on a class
# Parameters are needed to build the URL
# Returns a list of groups of the same course
def scrape_class_info(course_id: str, year: str, semester: str, program):
    try:
        URL = f"""https://etudier.uqam.ca/wshoraire/cours/{course_id}/{year}{semester}/{program}"""
        html_doc = requests.get(URL).text
        soup = BeautifulSoup(html_doc, "html.parser")
        groups = soup.find_all("div", {"class": "groupe"})
        liste_cours = []
        for item in groups:
            cours = Course()
            cours.titre = course_id
            cours.semestre = year + semester
            cours.programme_id = program
            cours.groupe = get_group(item)
            cours.nb_places = get_places(item)
            cours.enseignants = get_professors(item)
            cours.remarques = get_remarques(item)
            cours.modalite = get_modalite(item)
            cours.horaires = get_horaire(item)

            liste_cours.append(cours)
        return liste_cours
    except Exception as e:
        print("Exception in scraping course : " + str(e))
        return []


def get_group(item: any):
    group = item.find(class_="no_groupe")
    if group is not None:
        return (group.text.strip())


def get_places(item: any):
    places = item.find(class_="places")
    if places is not None:
        return (places.text.strip())


def get_professors(item: any):
    tables = item.find_all("table", {"class": "alignement"})
    if len(tables) > 0:
        for tab in tables:
            # finds the right table
            flag = tab.find_all(lambda tag: tag.name == "h3"
                                and "Enseignant" in tag.text)
            if len(flag) > 0:
                profs = []
                list = tab.find_all("li")
                if len(list) > 0:
                    for li in list:
                        profs.append(li.text)
                    return profs
            else:
                continue


def get_remarques(item: any):
    tables = item.find_all("table", {"class": "alignement"})
    if len(tables) > 0:
        for tab in tables:
            # finds the right table
            flag = tab.find_all(lambda tag: tag.name == "h3"
                                and "Remarque" in tag.text)
            if len(flag) > 0:
                remarques = []
                list = tab.find_all("li")
                if len(list) > 0:
                    for li in list:
                        remarques.append(li.text)
                    return remarques
            else:
                continue


def get_modalite(item: any):
    modalite = item.find(class_="avertissement")
    if modalite is not None:
        return (modalite.text.strip())


def get_horaire(item: any):
    tables = item.find_all("table")
    for tab in tables:
        # finds the right table
        flag_table = tab.find_all(lambda tag: tag.name == "th"
                                  and "Jour" in tag.text)
        if len(flag_table) > 0:
            horaires = []
            # finds rows with data
            rows = tab.find_all(lambda tag: tag.name == "tr"
                                and "Du" in tag.text)
            if len(rows) > 0:
                for row in rows:
                    data = row.select("tr td")
                    start_time, end_time = extract_time_range(data[2]
                        .get_text(strip=True).replace('\xa0', ' '))
                    json_obj = {
                        "jour": data[0].get_text(strip=True),
                        "date": data[1].get_text(strip=True),
                        "heure": data[2].get_text(strip=True)
                        .replace('\xa0', ' '),
                        "lieu": data[3].get_text(strip=True),
                        "type": data[4].get_text(strip=True),
                        "heure_debut": start_time,
                        "heure_fin": end_time
                        }
                    horaires.append(json_obj)
                return horaires


def extract_time_range(time_str):
    time_str = time_str.lower().replace('de ', '').replace('h', '')
    start_time, end_time = time_str.split(' à ')
    start_time = int(start_time)
    end_time = int(end_time)
    return start_time, end_time


def get_all_courses_data(program_id: str):
    # call to other functions
    return 0

# print(scrape_class_info("INF5190","2023",SEMESTER_ID["fall"],"7316"))


# Scrapes course title and program id
# Needs a course name to retrieve data
# Returns a json object with the title and program id
def get_course_title_and_program_id(course_name: str):
    URL = f"https://etudier.uqam.ca/cours?sigle={course_name}"
    html_doc = requests.get(URL).text
    soup = BeautifulSoup(html_doc, "html.parser")
    course_title_raw = soup.find("h1", {"class": "title"})
    title = course_title_raw.text
    trimmed = title.strip()
    split_strings = trimmed.split(" - ")
    title = split_strings[1]
    course_id_raw = soup.find("div", {"class": "related-programs bloc"})
    a_tag = course_id_raw.find("a")
    href = a_tag.get('href')
    id_split_strings = href.split("=")
    id = id_split_strings[1]
    if not title or not id:
        return ""
    json_obj = {
            "program_id": id,
            "title": title
            }
    return json.dumps(json_obj)


# Scrapes all courses related to a certain program
# Needs a program id to retrieve data
# Returns a json object list of the courses
def get_program_courses(program_id: str):
    # Check if courses are already cached
    cached_courses = load_courses_from_cache(program_id)
    if cached_courses:
        print("--- Loading Courses From CACHE ---")
        return json.dumps(load_courses_from_cache(program_id))

    URL = f"https://etudier.uqam.ca/programme?code={program_id}#bloc_cours"
    html_doc = requests.get(URL).text
    soup = BeautifulSoup(html_doc, "html.parser")
    courses_list_raw = soup.find_all("div", {"class": "bloc_cours"})
    courses_list = []
    for item in courses_list_raw:
        tag = item.find("a")
        trimmed = tag.text.strip()
        split_strings = trimmed.split(" - ")
        id, title = split_strings
        json_obj = {
                "id": id,
                "title": title
                }
        courses_list.append(json_obj)

    print("--- Saving Courses To CACHE ---")
    save_courses_to_cache(program_id, courses_list)

    return json.dumps(load_courses_from_cache(program_id))


# Scrapes all programs from the website
# saves a copy on cache file,
# then loads the file every time the function is called
# Returns a json object list of the programs
def get_programs():
    cached_programs = load_programs_from_cache()
    if cached_programs:
        print("--- Loading Programs From CACHE ---")
        return json.dumps(cached_programs)
    # type de programmes:
    program_bac_list = []  # Baccalauréat
    program_cert_list = []  # Certificat
    program_conc_list = []  # Concentration
    program_dess_list = []  # DESS
    program_doct_list = []  # Doctorat
    program_mait_list = []  # Maîtrise
    program_major_list = []  # Majeure
    program_mba_list = []  # MBA
    program_micro_list = []  # Microprogramme
    program_minor_list = []  # Mineure
    program_court_list = []  # Programme court

    URL = "https://etudier.uqam.ca/programmes"
    html_doc = requests.get(URL).text
    soup = BeautifulSoup(html_doc, "html.parser")
    programs_table = soup.find('table', {'id': 'tableProgrammes'})
    rows = programs_table.find_all('tr')

    programs_dict = {
        "baccalaureat": program_bac_list,
        "certificat": program_cert_list,
        "concentration": program_conc_list,
        "dess": program_dess_list,
        "doctorat": program_doct_list,
        "maitrise": program_mait_list,
        "majeure": program_major_list,
        "mba": program_mba_list,
        "microprogramme": program_micro_list,
        "mineure": program_minor_list,
        "programme court": program_court_list
    }

    for row in rows:
        tag_td = row.find("a")
        if (tag_td):
            title = tag_td.text.strip()

        code_td = row.find('td', {'class': 'code'})
        if (code_td):
            code = code_td.text.strip()

        types_td = row.find('td', {'class': 'types'})
        if (types_td):
            types = (unicodedata.normalize('NFKD', types_td.text.strip())
                     .encode('ASCII', 'ignore').decode('utf-8')).lower()

        if (tag_td and code_td and types_td):
            program = {'code': code, 'title': title}
            append_to_list(types, program, programs_dict)

    print("--- Saving Programs To CACHE ---")
    save_programs_to_cache(programs_dict)
    return json.dumps(load_programs_from_cache())


# Appends the ptogram to the corresponding array in the dictionary
def append_to_list(types, program, programs_dict):
    if types in programs_dict:
        programs_dict[types].append(program)


# Saves the programs list in a cache file
# requires the list of programs as parameter
def save_programs_to_cache(program_lists):
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)

    with open("cache/cache_programs.json", "w") as file:
        json.dump(program_lists, file, indent=4)


# Saves the courses list in a cache file
# requires the list of courses and the programID as parameter
def save_courses_to_cache(program_id: str, courses: list):
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)

    cache_file = f"cache/cache_{program_id}_courses.json"
    with open(cache_file, "w") as file:
        json.dump(courses, file, indent=4)


# Loads the programs list from the cache file
# returns the json file if exists or None
def load_programs_from_cache():
    filename = "cache/cache_programs.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    return None


# Loads the courses list from the cache file
# returns the json file if exists or None
def load_courses_from_cache(program_id):
    filename = f"cache/cache_{program_id}_courses.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    return None


# get_program_courses("7416") # decomment to save a cache file of the course
# get_programs() # decomment to save a cache file of list of programs
