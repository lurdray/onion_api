from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = '__all__'
        
class StatusLeanSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    status_lean = serializers.BooleanField(default=False)
    class Meta:
        #model = Wallet
        fields = ('status', 'status_lean')

class AddSolutionStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    status_lean = serializers.BooleanField(default=False)
    solution_id = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status', 'solution_id')

class AddProblemStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    status_lean = serializers.BooleanField(default=False)
    problem_id = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status', 'problem_id')


class SignInStatusSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=False)
    message = serializers.CharField(max_length=120, default=None)
    auth_code = serializers.CharField(max_length=120, default=None)
    first_name = serializers.CharField(max_length=120, default=None)
    last_name = serializers.CharField(max_length=120, default=None)
    payment_status = serializers.BooleanField(default=False)
    
    class Meta:
        #model = Wallet
        fields = ('status', 'message', 'auth_code', 'first_name', 'last_name', 'payment_status')



class EditUserStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    status_lean = serializers.BooleanField(default=False)
    class Meta:
        #model = Wallet
        fields = ('status', 'status_lean')




class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = ('status')


class TagsSerializer(serializers.Serializer):
    #tags = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = '__all__'       


class GetAllCategoriesView(serializers.Serializer):
    #tags = serializers.CharField(max_length=120)
    class Meta:
        #model = Wallet
        fields = '__all__'       



class StatusCBSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=120)
    status_lean = serializers.BooleanField(default=False)
    class Meta:
        #model = Wallet
        fields = ('status', 'status_lean')



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = '__all__'


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
    status = serializers.BooleanField(default=False)
    profile_photo = serializers.CharField(max_length=120)
    first_name = serializers.CharField(max_length=120)
    last_name = serializers.CharField(max_length=120)
    email = serializers.CharField(max_length=120)
    payment_status = serializers.BooleanField(default=False)
    
    class Meta:
        model = AppUser
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = ("status", "profile_photo", "first_name", "last_name", "email", "payment_status")
