from rest_framework import serializers
from .models import *



class profileSer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'

class personalSer(serializers.ModelSerializer):
        class Meta:
            model = personal
            fields = '__all__'