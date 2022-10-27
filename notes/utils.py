import json
import logging

from notes.redis_service import GenericRedis
from user.models import User
from user.utils import JwtService


def verify_token(function):
    def wrapper(self, request):
        headers = request.headers

        token = headers.get("Token")
        if token is None:
            raise Exception("Token not found")
        payload = JwtService().decode(token)
        if "user_id" not in payload.keys():
            raise Exception("User not found ")
        user_id = payload.get("user_id")
        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise Exception(" user not found")
        request.data.update(user_id=user.id)
        print("verify_token",request.data)
        return function(self, request)

    return wrapper


class NoteRedisCrud:
    def __init__(self):

        self.redis = GenericRedis()

    def get_note(self, user_id):
        try:
            payload = self.redis.getter(user_id)
            return json.loads(payload) if payload else {}
        except Exception as e:
            logging.error(e)

    def save_note(self, notes, user_id):
        try:

            note_dict = self.get_note(user_id)
            if not user_id:
                raise ValueError("invalid datatype")


            note_id = notes.get("id")


            note_dict.update({note_id: notes})
            self.redis.setter(user_id, json.dumps(note_dict))
            # {
            #     "msg": "created successfully",
            #     "data": {
            #         "id": 19,
            #         "title": "Information",
            #         "description": "project details",
            #         "user_id": 20
            #     }
            # }
        except Exception as e:
            logging.error(e)


    def delete_note(self, user_id, id):
        try:
            note_dict = self.get_note(user_id)
            notes = note_dict.get(id)
            if notes is not None:
                note_dict.pop(id)
                self.redis.setter(user_id, json.dumps(note_dict))
        except Exception as e:
            logging.error(e)

