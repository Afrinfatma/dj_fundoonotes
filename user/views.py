
import logging as lg
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

lg.basicConfig(filename="user.log", format="%(asctime)s %(name)s %(levelname)s %(message)s", level=lg.DEBUG)

class UserRegistration(APIView):

    def post(self, request, format=None):
        """
                   Args:
                       request: accepting the user details from  postman
                   Returns:
                       response with success message
                   """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()# serialize the data after validation
            return Response({"msg":"created successfully","data":serializer.data},status=status.HTTP_201_CREATED)#serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"msg":str(e)},status=400)
class UserLogin(APIView):

    def post(self,request):
        """
              Args:
                  request: accepting the user details from  postman
              Returns:
                  response with success message
              """
        try:

                login_details = authenticate(**request.data)

                if login_details is not None:
                    lg.debug(f"User{login_details.username} login successfully")
                    return Response({"msg": f"{login_details.username} login successfully"},status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"msg": "Invalid credentials"},status=400)

        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)},status==400)
