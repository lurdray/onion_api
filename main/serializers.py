from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *



class AddSolutionStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    solution_id = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status', 'solution_id')

class AddProblemStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    problem_id = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status', 'problem_id')


class SignInStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    auth_code = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status', 'auth_code')

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
