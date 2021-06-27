from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#


from django_backend.GlobalImports import *
from django_backend.GlobalFunctions import *
from users_profile.serializers import UserSerializers


class UsersAPIView(ListAPIView):
    # 'rest_framework.permissions.IsAuthenticated',
    # authentication_classes = (JSONWebTokenAuthentication,)
    authentication_classes = (JWTAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializers
    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def post(self, request):
        required = []
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'])
        else:
            print("Receved required Fields")

        try:
            # print(self.request.POST.get("name",""))

            print("Data ", self.request.data)
            serializer = UserSerializers(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save(password=make_password(self.request.data['password']))
            msg = "Data saved "


            # print("Data id or object : ", obj.id)
            return ResponseFunction(1, msg)
        except Exception as e:
            printLineNo()

            print("Excepction ", printLineNo(), " : ", e)
            # print("Excepction ",type(e))

            return ResponseFunction(0, f"Excepction occured {str(e)}")

class LoginView(ObtainAuthToken):

    def get(self,request):
        return Response({
            True
        })

    def post(self, request, *args, **kwargs):
        # print("Login request recieved :",self.request.POST.get("username"))
        # print("Data ",request.data)

        required = ["username","password"]
        validation_errors = ValidateRequest(required,self.request.data)

        if len(validation_errors)>0:
            return ResponseFunction(0,validation_errors[0]['error'])
        else:
            print("Receved required Fields")


        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # print(serializer)
        try:
            test = serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']


            token, created = Token.objects.get_or_create(user=user)
            return Response({
                STATUS:True,
                'token': "Token "+token.key,
                'user_id': user.pk,
                'username': user.username,
                'is_staff':user.is_staff,
                'is_superuser':user.is_superuser,
            })
        except Exception as e:
            return Response({
                STATUS:False,
                MESSAGE:"Incorrect Username or Password",
                "excepction":str(e),
            })

