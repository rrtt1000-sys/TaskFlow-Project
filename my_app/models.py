from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Role(models.TextChoices):
        MANAGER = 'manager', 'מנהל'
        EMPLOYEE = 'employee', 'עובד'

    role = models.CharField( max_length=20, choices=Role.choices, default=Role.EMPLOYEE, verbose_name="תפקיד" )
    Team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='members',verbose_name="צוות", null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Task(models.Model):

    class Status(models.TextChoices):
        New = 'New', 'New'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    Title = models.CharField(max_length=40)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.New)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='tasks',verbose_name="מבצע המשימה", null=True, blank=True)
    Team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='tasks', verbose_name="צוות", null=True, blank=True)

    def __str__(self):
        return self.Title