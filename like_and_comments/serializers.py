
from rest_framework import serializers

from .models import *

#
class LikeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = "__all__"

