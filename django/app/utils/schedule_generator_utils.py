from ..models import Schedule, Course
from datetime import datetime
import networkx as nx


def create_compatible_schedules(courses: list[str], minimum: int = 3, teachers_names: list[str] = None) -> list[dict[str, str]]:
    """
    Create a list of compatible schedules.
    """
    schedules = []

    # Get the courses ids from the courses names
    courses = [course_id for course_id in Course.objects.filter(
        name__in=courses).values_list('id', flat=True)]

    print(courses)

    for course in courses:
        schedules_queryset = Schedule.objects.filter(
            course=course).values()
        schedules.extend(schedules_queryset)

# Initialize graph
    graph = nx.Graph()
    for i, schedule in enumerate(schedules):
        graph.add_node(i, schedule=schedule)

    # Add edges if schedules do not overlap
    for i in range(len(schedules)):
        for j in range(i+1, len(schedules)):
            if not schedules_overlap(schedules[i], schedules[j]):
                graph.add_edge(i, j)

    # Find cliques
    cliques = list(nx.find_cliques(graph))
    compatible_schedules = [
        [schedules[index] for index in clique] for clique in cliques if len(clique) >= minimum
    ]

    # Filter by teachers if needed
    if teachers_names:
        compatible_schedules = [
            schedule for schedule in compatible_schedules
            if any(teacher['id'] in teachers_names for teacher in schedule['teachers'])
        ]

    return compatible_schedules


def schedules_overlap(schedule_1, schedule_2):
    if schedule_1['day'] == schedule_2['day']:
        start_1 = schedule_1['start_time']
        end_1 = schedule_1['end_time']
        start_2 = schedule_2['start_time']
        end_2 = schedule_2['end_time']
        return max(start_1, start_2) < min(end_1, end_2)
    return False
