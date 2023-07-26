# from app import app
from helpers import data_scraper, combinations


def test_combination():
    cours1 = data_scraper.scrape_class_info("INF3135", "2023", "3", "7416")
    cours2 = data_scraper.scrape_class_info("INF5151", "2023", "3", "7416")
    cours_list = []
    cours_list.append(cours1)
    cours_list.append(cours2)
    agendas = combinations.generate_agendas(cours_list)
    for agenda in agendas:
        print("AGENDA : ")
        print("===========")
        print(agenda.courses)
        for course in agenda.courses:
            print(course.titre)
            print(course.groupe)
            for horaire in course.horaires:
                print(horaire["type"])
                print("start_time :" + str(horaire["heure_debut"]))
                print("end_time :" + str(horaire["heure_fin"]))
