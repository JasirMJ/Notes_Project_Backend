
from rest_framework import serializers

from .models import *


class PostsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Medias
        fields = "__all__"

