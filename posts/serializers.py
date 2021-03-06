
from rest_framework import serializers

from like_and_comments.models import Likes
from medias.serializers import MediaSerializers
from .models import *


class PostsSerializers(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()
    files = MediaSerializers(many=True)

    class Meta:
        model = Posts
        fields = ["id","title","files","created","desc","posted","weight","like","dislike"]

    def get_like(self,obj):
        # self.context
        like_count = Likes.objects.filter(posts=obj,like=1).count()
        return like_count
    def get_dislike(self,obj):
        dislike_count = Likes.objects.filter(posts=obj, like=-1).count()
        return dislike_count

