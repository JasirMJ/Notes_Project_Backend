from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class UsersAPIView(ListAPIView):
    # 'rest_framework.permissions.IsAuthenticated',
    # authentication_classes = (JSONWebTokenAuthentication,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(self.request.user)
        return Response({"status":True,"message":"get method worked"})
#
# class LoginView(ObtainAuthToken):
#
#     def get(self,request):
#         return Response({
#             True
#         })
#
#     def post(self, request, *args, **kwargs):
#         # print("Login request recieved :",self.request.POST.get("username"))
#         # print("Data ",request.data)
#
#         required = ["username","password"]
#         validation_errors = ValidateRequest(required,self.request.data)
#
#         if len(validation_errors)>0:
#             return ResponseFunction(0,validation_errors[0]['error'])
#         else:
#             print("Receved required Fields")
#
#
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         # print(serializer)
#         try:
#             test = serializer.is_valid(raise_exception=True)
#             user = serializer.validated_data['user']
#
#
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 STATUS:True,
#                 'token': "Token "+token.key,
#                 'user_id': user.pk,
#                 'username': user.username,
#                 'is_staff':user.is_staff,
#                 'is_superuser':user.is_superuser,
#             })
#         except Exception as e:
#             return Response({
#                 STATUS:False,
#                 MESSAGE:"Incorrect Username or Password",
#                 "excepction":str(e),
#             })
#
