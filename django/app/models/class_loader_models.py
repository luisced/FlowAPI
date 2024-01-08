from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=255)  # The name of the professor

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField()


class Course(models.Model):
    course_id = models.CharField(max_length=50)       # Id del Curso
    name = models.CharField(max_length=255)           # Materia
    catalog_number = models.CharField(max_length=50)  # No de catálogo

    def __str__(self):
        return f"{self.name} ({self.course_id})"


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    start_date = models.DateField()      # Fecha inicial
    end_date = models.DateField()        # Fecha final
    start_time = models.TimeField()      # Hora iniciofrom django.db import models

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

    # String representation of the Course model
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

    # Choices for the day_of_week field
    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    # Field for the day of the week
    day_of_week = models.CharField(max_length=1, choices=DAY_CHOICES)

    # String representation of the Schedule model
    def __str__(self):
        return f"{self.course.name} - {self.professor.name}"
    end_time = models.TimeField()        # Hora fin

    MONDAY = 'L'
    TUESDAY = 'M'
    WEDNESDAY = 'W'
    THURSDAY = 'J'
    FRIDAY = 'V'
    SATURDAY = 'S'
    SUNDAY = 'D'
    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]
    day_of_week = models.CharField(max_length=1, choices=DAY_CHOICES)

    def __str__(self):
        return f"{self.course.name} - {self.professor.name}"
