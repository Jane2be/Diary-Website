from django.shortcuts import render
from datetime import datetime, timedelta
from .models import MyUser, Board, Reminder
from .forms import ReminderForm
from django.http import HttpResponseRedirect


def show_day(day):
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    if day == 'Monday':
        current_date = monday
    elif day == 'Tuesday':
        current_date = monday + timedelta(days=1)
    elif day == 'Wednesday':
        current_date = monday + timedelta(days=2)
    elif day == 'Thursday':
        current_date = monday + timedelta(days=3)
    elif day == 'Friday':
        current_date = monday + timedelta(days=4)
    elif day == 'Saturday':
        current_date = monday + timedelta(days=5)
    elif day == 'Sunday':
        current_date = monday + timedelta(days=6)
    else:
        current_date = today

    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    return_day = current_date.strftime('%d')


    return year, month, return_day

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
    wd = request.GET.get('wd')
    year, month, day = show_day(wd)
    
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
    current_date = f"{year}-{month}-{day}"

    reminder_list = Reminder.objects.all().filter(date=current_date).order_by('reminder_time')
    tasks_num = len(reminder_list)

    return render(request, 'reminders/home.html', {'message':message,
                                                   'weekday':weekday,
                                                   'date':date,
                                                   'time':time,
                                                   'reminder_list':reminder_list,
                                                   'tasks_num':tasks_num})
                                                   
    