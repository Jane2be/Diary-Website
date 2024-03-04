from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class MyUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Board(models.Model):
    name = models.CharField('Board Name', max_length=120)
    color = models.CharField('Board Color', max_length=20)
    people = models.ManyToManyField(MyUser)

    def __str__(self):
        return self.name

class Reminder(models.Model):
    #define columns
    name = models.CharField('Reminder', max_length=120)
    board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField('Date')
    reminder_time = models.TimeField('Time', blank=True, null=True)
    description = models.TextField(blank=True)
    assignee = models.ManyToManyField(MyUser, blank=True)
    status = models.BooleanField('Status', default=False)
    created_date = datetime.now()
    created_by = User
    def __str__(self):
        return self.name