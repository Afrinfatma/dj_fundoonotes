from .models import Notes
from rest_framework import serializers

class NotesSerializer(serializers.ModelSerializer):
    """
       serialization is the process of converting user readable data into machine understandable code
       and deserialization is vice versa
        ModelSerializer classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:

       An automatically determined set of fields.
       Simple default implementations for the create() and update() methods.
       """
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user_id',]
        read_only_fields = ['id']

