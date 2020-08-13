from django.urls import path, include
from . import views
from .views import *


urlpatterns = [
    path('taskapi/', TaskApi.as_view()),
    path('taskupdateapi/<pk>', TaskUpdateApi.as_view()),
    path('taskdeleteapi/<pk>', TaskDeleteApi.as_view()),
    path('tasktrackerapi/', TaskTrackerApi.as_view()),
]