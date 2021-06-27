
from rest_framework import serializers

from .models import *


class UserIntestSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserIntests
        fields = "__all__"

