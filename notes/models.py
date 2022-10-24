from django.db import models
from user.models import User


class Notes(models.Model):
    title=models.CharField(max_length=25)
    description=models.CharField(max_length=300)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    collaborator=models.ManyToManyField(User,related_name="collaborator")


