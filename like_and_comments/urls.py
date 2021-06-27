
from django.urls import path

from .views import *

urlpatterns = [
    path('', LikeAPIView.as_view(), name='user_api'),

]
