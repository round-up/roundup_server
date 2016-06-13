# -*- coding : utf-8 -*-
from rest_framework import viewsets
from serializers import *
from models import UserExtend, GroupBelong, Group, UnitedGroup, GroupUserLevel, GroupUsers, GroupFeeds, GroupSchedules
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import HttpResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import detail_route
from django.core import serializers
import json
from django.forms.models import model_to_dict
from datetime import date
import dateutil.parser
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

def convert_inst_to_json(inst):
    result = serializers.serialize("json", inst)
    temp = json.loads(result)
    result = []
    for item in temp:
        item['fields']['pk'] = item['pk']
        result.append(item['fields'])
    result = json.dumps(result)
    return result

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


class GroupBelongViewSet(viewsets.ModelViewSet):
    queryset = GroupBelong.objects.all()
    serializer_class = GroupBelongSerializer
    renderer_classes = (JSONRenderer, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-group_name')
    serializer_class = GroupSerializer
    renderer_classes = (JSONRenderer, )

    @detail_route(renderer_classes=[JSONRenderer])
    def group_detail(self, request, *args, **kwargs):
        super_result = super(GroupViewSet, self).retrieve(request, args, kwargs)
        try:
            d = super_result.data
            group_id = d['id']
            leader = UserExtend.objects.get_by_natural_key(d['group_leader_email'])
            users = GroupUsers.objects.get_all_users_in_group(group_id)
            d['users'] = [model_to_dict(leader)]
            # get detail user info
            for user in users:
                email = model_to_dict(user)['email']
                user_info = UserExtend.objects.get_by_natural_key(email)
                d['users'].append(model_to_dict(user_info))

            # check date time
            for idx, user in enumerate(d['users']):
                print user
                if type(user['user_birth']) == date:
                    user['user_birth'] = user['user_birth'].strftime('yyyy-MM-dd')
                    d['users'][idx] = user
                print user
            print json.dumps(d)
            return HttpResponse(json.dumps(d), status=status.HTTP_200_OK)
        except Exception, e:
            print e.message
            return HttpResponse('{"message" : "404 bad request"}', status=status.HTTP_400_BAD_REQUEST)


    def list_by_user(self, request, group_leader_email):
        #serializer = self.get_serializer(data=request.data)
        #serializer.is_valid()
        email = group_leader_email#serializer.data['group_leader_email']
        if email is not None:
            result = {}
            inst = Group.objects.filter_group_by_leader(email)
            result_part1 = convert_inst_to_json(inst)
            inst2 = Group.objects.filter_group_by_group_user(email)
            result_part2 = convert_inst_to_json(inst2)

            print result_part1
            print result_part2
            if result_part1 is not None:
                result['leader'] = result_part1
            if result_part2 is not None:
                result['member'] = result_part2
            if len(result) == 0:
                result['message'] = 'There is no groups.'

            result = json.dumps(result)
            if inst is not None:
                return HttpResponse(result, status=status.HTTP_200_OK)#, headers=headers)
        return HttpResponse('{"message" : "no email passed"}', status=status.HTTP_400_BAD_REQUEST)



class UnitedGroupViewSet(viewsets.ModelViewSet):
    queryset = UnitedGroup.objects.all()
    serializer_class = UnitedGroupSerializer
    renderer_classes = (JSONRenderer, )


class GroupUserLevelViewSet(viewsets.ModelViewSet):
    queryset = GroupUserLevel.objects.all()
    serializer_class = GroupUserLevelSerializer
    renderer_classes = (JSONRenderer, )

    def list(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        group_id = serializer.data['group_id']
        if group_id is not None:
            inst = GroupUserLevel.objects.get_all_user_level(group_id)
            result = convert_inst_to_json(inst)
            if inst is not None:
                return HttpResponse(result, status=status.HTTP_200_OK)#, headers=headers)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupUsersViewSet(viewsets.ModelViewSet):
    queryset = GroupUsers.objects.all()
    serializer_class = GroupUsersSerializer
    renderer_classes = (JSONRenderer, )

    def list(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        group_id = serializer.data['group_id']
        if group_id is not None:
            inst = GroupUsers.objects.get_all_users_in_group(group_id = group_id)
            result = convert_inst_to_json(inst)
            if inst is not None:
                return HttpResponse(result, status=status.HTTP_200_OK)#, headers=headers)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_by_email(self, request=None, pk=None):
        if pk is None:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            result = GroupUsers.objects.delete_by_useremail(pk)
            result = json.dumps(result)
            return HttpResponse(result, status=status.HTTP_200_OK)#, headers=headers)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        group_id = serializer.data['group_id']
        email = serializer.data['email']
        if group_id is None or email is None:
            HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = GroupUsers.objects.add_group_user(group_id=group_id, email=email)
            result = json.dumps(result)
            return HttpResponse(result, status=status.HTTP_200_OK)

class GroupFeedsViewSet(viewsets.ModelViewSet):
    queryset = GroupFeeds.objects.all()
    serializer_class = GroupFeedsSerializer
    renderer_classes = (JSONRenderer, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if serializer.data is not None :
            result = GroupFeeds.objects.create(serializer.data)
            if result['result'] == 'fail':
                return HttpResponse(json.dumps(result), status=status.HTTP_400_BAD_REQUEST)
            else:
                return HttpResponse(json.dumps(result), status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def get_home_feeds(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid()
        if serializers.data is not None :
            email = serializers.data['email']
            result = GroupFeeds.objects.get_home_feeds(email)
        return HttpResponse(json.dumps(result), status=status.HTTP_200_OK)

    def get_group_feeds(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid()



class GroupSchedulesViewSet(viewsets.ModelViewSet):
    queryset = GroupSchedules.objects.all()
    serializer_class = GroupSchedulesSerializer
    renderer_classes = (JSONRenderer, )