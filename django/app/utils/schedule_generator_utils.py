from ..models import Schedule, Course, Professor
from datetime import datetime
import networkx as nx


from collections import defaultdict
# Función auxiliar para determinar si dos horarios se solapan


def schedules_overlap(schedules_set_1, schedules_set_2) -> bool:
    for schedule_1 in schedules_set_1:
        for schedule_2 in schedules_set_2:
            if schedule_1['day'] == schedule_2['day']:
                start_1 = datetime.combine(
                    datetime.min, schedule_1['start_time'])
                end_1 = datetime.combine(datetime.min, schedule_1['end_time'])
                start_2 = datetime.combine(
                    datetime.min, schedule_2['start_time'])
                end_2 = datetime.combine(datetime.min, schedule_2['end_time'])

                if (start_1 < end_2) and (end_1 > start_2):
                    return True  # Hay overlap
    return False  # No hay overlap


# Función auxiliar para obtener los días esperados de un curso


def get_expected_days_for_course(course_id: int) -> set:
    unique_schedule_days = Schedule.objects.filter(
        course__id=course_id
    ).values_list('day', flat=True).distinct()
    return set(unique_schedule_days)

# Función para agrupar horarios por curso y profesor


def get_grouped_schedules(courses):
    grouped_schedules = defaultdict(lambda: defaultdict(list))
    for course_name in courses:
        course_schedules = Schedule.objects.filter(
            course__name=course_name
        ).values(
            'id', 'course_id', 'professor_id', 'day', 'start_time', 'end_time', 'room_id',
            'start_date', 'end_date', 'modality'
        )
        for schedule in course_schedules:
            grouped_schedules[schedule['course_id']
                              ][schedule['professor_id']].append(schedule)
    return grouped_schedules


def is_schedule_consistent(clique, graph):
    '''Check that the schedules in a clique are consistent.
    A schedule is consistent if it has at least one session for each day
    of the week, but no more than one session for each day of the week.
    '''
    # Obtener los días esperados para cada curso
    expected_days = {}
    for node_id in clique:
        course_id = graph.nodes[node_id]['schedules'][0]['course_id']
        expected_days[course_id] = get_expected_days_for_course(course_id)
    # Obtener los días de cada horario
    schedule_days = {}
    for node_id in clique:
        course_id = graph.nodes[node_id]['schedules'][0]['course_id']
        schedule_days[course_id] = set(
            [schedule['day'] for schedule in graph.nodes[node_id]['schedules']])
    # Verificar que los horarios sean consistentes
    for course_id, days in expected_days.items():
        if days != schedule_days[course_id]:
            return False
        else:
            return True


def create_compatible_schedules(courses: list[str], minimum: int = 3, teachers_names: list[str] = None) -> list[dict]:
    grouped_schedules = get_grouped_schedules(courses)

    # Inicializar el grafo
    graph = nx.Graph()
    for course_id, professors_schedules in grouped_schedules.items():
        for professor_id, schedules in professors_schedules.items():
            node_id = (course_id, professor_id)
            graph.add_node(node_id, schedules=schedules)

    # Agregar aristas entre nodos con horarios no superpuestos
    for node_id_1, data_1 in graph.nodes(data=True):
        for node_id_2, data_2 in graph.nodes(data=True):
            if node_id_1 != node_id_2 and not schedules_overlap(data_1['schedules'], data_2['schedules']):
                graph.add_edge(node_id_1, node_id_2)

    # Encontrar cliques de horarios compatibles
    cliques = list(nx.find_cliques(graph))

    # Filtrar cliques por consistencia y número mínimo de materias
    final_cliques = []
    for clique in cliques:
        if is_schedule_consistent(clique, graph):
            final_cliques.append(clique)

    # Transformar la estructura de datos
    return transform_schedule_data(final_cliques, graph)


def remove_duplicates(schedule_list):
    unique_schedules = []
    seen = set()

    for schedule in schedule_list:
        identifier = (schedule['day'], schedule['start_time'],
                      schedule['end_time'], schedule['room_id'])
        if identifier not in seen:
            seen.add(identifier)
            unique_schedules.append(schedule)

    return unique_schedules


def transform_schedule_data(cliques, graph):
    final_schedules = []

    for clique in cliques:
        course_professor_map = {}
        for node_id in clique:
            # Asegurándonos de que 'schedules' sea una lista de diccionarios
            schedules = graph.nodes[node_id]['schedules']
            if not isinstance(schedules, list) or not all(isinstance(schedule, dict) for schedule in schedules):
                raise TypeError(
                    "Se esperaba una lista de diccionarios para 'schedules'")

            for schedule in schedules:
                key = (schedule['course_id'], schedule['professor_id'])
                if key not in course_professor_map:
                    course_professor_map[key] = {
                        "course_id": schedule['course_id'],
                        "professor_id": schedule['professor_id'],
                        "start_date": schedule['start_date'],
                        "end_date": schedule['end_date'],
                        "modality": schedule['modality'],
                        "schedule": []
                    }
                session_info = {
                    "day": schedule['day'],
                    "start_time": schedule['start_time'],
                    "end_time": schedule['end_time'],
                    "room_id": schedule['room_id']
                }
                if session_info not in course_professor_map[key]['schedule'] and session_info['day'] not in [session['day'] for session in course_professor_map[key]['schedule']]:
                    course_professor_map[key]['schedule'].append(session_info)

        final_schedules.append(
            [value for key, value in course_professor_map.items()])

    return final_schedules
