from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status')



class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = '__all__'




class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = '__all__'





class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = '__all__'
