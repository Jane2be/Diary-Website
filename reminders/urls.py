from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('show_task/<reminder_id>', views.show_task, name="show-task"),
    path('add_reminder', views.add_reminder, name="add-reminder"),
    path('home.html/', views.home, name='home_with_query'),

]
