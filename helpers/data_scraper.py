from bs4 import BeautifulSoup
# from datetime import date, datetime
import requests
import json

SEMESTER_ID = {
    "not_found": "0",
    "winter": "1",
    "summer": "2",
    "fall": "3",
}
# DATE_TIME_FORMAT = "%m-%d-%Y"
# URL_LINK_EXAMPLE =
# f"https://etudier.uqam.ca/wshoraire/cours/INF1120/20233/7316"


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
                    json_obj = {
                        "jour": data[0].get_text(strip=True),
                        "date": data[1].get_text(strip=True),
                        "heure": data[2].get_text(strip=True)
                        .replace('\xa0', ' '),
                        "lieu": data[3].get_text(strip=True),
                        "type": data[4].get_text(strip=True)
                        }
                    horaires.append(json_obj)
                return horaires


# Scrapes all available info on a class
# Parameters are needed to build the URL
# Returns JSON Object with result or empty
def scrape_class_info(course: str, current_year: str, semester: str, program):
    try:
        URL = f"""https://etudier.uqam.ca/wshoraire/cours/{course}/
        {current_year}{semester}/{program}"""
        html_doc = requests.get(URL).text
        soup = BeautifulSoup(html_doc, "html.parser")
        groups = soup.find_all("div", {"class": "groupe"})
        infos_cours = []
        for item in groups:
            json_obj = {
                "groupe": get_group(item),
                "nb_places": get_places(item),
                "enseignants": get_professors(item),
                "remarques": get_remarques(item),
                "modalite": get_modalite(item),
                "horaires": get_horaire(item)
                        }
            infos_cours.append(json_obj)
        return json.dumps(infos_cours)
    except AttributeError:
        return []


def get_all_courses_data(program_id: str):
    # call to other functions
    return 0

# print(scrape_class_info("INF5190","2023",SEMESTER_ID["fall"],"7316"))


# a utiliser dans la section selection par cours
def get_course_title_and_id(course_name: str):
    URL = f"https://etudier.uqam.ca/cours?sigle=INF1132"
    # get h1 class title.text
    # get div.class related-programs > ul > (list of li, for each decortiquer url de <a>.href:
    # <a href="/programme?code=6571">Baccalauréat en économique</a>)
    return 0


def get_program_courses(program_id: str):
    URL = f"https://etudier.uqam.ca/programme?code={program_id}#bloc_cours"
    html_doc = requests.get(URL).text
    soup = BeautifulSoup(html_doc, "html.parser")
    courses_list_raw = soup.find_all("div", {"class": "bloc_cours"})
    courses_list = []
    for item in courses_list_raw:
        tag = item.find("a")
        courses_list.append(tag.text)
        print(tag.text)
    return courses_list


# print(get_program_courses("7416"))
get_program_courses("7416")
