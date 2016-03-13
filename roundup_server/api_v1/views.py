from django.contrib.auth.models import User
from rest_framework import viewsets
from serializers import UserSerializer, UsersSerializer
from models import Users


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('-user_name')
    serializer_class = UsersSerializer