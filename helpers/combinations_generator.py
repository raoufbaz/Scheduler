from models.agenda import Agenda


# This function takes a list of courses(each can have multiple groups)
# Generates combinations depending on groups and overlapping hours.
# a combination must contain at least 1 group of each course to be valid
# Parameter: courses (list of lists)
# Returns: [] or list of : lists of courses
def generate_combinations(courses: list):
    combinations = []
    if courses is not None and len(courses) > 0:
        i = 1  # current position
        for course in courses:
            # if first element : append
            if len(combinations) == 0:
                for group in course:
                    combinations.append([group])
            else:
                if len(courses) == 1:
                    return combinations
                for group in course:
                    validate_overlap_and_append(group, combinations, i)
            i += 1
        combinations = [lst for lst in combinations if (
            len(lst) == len(courses)
        )]
        # convert lists to Agenda objects
        result = []
        for combinaison in combinations:
            agenda = Agenda(combinaison)
            result.append(agenda)
        return clean_data(result)


# Checks if a combination is valid before appending it
def validate_overlap_and_append(group, combinations: list, index: int):
    filtered_list = [lst for lst in combinations if len(lst) == index-1]
    for combination in filtered_list:
        if not is_overlapping(group, combination):
            combinations.append(combination + [group])


# Compares a course's group with a combination
def is_overlapping(group, combinations):
    for comb in combinations:
        for h1 in group.horaires:
            for h2 in comb.horaires:
                if (
                    h1['jour'] == h2['jour'] and
                    h1['heure_debut'] <= h2['heure_fin'] and
                    h1['heure_fin'] >= h2['heure_debut']
                ):
                    return True
    return False


day_mapping = {
    'Lundi': 'lun',
    'Mardi': 'mar',
    'Mercredi': 'mer',
    'Jeudi': 'jeu',
    'Vendredi': 'ven',
    'Samedi': 'sam',
    'Dimanche': 'dim'
}


def clean_data(combinations):
    jsonlist = []
    for comb in combinations:
        jsonlist.append(comb.agenda)

    classes = []
    for result in jsonlist:
        comb = []
        for course in result:
            titre = course['titre']
            # groupe = course['groupe']
            horaires = course['horaires']
            typeAdded = []
            for horaire in horaires:
                typ = horaire['type']
                jour = horaire['jour']
                heure_deb = horaire['heure_debut']
                format_heure_debut = f"{heure_deb // 100}:{heure_deb % 100:02}"
                heure_fin = horaire['heure_fin']
                format_heure_fin = f"{heure_fin // 100}:{heure_fin % 100:02}"
                if not typeAdded.__contains__(typ):
                    comb.append((day_mapping.get(jour), titre,
                                 format_heure_debut, format_heure_fin))
                    typeAdded.append(typ)
        classes.append(comb)
    return classes


def filter_unavailability(criteria, combinations: list):

    for comb in combinations:
        if is_overlapping_filter(criteria, combinations):
            combinations.remove(comb)
    return combinations
    # adapt object pour reutiliser is_overlapping


# Compares a list of unavailabilities with a list of combination
def is_overlapping_filter(indisponibilites, combinations):
    for comb in combinations:
        for h1 in indisponibilites:
            for h2 in comb:
                if (
                    h1['day'] == h2[0] and
                    h1['start_time'] <= h2[3] and
                    h1['end_time'] >= h2[2]
                ):
                    return True
    return False
