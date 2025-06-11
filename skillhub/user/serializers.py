from rest_framework import serializers
from .models import User
from course.serializers import CourseSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    enrolled_courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'enrolled_courses')
