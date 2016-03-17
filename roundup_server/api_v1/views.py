from rest_framework import viewsets
from serializers import *
from models import User, GroupBelong, Group, UnitedGroup, GroupUserLevel, GroupUsers, GroupBulletins, GroupSchedules
from django.contrib.auth import models
from rest_framework.renderers import JSONRenderer


class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = AuthUserSerializer
    renderer_classes = (JSONRenderer, )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-user_name')
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, )


class GroupBelongViewSet(viewsets.ModelViewSet):
    queryset = GroupBelong.objects.all()
    serializer_class = GroupBelongSerializer
    renderer_classes = (JSONRenderer, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-group_name')
    serializer_class = GroupSerializer
    renderer_classes = (JSONRenderer, )


class UnitedGroupViewSet(viewsets.ModelViewSet):
    queryset = UnitedGroup.objects.all()
    serializer_class = UnitedGroupSerializer
    renderer_classes = (JSONRenderer, )


class GroupUserLevelViewSet(viewsets.ModelViewSet):
    queryset = GroupUserLevel.objects.all()
    serializer_class = GroupUserLevelSerializer
    renderer_classes = (JSONRenderer, )


class GroupUsersViewSet(viewsets.ModelViewSet):
    queryset = GroupUsers.objects.all()
    serializer_class = GroupUsersSerializer
    renderer_classes = (JSONRenderer, )


class GroupBulletinsViewSet(viewsets.ModelViewSet):
    queryset = GroupBulletins.objects.all()
    serializer_class = GroupBulletinsSerializer
    renderer_classes = (JSONRenderer, )


class GroupSchedulesViewSet(viewsets.ModelViewSet):
    queryset = GroupSchedules.objects.all()
    serializer_class = GroupSchedulesSerializer
    renderer_classes = (JSONRenderer, )