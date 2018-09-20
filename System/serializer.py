from rest_framework import serializers
from .models import *



class profileSer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'