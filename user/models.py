import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import JwtService


class User(AbstractUser):

    phone_number=models.BigIntegerField()
    location=models.TextField(max_length=255)
    is_verify= models.BooleanField(default=False)

    @property
    def token(self):
         return JwtService().encode({"user_id":self.id,"username":self.username,"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=240)})



