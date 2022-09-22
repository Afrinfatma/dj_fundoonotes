import logging
#
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
import json
from user.models import User as CustomUser
import logging as lg


lg.basicConfig(filename="user.log", format="%(asctime)s %(name)s %(levelname)s %(message)s",level="lg.debug")




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
        if request.method =='POST':
            data=json.loads(request.body)
            user_details=CustomUser(user_name=data.get("user_name"),password=data.get("password"),
                              email=data.get("email"),phn_number=data.get("phn_number"),
                              location=data.get("location"))
            user_details.save()
            lg.debug((f" user {user_details.user_name} registred successfully"))
            return JsonResponse({"msg":f"{user_details.user_name} registered successfully"})
        return JsonResponse ({"msg":"Something went wrong"})
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
        if request.method=='POST':
            data=json.loads(request.body)
            login_details = CustomUser.objects.get(user_name=data.get("user_name"),
                               password=data.get("password"))
            # login_details.save()
            if login_details is not None:
                lg.debug (f"User{login_details.user_name} login successfully")
                return JsonResponse({"msg":f"{login_details.user_name} login successfully"})
            else:
                return JsonResponse({"msg":"Invalid credentials"})
        return JsonResponse({"msg":"Something went wrong"})
    except Exception as e:
        lg.error(e)
        return JsonResponse({"msg": str(e)})
