from pprint import pprint

from django.shortcuts import render

# Create your views here.
# Design an API for a posts like/dislike system for a social media site similar to facebook, instagram, etc...
# the system allows users to see posts that have been added by the admin
# (user won't be able to submit posts, only read them for now).
# users are allowed to either like or dislike the posts
# And the next set of posts should be based on posts users previously liked or disliked.


from django_backend.GlobalImports import *
from django_backend.GlobalFunctions import *
from like_and_comments.models import Likes
from posts.models import Posts
from posts.serializers import PostsSerializers
from user_interests.models import UserIntests
from users_profile.serializers import UserSerializers


def getPostObject(post_id):
    obj = Posts.objects.filter(id=post_id)
    if obj.count() > 0 :
        return obj.first()
    else:
        return None

def CustomPostAlgorithm(user):
    # get user interest keywords
    interest_list = []
    ui_obj = UserIntests.objects.filter(user=user)
    if ui_obj.count() > 0:
        ui_obj = ui_obj.first()
        keyword_list =  ui_obj.keyword.split(',')
        # print("Keyword : ",keyword_list)
        for word in set(keyword_list):
            if word:
                cnt = keyword_list.count(word)
                interest_list.append({"cnt":cnt,"word":word})

    return interest_list


def get_my_key(obj):
    return obj['cnt']


class PostLikeAPIView(ListAPIView):

    def get(self,request):
        data = Likes.objects.filter(posts__id=self.request.GET.get('post_id')).values('user__username','user__id')
        return ResponseFunction(1,data)


class PostsAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUserOrReadOnly]
    # permission_classes = [IsAdminUser, ReadOnly]

    serializer_class = PostsSerializers


    def get_queryset(self):
        qs = Posts.objects.all().order_by('weight')

        custom_posts = self.request.GET.get('custom_posts',1)
        if custom_posts:
            lst = CustomPostAlgorithm(self.request.user)
            lst = sorted(lst, key=lambda x: x['cnt'], reverse=True)

            qs_lists = []
            for x in lst:
                # print("xx ",x)
                qs_list = qs.exclude(id__in=qs_lists).filter(title__contains = x['word']).values_list('id', flat=True)
                qs_lists.extend((qs_list))

            qs_list_balance = qs.exclude(id__in=qs_lists).values_list('id', flat=True)
            qs_lists.extend(qs_list_balance)
            qs = Posts.objects.filter(id__in=qs_lists)

            # begin 2
            filtered_list = qs.values_list('id', flat=True)
            valid_list = []
            for x in qs_lists:
                if x in filtered_list:
                    valid_list.append(x)
            new_filtered_list = []
            a = valid_list
            b = list(filtered_list)
            for zx in a:
                b.remove(zx)
            new_filtered_list = a + b
            objects = dict([(obj.id, obj) for obj in qs])
            qs = [objects[id] for id in new_filtered_list]
            # end 2
            # print(qs)
            return  qs

        return qs

    def post(self, request):
        required = ["title"]
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'])
        else:
            print("Receved required Fields")

        try:
            # print(self.request.POST.get("name",""))



            print("Data ",self.request.data)
            serializer = PostsSerializers(data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save(posted=self.request.user)
            msg = "Data saved "

            lst_obj_images = saveImageFromList(self.request.FILES.getlist('attachements'))
            obj.files.add(*lst_obj_images)
            print("images added")

            # print("Data id or object : ", obj.id)
            return ResponseFunction(1,msg)
        except Exception as e:
            printLineNo()

            print("Excepction ", printLineNo(), " : ", e)
            # print("Excepction ",type(e))

            return ResponseFunction(0,f"Excepction occured {str(e)}")


    def delete(self, request):
        try:
            id = self.request.GET.get('id', "[]")
            if id == "all":

                Posts.objects.all().delete()
                return ResponseFunction(1, "Deleted all data")

            else:
                id = json.loads(id)
                # print(id)
                Posts.objects.filter(id__in=id).delete()
                return ResponseFunction(1, "Deleted data having id " + str(id))

        except Exception as e:
            printLineNo()

            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )
