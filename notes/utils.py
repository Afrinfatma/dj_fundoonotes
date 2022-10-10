from user.models import User
from user.utils import JwtService

def verify_token(function):
    def wrapper(self,request):
        headers = request.headers
        print(headers)
        token= headers.get("Token")
        if token is None:
            raise Exception("Token not found")
        payload= JwtService().decode(token )
        if "user_id" not in payload.keys():
            raise Exception("User not found ")
        user_id = payload.get("user_id")
        user = User.objects.filter(id = user_id).first()
        if user is None:
            raise Exception(" user not found")
        request.data.update(user_id = user.id)
        return function(self,request)
    return wrapper