from django.contrib import admin
from .models import Reminder
from .models import MyUser
from .models import Board

admin.site.register(Reminder)
admin.site.register(MyUser)
admin.site.register(Board)
