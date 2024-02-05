from django.shortcuts import render
from datetime import datetime
from .models import MyUser, Board, Reminder
from .forms import ReminderForm
from django.http import HttpResponseRedirect



def show_task(request, reminder_id):
    reminder = Reminder.objects.get(pk=reminder_id)
    return render(request, 'reminders/show_task.html',
                  {'reminder': reminder})

def add_reminder(request):
    submitted = False
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return 	HttpResponseRedirect('/add_reminder?submitted=True')
    else:
        form = ReminderForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'reminders/add_reminder.html', {'form':form, 'submitted':submitted})


def home(request):
    time = int(datetime.now().strftime('%H'))
    if 5 <= time < 12:
        message = 'Morning!'
    elif 12 <= time < 18:
        message = 'Afternoon!'
    elif 18 <= time < 23:
        message = 'Evening!'
    elif 23 <= time or 0 <= time < 5:
        message = 'Night!'

    weekday = datetime.now().strftime('%A')
    date = datetime.now().strftime('%b %d, %Y')
    current_date = datetime.today()

    reminder_list = Reminder.objects.all().filter(date=current_date)
    tasks_num = len(reminder_list)

    return render(request, 'reminders/home.html', {'message':message,
                                                   'weekday':weekday,
                                                   'date':date,
                                                   'time':time,
                                                   'reminder_list':reminder_list,
                                                   'tasks_num':tasks_num})
                                                   
    