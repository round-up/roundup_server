from rest_framework import serializers
from models import UserExtend, GroupBelong, Group, UnitedGroup, GroupUserLevel, GroupUsers, GroupBulletins, GroupSchedules


# Service User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtend
        fields = '__all__'
        extra_kwargs = {
            'user_profile': {'required': False},
            'user_cover': {'required': False},
            'user_phone_number': {'required': False},
            'user_passwd': {'write_only': True}
        }


class GroupBelongSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBelong
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        extra_kwargs = {
            'group_logo': {'required': False},
            'group_cover': {'required': False}
        }


class UnitedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitedGroup
        fields = '__all__'


class GroupUserLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUserLevel
        fields = '__all__'


class GroupUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUsers
        fields = '__all__'


class GroupBulletinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBulletins
        fields = '__all__'


class GroupSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSchedules
        fields = '__all__'