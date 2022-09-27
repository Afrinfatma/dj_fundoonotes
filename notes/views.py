import logging as lg
from .models import Notes
from .serializers import NotesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

lg.basicConfig(filename="notes.log", format="%(asctime)s %(name)s %(levelname)s %(message)s", level=lg.DEBUG)


class NotesApi(APIView):

    def post(self,request):
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

    def get(self,request):
        """
             Args:
                 request: accepting the user id from client server or postman
             Returns:
                 response with success message
             """
        try:

            notes=Notes.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(notes, many=True)
            lg.info(serializer.data)
            return Response({"msg":"Note retrieved successfully","data": serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)


    def put(self,request):
            """
                 Args:
                     request: accepting the note details from  postman
                 Returns:
                     response with success message
                 """

            try:
                print(request.data)
                print(request.data.get("id"))
                notes=Notes.objects.get(id=request.data.get("id"))
                serializer = NotesSerializer(notes,data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()  # serialize the data after validation
                lg.info(serializer.data)
                return Response({"msg": "Notes updated successfully", "data": serializer.data},
                                status=status.HTTP_202_ACCEPTED)  # serializer.data is used for deserialization

            except Exception as e:
                lg.error(e)
                return Response({"msg": str(e)}, status=400)

    def delete(self,request):
        """
             Args:
                 request: accepting the note id from  postman
             Returns:
                 response with success message
             """
        try:
            notes=Notes.objects.get(id=request.data.get("id"))
            notes.delete()
            return Response({"msg":"Notes deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            lg.error(e)
            return Response({"msg": str(e)}, status=400)