from django.urls import path

from .views import *

urlpatterns = [
    path('', NotesAPI.as_view(), name='user_api'),
]