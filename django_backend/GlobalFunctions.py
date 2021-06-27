#Variables
import sys
from .GlobalImports import *

from rest_framework.response import Response

from medias.models import Medias

STATUS = "Status"
MESSAGE = "Message"


#Functions
def ResponseFunction(status,message):
    false_list = [0,"false",False,"0"]
    if status in false_list:
        status = False
    else:
        status = True



    return Response({
        STATUS: status,
        MESSAGE: message
    })

def printLineNo():
    return str(format(sys.exc_info()[-1].tb_lineno))

def excludeValidation(exculded,data_dic):
    errors = []
    print("Receved data ",data_dic)

    message = ""

    for field in exculded:
        print(f"checking {field} in data")
        if field in data_dic:
            message = f"Remove {field} from data body"
            errors.append({"error": message})
        else:

            print("Non required field found")

            # print(message)
        # print(f"Conclusion of {field} : ",message)
    print(errors)

    return errors

def ValidateRequest(required,data_dic):
    errors = []

    message = ""
    for field in required:
        if field not in data_dic:
            message =f"Required {field}"
            errors.append({"error":message})
        else:
            if data_dic[field] == "" or not data_dic[field]:
                message = f"{field} cannot be empty"
                errors.append({"error": message})
                # print(message)
            else:
                message = f"{field} found"
            # print(message)
        # print(f"Conclusion of {field} : ",message)

    if len(errors):
        'Print if there where errors'
        print(errors)
    return errors


def saveImageFromList(lst_image):
    print("saveImageFromList : ",lst_image)
    lst_output = []
    for image in lst_image:
        print("ImageFromList : ", image)
        if image == None:
            continue
        if image == "null":
            continue

        # type = getContentTypeObject(image)

        # flag = type.find("image",0,len(type) - 1)
        #
        # if flag == -1:
        #     print("file rejected")
        #     continue


        obj = Medias()
        obj.file = image
        obj.type = "image"
        obj.save()
        lst_output.append(obj)

    return lst_output

# def getContentTypeObject(in_memory_file):
        #     mime = magic.from_buffer(in_memory_file.read(), mime=True)
        #     return mime


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        request = kwargs.get('context', {}).get('request')
        ex_list = json.loads(request.GET.get("ex_list","[]") if request else "[]")

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif exclude is not None:
            # drop fields that are specified in the 'exclude' argument
            for field_name in set(exclude):
                self.fields.pop(field_name)
        for field_name in set(ex_list):
            self.fields.pop(field_name)


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly,
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin