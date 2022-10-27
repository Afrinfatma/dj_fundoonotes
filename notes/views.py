import logging as lg

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.utils import verify_token
from .models import Notes, Label
from .serializers import NotesSerializer, LabelSerializer

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
            notes = Notes.objects.filter(
                Q(user_id=request.data.get("user_id")) | Q(collaborator__id=request.data.get("user_id"))).distinct("id")
            # notes=Notes.objects.filter(user_id=request.data.get("user_id"))
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
                                                     required=['id', 'user_id']),
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


class Collaborator(APIView):
    @verify_token
    def post(self, request):
        try:

            note = Notes.objects.get(id=request.data.get("id"))
            # note.collaborator.add(request.data.get("collaborator"))     for single data
            note.collaborator.set(request.data.get("collaborator"))  # for multiple data set method is used

            return Response({"msg": "created successfully", "data": NotesSerializer(note).data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_token
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get("id"))
            note.collaborator.remove(request.data.get("collaborator"))

            return Response({"msg": "Collaborator deleted successfully", "data": {}}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)


class LabelView(APIView):
    @verify_token
    def post(self, request):
        try:
            user_id = request.data.pop("user_id")
            request.data.update(user=user_id)
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            lg.info(serializer.data)

            # return Response({"msg": "created successfully", "data": NotesSerializer(note).data},
            #                 status=status.HTTP_201_CREATED)  # serializer.data is used for deserialization
            return Response({"msg": "created successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

    @verify_token
    def get(self, request):
        """
             Args:
                 request: accepting the user id from client server or postman
             Returns:
                 response with success message
             """
        try:

            label_list = Label.objects.filter(user=request.data.get("user_id"))

            serializer = LabelSerializer(label_list, many=True)
            lg.info(serializer.data)
            return Response({"msg": "Data retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

    @verify_token
    def put(self, request):

        try:
            user_id=request.data.pop("user_id")
            request.data.update(user=user_id)
            label = Label.objects.get(id=request.data.get("id"), user=user_id)
            serializer = LabelSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # serialize the data after validation
            lg.info(serializer.data)

            return Response({"msg": "Data updated successfully", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)  # serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

    @verify_token
    def delete(self, request):

        try:

            label = Label.objects.get(id=request.data.get("id"))
            label.delete()
            return Response({"msg": "Data deleted successfully", "data": {}}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)
class LabelNote(APIView):
    @verify_token
    def post(self, request):
        try:

            note = Notes.objects.get(id=request.data.get("id"))

            note.label.set(request.data.get("label"))  # for multiple data set method is used

            return Response({"msg": "created successfully", "data": NotesSerializer(note).data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for deserialization

        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_token
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get("id"))
            note.label.remove(*request.data.get("label"))

            return Response({"msg": "Label deleted successfully", "data": {}}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)

