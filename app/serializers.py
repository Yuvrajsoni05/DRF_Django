from django.contrib.auth.models import User
from django.forms import fields
from rest_framework import serializers
from .models import *








class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'username', 'email', 'first_name' ,'last_name'] 
        
        
        
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'username', 'email','first_name' ,'last_name','password']
        
        
    def create(self, validated_data):
        if Registration.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        
        
        user = Registration.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
      
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    password = serializers.CharField(required=True)
    
    
    
class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = "__all__"
    
    
    
class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        exclude = ['id']
        
        
        
        
        



    
        

        