import json
import logging as lg

from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import User

lg.basicConfig(filename="user.log", format="%(asctime)s %(name)s %(levelname)s %(message)s", level=lg.DEBUG)


def registration(request):
    """
    register user details into the database
    arguments :
               request:-accept request and  load the body  with user_details in json format from the postman
    return:
              json response  success msg
    """
    try:

        lg.info(request.method)
        if request.method == 'POST':
            data = json.loads(request.body)
            user_details = User.objects.create_user(username=data.get("username"), password=data.get("password"),
                                                    email=data.get("email"), phone_number=data.get("phn_number"),
                                                    location=data.get("location"))
            # user_details.save()
            lg.debug((f" user {user_details.username} registred successfully"))
            return JsonResponse({"msg": f"{user_details.username} registered successfully"})
        return JsonResponse({"msg": "Something went wrong"})
    except Exception as e:
        lg.error(e)
        return JsonResponse({"msg": str(e)})


def login(request):
    """
    login user details into the database
    arguments :
               request:-accept request and  load the body  with user_name and password if exist  in json format from the postman
    return:
              json response  success msg
    """
    try:
        lg.info(request.method)
        if request.method == 'POST':
            data = json.loads(request.body)
            login_details = authenticate(username=data.get("username"),
                                         password=data.get("password"))
            # login_details.save()
            if login_details is not None:
                lg.debug(f"User{login_details.username} login successfully")
                return JsonResponse({"msg": f"{login_details.username} login successfully"})
            else:
                return JsonResponse({"msg": "Invalid credentials"})
        return JsonResponse({"msg": "Something went wrong"})
    except Exception as e:
        lg.error(e)
        return JsonResponse({"msg": str(e)})
