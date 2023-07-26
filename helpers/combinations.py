import itertools
from models.agenda import Agenda


def generate_agendas(courses):

    agendas = []
    for r in range(1, len(courses) + 1):
        for combination in itertools.combinations(courses, r):
            if is_valid_combination(combination[0]):
                agenda = Agenda()
                for course in combination:
                    agenda.add_course(course)
                agendas.append(agenda)

    return agendas


# takes 2 time intervals and check if they overlap
# return True if they do else False
# def validate_overlapping_hours(start1, end1, start2, end2):
#    return start1 <= end2 and start2 <= end1


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


# def generate_combinations(courses_list, current_combination=[], index=0):
#     if index == len(courses_list):
#         return [tuple(current_combination)]

#     current_courses = courses_list[index]
#     combinations = []
#     for course in current_courses:
#         new_combination = current_combination + [course]
#         combinations.extend(generate_combinations(courses_list,
# new_combination, index + 1))

#     return combinations


def validate_overlapping_hours(horaire1, horaire2):
    for h1 in horaire1:
        for h2 in horaire2:
            if (
                h1['jour'] == h2['jour'] and
                h1['heure_debut'] <= h2['heure_fin'] and
                h1['heure_fin'] >= h2['heure_debut']
            ):
                return True
    return False


def generate_combinations(courses_list, current_combination=[], index=0):
    if index == len(courses_list):
        return [tuple(current_combination)]

    current_courses = courses_list[index]
    combinations = []
    for course in current_courses:
        new_combination = current_combination + [course]
        if not any(validate_overlapping_hours(course.horaires, c.horaires) for
                   c in new_combination[:-1]):
            combinations.extend(generate_combinations(
                courses_list, new_combination, index + 1))

    return combinations


# def get_combinations(courses_list):
# print(data_scraper.scrape_class_info("INF5151", "2023", "3", "7416"))


# def test_combination():

#     agendas = combinations.generate_agendas(cours_list)
#     for agenda in agendas:
#         print("AGENDA : ")
#         print("===========")
#         print(agenda.courses)
#         for course in agenda.courses:
#             print(course.titre)
#             print(course.groupe)
#             for horaire in course.horaires:
#                 print(horaire["type"])
#                 print("start_time :" + str(horaire["heure_debut"]))
#                 print("end_time :" + str(horaire["heure_fin"]))

# cours1 = data_scraper.scrape_class_info("INF3135", "2023", "3", "7416")
# cours2 = data_scraper.scrape_class_info("INF5151", "2023", "3", "7416")
# cours3 = data_scraper.scrape_class_info("INF2171", "2023", "3", "7416")
# cours_list = []
# cours_list.append(cours1)
# cours_list.append(cours2)
# cours_list.append(cours3)
# combinaisons = generate_combinations(cours_list)
# print(len(combinaisons))
# print(len(cours_list))
# test_combination()
