
from .views import *
from django.urls import path

urlpatterns = [
    path('', PostsAPIView.as_view(), name='post_api'),
    path('post-like/', PostLikeAPIView.as_view()),
]