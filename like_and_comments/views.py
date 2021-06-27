from django.shortcuts import render
from django_backend.GlobalImports import *
from django_backend.GlobalFunctions import *
# Create your views here.
from like_and_comments.models import Likes
from like_and_comments.serializers import LikeSerializers
from posts.models import Posts
from posts.views import getPostObject
from user_interests.models import UserIntests


class LikeAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    serializer_class = LikeSerializers

    def get_queryset(self):
        qs = Likes.objects.all()
        # Begin 1
        # lst1 = [8, 35, 10, 11, 12, 21, 36, 9]
        # qs_list = qs.exclude(id__in=lst1).values_list('id', flat=True).order_by('id')
        # new_list = lst1 + list(qs_list)
        # qs = Likes.objects.filter(id__in=new_list, is_deleted=False)
        # end 1
        return qs
        # return ResponseFunction(1,"worked")

    def post(self, request):
        required = ['like','post_id']
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'])
        else:
            print("Receved required Fields")

        try:
            # print(self.request.POST.get("name",""))
            print("Data ", self.request.data)
            post_id = self.request.data['post_id']
            user = self.request.user

            post_obj = getPostObject(post_id)
            print("Post obj ",post_obj)
            if not post_obj:
                return ResponseFunction(0,"Invalid post")

            like_obj = Likes.objects.filter(posts__id = post_id,user=user)
            print("Like obj ",like_obj)
            if like_obj.count() > 0:
                serializer = LikeSerializers(like_obj.first(), data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                obj = serializer.save(posts=post_obj, user=user)
                msg = "Data updated "
            else:
                serializer = LikeSerializers(data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                obj = serializer.save(
                    posts=post_obj,
                    user=user
                )
                msg = "Data saved "


            if self.request.data['like']==1:
                collect_user_interest_words(post_id,user)

            return ResponseFunction(1,msg)
        except Exception as e:
            printLineNo()

            print("Excepction ", printLineNo(), " : ", e)
            # print("Excepction ",type(e))

            return ResponseFunction(0,f"Excepction occured {str(e)}")



def collect_user_interest_words(post_id,user,like):
    print("collect_user_interest_words called")
    post_obj = Posts.objects.filter(id=post_id)
    post_obj=post_obj.first()
    words_list = post_obj.title.split()
    interest_obj = UserIntests.objects.filter(user__id = user.id)
    keywords = ""
    # print("data collected")
    if interest_obj.count()>0:
        # print("interest_obj found")
        u_obj = interest_obj.first()
        keywords = u_obj.keyword
    else:

        u_obj = UserIntests()
        # print("interest_obj Created")
    # print("looping words_list")
    for word in words_list:
        if len(word)>= 3 :
            # and word not in keywords
            if like==1:
                keywords = keywords+","+word
            if like == -1:
                keywords = keywords.replace(word,"")
    # print("keywords : ",keywords)
    u_obj.keyword = keywords
    u_obj.user = user
    u_obj.save()



