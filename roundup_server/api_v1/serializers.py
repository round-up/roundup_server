from django.contrib.auth import models
from rest_framework import serializers
from models import User


# Service User
class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user_email = serializers.CharField(max_length=100)
    user_passwd = serializers.CharField(max_length=16)
    user_name = serializers.CharField(max_length=50)
    user_birth = serializers.TimeField(format='yyyy-MM-dd')
    user_gender = serializers.BooleanField(default=False)
    user_profile_image = serializers.ImageField(required=False)
    user_curver = serializers.ImageField(required=False)
    user_phone_number = serializers.CharField(max_length=20, required=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_email = validated_data.get('user_email', instance.user_email)
        instance.user_passwd = validated_data.get('user_passwd', instance.user_passwd)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.user_birth = validated_data.get('user_birth', instance.user_birth)
        instance.user_gender = validated_data.get('user_gender', instance.user_gender)
        instance.user_profile_image = validated_data.get('user_profile_image', instance.user_profile_image)
        instance.user_curver = validated_data.get('user_curver', instance.user_curver)
        instance.user_phone_number = validated_data.get('user_phone_number', instance.user_phone_number)
        instance.save()
        return instance


# Auth User
class AuthUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ('url', 'username', 'email', 'groups')
