from rest_framework import serializers
from .models import Waitlist

class WaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = '__all__'


