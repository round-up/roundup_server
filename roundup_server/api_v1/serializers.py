from rest_framework import serializers
from models import UserExtend, GroupBelong, Group, UnitedGroup, GroupUserLevel, GroupUsers, GroupFeeds, GroupSchedules, FeedLike, FeedComment, FeedImage, GroupUserFollowing
from additionals import Base64ImageField

# Service User
class UserSerializer(serializers.ModelSerializer):

    #user_profile_image = Base64ImageField()

    class Meta:
        model = UserExtend
        fields = '__all__'
        extra_kwargs = {
            'user_profile_image': {'required': False},
            'user_cover': {'required': False},
            'user_phone_number': {'required': False},
            'password': {'write_only': True},
            'last_login': {'write_only': True},
            'is_admin': {'write_only': True}
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
            'group_cover': {'required': False},
            'group_category': {'required': False},
            'group_belong': {'required': False},
            'group_place': {'required': False},
            'group_description': {'required': False}
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


class GroupFeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupFeeds
        fields = '__all__'


class GroupSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSchedules
        fields = '__all__'


class FeedLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedLike
        fields = '__all__'


class FeedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedComment
        fields = '__all__'


class FeedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedImage
        fields = '__all__'


class GroupUserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUserFollowing
        fields = '__all__'