from rest_framework_simplejwt.authentication import JWTAuthentication

from django_backend.GlobalFunctions import *
from django_backend.GlobalImports import *
# Create your views here.
from notes.models import *
from notes.serializers import NotesSerializer


class NotesAPI(ListAPIView):

    serializer_class = NotesSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pagination = self.request.GET.get('pagination', '1')
        if pagination == '0':
            print("Pagination None")
            self.pagination_class = None

        queryset = Notes.objects.all().order_by("-id")
        return queryset

    def post(self, request):
        print(self.request.data)
        required = ["heading"]
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'])
        else:
            print("Receved required Fields")

        try:
            # print(self.request.POST.get("name",""))
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            msg = "Data saved "
            print(msg)
            return ResponseFunction(1,msg)
        except Exception as e:
            printLineNo()
            print("Excepction ", printLineNo(), " : ", e)
            return ResponseFunction(0,f"Excepction occured {str(e)}")

    def put(self, request):
        # ResponseFunction(0,"Not enabled")
        required = ["heading"]
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'])
        else:
            print("Receved required Fields")


        id = self.request.POST.get("id")
        if not id or id == "":
            return Response({
                STATUS: False,
                MESSAGE: "Required object id as id"
            })
        serializer = NotesSerializer(Notes.objects.filter(id=id).first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseFunction(1, "Data updated")


    def delete(self, request):
        try:
            id = self.request.GET.get('id', "[]")
            if id == "all":

                Notes.objects.all().delete()
                return ResponseFunction(1, "Deleted all data")

            else:
                id = json.loads(id)
                # print(id)
                Notes.objects.filter(id__in=id).delete()
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
