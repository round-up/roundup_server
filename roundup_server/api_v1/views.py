from rest_framework import viewsets
from serializers import *
from models import UserExtend, GroupBelong, Group, UnitedGroup, GroupUserLevel, GroupUsers, GroupBulletins, GroupSchedules
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import HttpResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import detail_route
import json
from permissions import IsAnonCreate
from django.shortcuts import get_object_or_404

def get_B64_JSON_Parser(fields):
    class Impl(JSONParser):
        media_type = 'application/json+b64'

        def parse(self, *args, **kwargs):
            ret = super(Impl, self).parse(*args, **kwargs)
            for field in fields:
                ret[field] = ContentFile(name=field, content=ret[field].decode('base64'))
            return ret
    return Impl

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer,)# get_B64_JSON_Parser('user_profile_image'))
    parser_classes = (JSONParser, )
    #permission_classes = (IsAnonCreate, )
    queryset = UserExtend.objects.all()

    # def __init__(self):
    #     self.queryset = self.get_queryset(self)
    #
    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return UserExtend.objects.all()
    #     else:
    #         return UserExtend.objects.filter(id=self.request.user.id)


    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        #serializer.data['password'] = request.data['password']
        wrapper = dict(serializer.data)
        wrapper['password'] = request.data['password']
        #print wrapper
        u = UserExtend.objects.create_user_by_view(wrapper)
        if u is not None:
            #headers = self.get_success_headers(serializer.data)
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)#, headers=headers)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(renderer_classes=[JSONRenderer])
    def check_password(self, request, *args, **kwargs):
        data = request.data
        chk_result = {'result' : UserExtend.objects.check_password(data)}
        return HttpResponse(json.dumps(chk_result), status=status.HTTP_200_OK)


    #
    # def retrieve(self, request, pk=None):
    #     queryset = UserExtend.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return HttpResponse(serializer.data)

    # def metadata(self, request):
    #     data = super(UserViewSet, self).metadata(request)
    #     return data
    #
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)#, files=request.files)
    #     if serializer.is_valid():
    #         self.pre_save(serializer.object)
    #         self.object = serializer.save(force_insert=True)
    #         self.post_save(self.object, created=True)
    #         self.object.set_password(self.object.password)
    #         self.object.save()
    #         headers = self.get_success_headers(serializer.data)
    #         return HttpResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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