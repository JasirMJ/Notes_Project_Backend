from .models import *
from django_backend.GlobalImports import *
from django_backend.GlobalFunctions import *


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Notes

