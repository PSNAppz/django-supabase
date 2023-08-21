from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User

User = get_user_model()

class UserMinSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = User
        fields = (
            'id',
            'display_name',
        )
