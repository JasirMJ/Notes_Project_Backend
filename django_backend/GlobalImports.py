from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from rest_framework import serializers
from django.urls import path
import json
from rest_framework.permissions import *
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework.authtoken.views import ObtainAuthToken
import datetime

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

