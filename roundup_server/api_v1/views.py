from django.contrib.auth import models
from rest_framework import viewsets
from serializers import AuthUserSerializer, UserSerializer
from models import User


class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = AuthUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-user_name')
    serializer_class = UserSerializer