from datetime import datetime, timezone
from datetime import timedelta
import jwt



class JwtService:
    def encode(self,data):

            if not isinstance(data,dict):
                raise Exception ("data in dictionary format")

            return jwt.encode(data, "secret",algorithm="HS256")

    def decode(self,token):
        try:
            return jwt.decode(token,"secret",algorithms=["HS256"])
        except jwt.exceptions.PyJWTError as e:
            raise e