from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import MyUser, Board, Reminder
from .forms import ReminderForm, BoardForm
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
import urllib.request
import json
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
 

def reminder_pdf(request):
     buf = io.BytesIO()
     canv = canvas.Canvas(buf, pagesize=letter, bottomup=0)
     textob = canv.beginText()
     textob.setTextOrigin(inch, inch)
     textob._setFont('Helvetica', 12)

     date = datetime.now().strftime('%Y-%m-%d')
     reminder_raw_list = Reminder.objects.all().filter(date=date).order_by('reminder_time')
     reminder_no_time = [reminder for reminder in reminder_raw_list if reminder.reminder_time is None]
     reminder_list = [reminder for reminder in reminder_raw_list if reminder.reminder_time is not None]
     for reminder in reminder_no_time:
         reminder_list.append(reminder)
     lines = []
     for reminder in reminder_list:
          lines.append(reminder.name)
          lines.append(f"Board: {reminder.board.name}")
          lines.append(f"Date: {reminder.date.strftime('%d.%m.%Y')}")
          if reminder.reminder_time:
            lines.append(f"Time: {reminder.reminder_time.strftime('%H.%M')}")
          if reminder.description:
            lines.append(f"Description: {reminder.description}")
          lines.append(reminder.created_date.strftime('%d.%m.%Y %H.%M'))
          lines.append(' ')

     for line in lines:
          textob.textLine(line)

     canv.drawText(textob)
     canv.showPage()
     canv.save()
     buf.seek(0)

     return FileResponse(buf, as_attachment=True, filename='Tasks.pdf')
    

def toggle_switch(request, id):
    if request.method == 'POST':
        reminder = Reminder.objects.get(pk=id)
        reminder.status = not reminder.status
        reminder.save()

    # Get the previous path from the referer header
    previous_path = request.META.get('HTTP_REFERER')

    # Construct the URL to redirect to the previous path with the anchor
    if previous_path:
        redirect_url = f"{previous_path}#{id}"
    else:
        redirect_url = reverse('home')  # Default to home page if no previous path

    return HttpResponseRedirect(redirect_url) # If there is no previous path, redirect to the default home page

def search(request):
	if request.method == "POST":
		searched = request.POST['searched']
		reminder_list = Reminder.objects.filter(name__contains=searched)
		
		return render(request, 'reminders/search.html',
                  {'searched':searched,
				   'reminder_list':reminder_list,
                   })
	else:
		return render(request, 'reminders/search.html',
                  {})

def delete_reminder(request, reminder_id):
	reminder = Reminder.objects.get(pk=reminder_id)
	reminder.delete()
	return redirect ('home')

def delete_board(request, board_id):
	board = Board.objects.get(pk=board_id)
	board.delete()
	return redirect ('all-boards')

def edit_reminder(request, reminder_id):
	reminder = Reminder.objects.get(pk=reminder_id)
	form = ReminderForm(request.POST or None, instance=reminder)
	if form.is_valid():
		form.save()
		return redirect('home')
	return render(request, 'reminders/edit_reminder.html',
                  {'reminder': reminder,
				   'form':form})

def edit_board(request, board_id):
	board = Board.objects.get(pk=board_id)
	form = BoardForm(request.POST or None, instance=board)
	if form.is_valid():
		form.save()
		return redirect('all-boards')
	return render(request, 'reminders/edit_board.html',
                  {'board': board,
				   'form':form})

def all_boards(request):
    board_list = Board.objects.all().order_by('name') #'?' = random
    return render(request, 'reminders/all_boards.html',
                  {'board_list': board_list})

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

    return render(request, 'reminders/add_reminder.html', {'form':form, 'submitted':submitted,})

def add_board(request):
    submitted = False
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return 	HttpResponseRedirect('/add_board?submitted=True')
    else:
        form = BoardForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'reminders/add_board.html', {'form':form, 'submitted':submitted})


def home(request):
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

    wd = request.GET.get('wd')
    year, month, day = show_day(wd)
    
    time = int(datetime.now().strftime('%H')) + 2
    time_now = datetime.now().strftime('%H.%m')
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

    reminder_raw_list = Reminder.objects.all().filter(date=current_date).order_by('reminder_time')
    reminder_no_time = [reminder for reminder in reminder_raw_list if reminder.reminder_time is None]
    reminder_list = [reminder for reminder in reminder_raw_list if reminder.reminder_time is not None]
    for reminder in reminder_no_time:
         reminder_list.append(reminder)
    tasks_num = len(reminder_list)
    done_tasks = sum(1 for reminder in reminder_list if reminder.status == True)
    if tasks_num > 0:
        done_percent = int(done_tasks / tasks_num *100)
    else:
         done_percent = 100
    current_date_str = datetime.strptime(current_date, "%Y-%m-%d")

    user = MyUser.objects.all()
    city = ''.join([i.city for i in user])

    def get_weather(city):
        API = 'ff6275d9ae24d29cfd3404474a66346e'
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"
            res = urllib.request.urlopen(url)
            data = json.loads(res.read().decode('utf-8'))
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"cod": "404"}
            else:
                raise

    weather_data = get_weather(city)
    if weather_data["cod"] == "404":
        city = "The city is not found."
    else:
        temperature = round(weather_data['main']['temp'])
        temp_min = round(weather_data['main']['temp_min'])
        temp_max = round(weather_data['main']['temp_max'])
        feels_like = round(weather_data['main']['feels_like'])
        humidity = round(weather_data['main']['humidity'])
        weather_description = weather_data['weather'][0]['description']

    return render(request, 'reminders/home.html', {'message':message,
                                                   'weekday':weekday,
                                                   'date':date,
                                                   'time_now':time_now,
                                                   'reminder_list':reminder_list,
                                                   'tasks_num':tasks_num,
                                                   'current_date_str':current_date_str,
                                                   'done_tasks':done_tasks,
                                                   'done_percent':done_percent,
                                                   'city':city,
                                                   'temperature':temperature,
                                                   'weather_description':weather_description,
                                                   'feels_like':feels_like,
                                                   'humidity':humidity,
                                                   'temp_min':temp_min,
                                                   'temp_max':temp_max,
                                                   })
                                                   
    