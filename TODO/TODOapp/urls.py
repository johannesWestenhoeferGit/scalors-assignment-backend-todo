from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # all the URLS our API can access
    path( 'boards/', views.BoardList.as_view() ),
    path( 'boards/<int:pk>/', views.BoardDetail.as_view() ),
    path( 'boards/<int:pk>/nc/', views.BoardsNC.as_view() ), #nc = 1 only non completed
    path( 'todos/', views.TodoList.as_view() ),
    path( 'todos/<int:pk>/', views.TodoDetails.as_view() ),
    path( 'reminders/', views.ReminderList.as_view() ),
    path( 'reminders/<int:pk>/', views.ReminderDetails.as_view() ),
]

urlpatterns = format_suffix_patterns( urlpatterns )