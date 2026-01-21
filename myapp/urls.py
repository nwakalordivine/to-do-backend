from django.urls import path
from . import views

urlpatterns = [
    path('create-task/', views.CreateTask.as_view()),
    path('update-task/<int:pk>/', views.UpdateTaskStatus.as_view()),
    path('delete-task/<int:pk>/', views.DestroyTask.as_view()),
    path('gettask-total/', views.NumberOfTask.as_view())
]