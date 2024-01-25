from ..models import Course, Professor, Room, Schedule
from django.db.utils import IntegrityError
from django.core.files import File
from datetime import datetime
import pandas as pd


def process_excel_data(file_obj: File):
    """
    Process and validate data from an Excel file.

    Args:
        file_obj (File): An Excel file object to process.

    Returns:
        DataFrame: A processed and validated pandas DataFrame.

    Raises:
        ValueError: If any validation checks fail.
    """

    # Read Excel file
    try:
        data = pd.read_excel(file_obj)
        print(data.columns)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

    # Dataset validation
    required_columns = [
        "Id del Curso",
        "Ciclo",
        "Sesión",
        "Materia",
        "Mat. Comb.",
        "Clases Comb.",
        "Capacidad\nInscripción\nCombinación",
        "No de catálogo",
        "Clase",
        "No de clase",
        "Capacidad Inscripción",
        "Total  inscripciones",
        "Total de inscripciones materia combinada",
        "Fecha inicial",
        "Fecha final",
        "Salón",
        "Capacidad del salón",
        "Hora inicio",
        "Hora fin",
        "Profesor",
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
        "Bloque optativo",
        "Idioma en que se imparte la materia ",
        "Modalidad de la clase"
    ]
    missing_columns = [
        col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Fill missing values
    # Idioma en que se imparte la materia: Español
    # Modalidad de la clase: Presencial; ENLINEA -> En línea

    data["Idioma en que se imparte la materia "] = data["Idioma en que se imparte la materia "].fillna(
        "Español")
    data["Modalidad de la clase"] = data["Modalidad de la clase"].fillna(
        "Presencial")
    data["Modalidad de la clase"] = data["Modalidad de la clase"].replace(

        "ENLINEA", "En línea")

    # if 'modalidad' is ENLINEA, then 'salon' is null
    data.loc[data['Modalidad de la clase'] == 'ENLINEA', 'Salón'] = None

    insert_data_to_db(data)

    return data


def day_from_row(row):
    """
    Process a row from the Excel data to determine the days for the schedule.

    Args:
        row (pd.Series): A row of data from the DataFrame.

    Returns:
        list of str: List of days when the class is scheduled.
    """
    days = []
    day_columns = ["Lunes", "Martes", "Miércoles",
                   "Jueves", "Viernes", "Sábado", "Domingo"]
    day_mappings = {"Lunes": "L", "Martes": "M", "Miércoles": "W",
                    "Jueves": "J", "Viernes": "V", "Sábado": "S", "Domingo": "D"}

    for day_col in day_columns:
        if pd.notna(row[day_col]):
            days.append(day_mappings[day_col])

    return days


def convert_to_24hr_format(time_str):
    """
    Converts a time string from 12-hour format to 24-hour format.

    Args:
        time_str (str): Time string in 12-hour format (e.g., '02:00 PM').

    Returns:
        str: Time string in 24-hour format.
    """
    # Convert the 12-hour time format to a datetime object
    time_obj = datetime.strptime(time_str, '%I:%M %p')

    # Format the time object to a 24-hour time string
    return time_obj.strftime('%H:%M')


def insert_data_to_db(data: pd.DataFrame) -> None:
    """
    Insert processed data into the database.

    Args:
        data (DataFrame): The processed pandas DataFrame.
    """
    for index, row in data.iterrows():
        try:
            # Crear o actualizar el profesor
            professor, _ = Professor.objects.get_or_create(
                name=row['Profesor'])

            # Crear o actualizar el salón
            room, _ = Room.objects.get_or_create(
                room_number=row['Salón'].rstrip(),
                defaults={'capacity': row['Capacidad del salón']}
            )

            # Crear o actualizar el curso
            course, _ = Course.objects.get_or_create(
                course_id=row['Id del Curso'],
                defaults={
                    'name': row['Clase'].rstrip(),
                    'catalog_number': row['No de catálogo']
                }
            )

            # Procesar los días para cada horario
            days = day_from_row(row)
            for day in days:
                Schedule.objects.get_or_create(
                    course=course,
                    professor=professor,
                    room=room,
                    start_date=row['Fecha inicial'],
                    end_date=row['Fecha final'],
                    start_time=convert_to_24hr_format(row['Hora inicio']),
                    end_time=convert_to_24hr_format(row['Hora fin']),
                    modality=row['Modalidad de la clase'].rstrip(),
                    day=day,
                )

        except IntegrityError as e:
            # Manejar posibles errores de integridad, como duplicados
            print(f"Error inserting data: {e}")
