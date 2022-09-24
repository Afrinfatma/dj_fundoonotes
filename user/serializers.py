from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    serialization is the process of converting user readable data into machine understandable code
    and deserialization is vice versa
     ModelSerializer classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:

    An automatically determined set of fields.
    Simple default implementations for the create() and update() methods.
    """

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'location']
        read_only_fields=['id']
