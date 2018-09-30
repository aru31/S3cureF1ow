from rest_framework import serializers
from user.models import Identity

class IdentitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Identity
        fields = ('name', 'signature')
