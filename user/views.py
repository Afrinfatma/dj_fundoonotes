import logging as lg

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from dj_fundoo_notes import settings
from .models import User
from .serializers import UserSerializer
from .utils import JwtService

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
            serializer.save()  # serialize the data after validation
            token = JwtService().encode({"user_id": serializer.data.get("id"),
                                         "username": serializer.data.get("username")})
            send_mail(
                subject='Json Web Token For User Registration',
                message=settings.BASE_URL +
                        reverse('verify_token', kwargs={"token": token}),
                from_email=None,
                recipient_list=[serializer.data.get('email')],
                fail_silently=False,
            )
            return Response({"msg": "created successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)


class UserLogin(APIView):

    def post(self, request):
        """
              Args:
                  request: accepting the user details from  postman
              Returns:
                  response with success message
              """
        try:

            user = authenticate(**request.data)

            if not user:
                return Response({"msg": "Invalid credentials"}, status=400)

            return Response({"msg": f"{user.username} login successfully","data":{"token":user.token}},
                            status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status == 400)


class VerifyToken(APIView):
    def get(self, request, token):
        """
        request: sending request from the browsable api
        after generating the token from registraion process, this function will decode with username and return
        with success message
        """
        try:
            decoded_data = JwtService().decode(token)
            if "username" not in decoded_data:
                raise Exception("Invalid Token")
            user = User.objects.get(username=decoded_data.get("username"))
            user.is_verify = True
            user.save()
            return Response({"message": "User verified"})
        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=400)
