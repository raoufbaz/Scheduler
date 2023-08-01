# import itertools
# from models.agenda import Agenda

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
        return combinations


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
