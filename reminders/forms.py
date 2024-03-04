from django import forms
from django.forms import ModelForm
from .models import Reminder, Board

class BoardForm(ModelForm):
    COLORS = [
        ('primary-subtle', 'Deep Blue'),
        ('secondary-subtle', 'Grey'),
        ('success-subtle', 'Green'),
        ('danger-subtle', 'Red'),
        ('warning', 'Gold'),
        ('warning-subtle', 'Yellow'),
        ('info', 'Blue'),
        ('info-subtle', 'Light Blue'),
        ('light', 'Light'),
    ]

    color = forms.ChoiceField(choices=COLORS, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Board
        #fields = "__all__"
        fields = ('name', 'color', 'people')
        labels = {
            'name': "Board Name:",
            'color': "",
            'people': "",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Board Name'}),
            'people': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Assignees'}),
        }



class ReminderForm(ModelForm):
    class Meta:
        model = Reminder
        #fields = "__all__"
        fields = ('name', 'board', 'date', 'reminder_time', 'description', 'assignee')
        labels = {
            'name': "Reminder",
            'board': "Board",
            'date': "YYYY-MM-DD",
            'reminder_time': "HH:MM:SS",
            'description': "Description",
            'assignee': "Assignees",

        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reminder'}),
            'board': forms.Select(attrs={'class':'form-select', 'placeholder':'Board'}),
            'date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reminder Date'}),
            'reminder_time': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reminder Time'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
            'assignee': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Assignees'}),
        }