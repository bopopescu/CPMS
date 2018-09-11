from rest_framework import serializers
from .models import *


class signupSer(serializers.ModelSerializer):

    class Meta:

        model = register
        fields = '__all__'


class profileSer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'