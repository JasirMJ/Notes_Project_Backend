from django.contrib.auth.models import User
from rest_framework import serializers

from django_backend.GlobalFunctions import DynamicFieldsModelSerializer
from .models import *


class UserSerializers(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

