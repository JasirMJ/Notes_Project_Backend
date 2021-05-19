#Variables
import sys

from rest_framework.response import Response

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

