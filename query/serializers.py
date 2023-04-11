from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Script, ScriptUser


# class ScriptSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Script
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ScriptUserSerializer(serializers.ModelSerializer):
    script = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ScriptUser
        fields = '__all__'


class ScriptSerializer(serializers.ModelSerializer):
    users = ScriptUserSerializer(many=True, read_only=True)

    class Meta:
        model = Script
        fields = '__all__'
