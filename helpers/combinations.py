import itertools
from models.agenda import Agenda


def generate_agendas(courses):

    agendas = []
    for r in range(1, len(courses) + 1):
        for combination in itertools.combinations(courses, r):
            if is_valid_combination(combination):
                agenda = Agenda()
                for course in combination:
                    agenda.add_course(course)
                agendas.append(agenda)

    return agendas


# takes 2 time intervals and check if they overlap
# return True if they do else False
def validate_overlapping_hours(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1


def is_valid_combination(combination):
    for i, course1 in enumerate(combination):
        for course2 in combination[i+1:]:
            if course1.titre == course2.titre:
                return False
            for h1 in course1.horaires:
                for h2 in course2.horaires:
                    if h1['jour'] == h2['jour'] and validate_overlapping_hours(
                        h1['heure_dedut'], h1['heure_fin'], h2['heure_debut'],
                            h2["heure_fin"]):
                        return False
    return True


# def get_combinations(courses_list):
# print(data_scraper.scrape_class_info("INF5151", "2023", "3", "7416"))
