from ..models import Schedule, Course, Professor
from datetime import datetime
import networkx as nx


def create_compatible_schedules(courses: list[str], minimum: int = 3, teachers_names: list[str] = None) -> list[dict]:
    """
    Create a list of compatible schedules.
    """
    # Get the courses objects from the courses names
    courses_ids = list(Course.objects.filter(
        name__in=courses).values_list('id', flat=True))

    # Initialize graph
    graph = nx.Graph()
    for course_id in courses_ids:
        # Get all schedules for this course
        for schedule in Schedule.objects.filter(course_id=course_id).values():
            node_id = schedule['id']
            graph.add_node(node_id, schedule=schedule)
            # Check and add edges for non-overlapping schedules
            for other_node_id in graph.nodes:
                if other_node_id != node_id:
                    other_schedule = graph.nodes[other_node_id]['schedule']
                    if not schedules_overlap(schedule, other_schedule):
                        graph.add_edge(node_id, other_node_id)

    # Find cliques of compatible schedules
    cliques = list(nx.find_cliques(graph))
    compatible_schedules = [
        [graph.nodes[index]['schedule'] for index in clique] for clique in cliques if len(clique) >= minimum
    ]

    # Filter by teachers if needed
    if teachers_names:
        professor_ids = list(Professor.objects.filter(
            name__in=teachers_names).values_list('id', flat=True))
        compatible_schedules = [
            schedule for schedule in compatible_schedules
            if any(schedule_item['professor_id'] in professor_ids for schedule_item in schedule)
        ]

    return compatible_schedules


def schedules_overlap(schedule_1: dict, schedule_2: dict) -> bool:
    # Assumes that start_time and end_time are datetime.time objects
    if schedule_1['day'] == schedule_2['day']:
        start_1 = schedule_1['start_time']
        end_1 = schedule_1['end_time']
        start_2 = schedule_2['start_time']
        end_2 = schedule_2['end_time']
        return max(start_1, start_2) < min(end_1, end_2)
    return False
