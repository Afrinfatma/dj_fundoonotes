

from django.db import models


from user.models import User


class Label(models.Model):
    title = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)


class Notes(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborator = models.ManyToManyField(User, related_name="collaborator")
    label = models.ManyToManyField(Label, related_name="label")



