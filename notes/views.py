import logging as lg

from user.models import User
from user.utils import JwtService
from .models import Notes
from .serializers import NotesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notes.utils import verify_token
from .utils import NoteRedisCrud
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

lg.basicConfig(filename="notes.log", format="%(asctime)s %(name)s %(levelname)s %(message)s", level=lg.DEBUG)
"""
Instead of writing the separate function we are using decorator
decoraters allows to preprocess the function and perform some sort of operation, before the function is executed,
we are passing the function whatever we written in decorater as a parameter, inside that wrapper function, with
this we are accessing to the parameter of the functon below the decorater(child function),in this case it is 
(self and request), when request comes it will hit the decorator first, inside decorator whatever preposseing
required that will happens and finally it will call the fuction
"""


class NotesApi(APIView):
    @swagger_auto_schema(request_body=NotesSerializer)
    @verify_token
    def post(self, request):
        """
                          Args:
                              request: accepting the note details from  postman
                          Returns:
                              response with success message
                          """
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # serialize the data after validation
            lg.info(serializer.data)

            return Response({"msg": "created successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

    # @swagger_auto_schema(request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     properties={
    #         'id': openapi.Schema(type=openapi.TYPE_INTEGER),
    #         'title': openapi.Schema(type=openapi.TYPE_STRING),
    #         'description': openapi.Schema(type=openapi.TYPE_STRING)
    #
    #     }))
    @verify_token
    def get(self, request):
        """
             Args:
                 request: accepting the user id from client server or postman
             Returns:
                 response with success message
             """
        try:
            notes = Notes.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(notes, many=True)
            # for item in serializer.data:
            #       NoteRedisCrud().save_note(item,request.data.get("user_id"))
            # lg.info(serializer.data)

            return Response({"msg": "Note retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

    @swagger_auto_schema(request_body=NotesSerializer)
    @verify_token
    def put(self, request):
        """
                 Args:
                     request: accepting the note details from  postman
                 Returns:
                     response with success message
                 """

        try:
            print(request.data)
            print(request.data.get("id"))
            notes = Notes.objects.get(id=request.data.get("id"), user_id=request.data.get("user_id"))
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # serialize the data after validation
            lg.info(serializer.data)

            return Response({"msg": "Notes updated successfully", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)  # serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={
                                                         'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                         'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                     },
                                                     required=['id','user_id']),
                         operation_summary='delete Notes')
    @verify_token
    def delete(self, request):
        """
             Args:
                 request: accepting the note id from  postman
             Returns:
                 response with success message
             """
        try:

            notes = Notes.objects.get(id=request.data.get("id"), user_id=request.data.get("user_id"))
            notes.delete()
            return Response({"msg": "Notes deleted successfully", "data": {}}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)
