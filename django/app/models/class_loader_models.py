from django.db import models

# Professor model


class Professor(models.Model):
    name = models.CharField(max_length=255)  # The name of the professor

    # String representation of the Professor model
    def __str__(self):
        return self.name

# Room model


class Room(models.Model):
    room_number = models.CharField(max_length=50)  # Room number
    capacity = models.IntegerField()  # Room capacity

# Course model


class Course(models.Model):
    course_id = models.CharField(max_length=50)  # Course ID
    name = models.CharField(max_length=255)  # Course name
    catalog_number = models.CharField(max_length=50)  # Catalog number

    def __str__(self):
        return f"{self.name} ({self.course_id})"

# Schedule model


class Schedule(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)  # Course foreign key
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE)  # Professor foreign key
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE)  # Room foreign key

    start_date = models.DateField()  # Start date of the schedule
    end_date = models.DateField()  # End date of the schedule
    start_time = models.TimeField()  # Start time of the schedule
    end_time = models.TimeField()  # End time of the schedule

    # Constants for days of the week
    MONDAY = 'L'
    TUESDAY = 'M'
    WEDNESDAY = 'W'
    THURSDAY = 'J'
    FRIDAY = 'V'
    SATURDAY = 'S'
    SUNDAY = 'D'
    DAY_CHOICES = [
        (MONDAY, 'Lunes'),
        (TUESDAY, 'Martes'),
        (WEDNESDAY, 'Miércoles'),
        (THURSDAY, 'Jueves'),
        (FRIDAY, 'Viernes'),
        (SATURDAY, 'Sábado'),
        (SUNDAY, 'Domingo'),
    ]
    day = models.CharField(max_length=1, choices=DAY_CHOICES)

    ONLINE = 'ENLINEA'
    IN_PERSON = 'PRESENCIAL'
    HYBRID = 'HIBRIDO'
    MODALITY_CHOICES = [
        (ONLINE, 'En línea'),
        (IN_PERSON, 'Presencial'),
        (HYBRID, 'Híbrido'),
    ]
    modality = models.CharField(
        max_length=10,
        choices=MODALITY_CHOICES,
        default=IN_PERSON,
    )

    def __str__(self):
        return f"{self.course.name}, {self.professor.name}, "
