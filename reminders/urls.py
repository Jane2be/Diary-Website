from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('show_task/<reminder_id>', views.show_task, name="show-task"),
    path('add_reminder', views.add_reminder, name="add-reminder"),
    path('add_board', views.add_board, name="add-board"),
    path('all_boards', views.all_boards, name="all-boards"),
    path('home.html/', views.home, name='home_with_query'),
    path('edit_reminder/<reminder_id>', views.edit_reminder, name='edit-reminder'),
    path('edit_board/<board_id>', views.edit_board, name='edit-board'),
    path('delete_reminder/<reminder_id>', views.delete_reminder, name='delete-reminder'),
    path('delete_board/<board_id>', views.delete_board, name='delete-board'),
    path('toggle_switch/<int:id>/', views.toggle_switch, name='toggle-switch'),
    path('search', views.search, name='search'),
    path('reminder_pdf', views.reminder_pdf, name='reminder-pdf'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
