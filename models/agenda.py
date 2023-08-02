# Agenda objects contain a list of courses from combination_generator
class Agenda:
    def __init__(self, combinaison):
        self.courses = combinaison
        self.agenda = self.generate_schedule(self.courses)

    SEMESTER_ID = {
        "1": "H",
        "2": "E",
        "3": "A",
    }

    # takes a list of course objects and generates json schedule
    def generate_schedule(self, courses: list):
        schedules = []
        for course in courses:
            semestre = self.SEMESTER_ID[course.semestre[4]] + course.semestre[
                2:4]
            schedule = {
                'titre': course.titre,
                'groupe': course.groupe,
                'semestre': semestre,
                'modalite': course.modalite,
                'nb_places': course.nb_places,
                'enseignants': course.enseignants,
                'horaires': course.horaires
            }
            schedules.append(schedule)
        return schedules
