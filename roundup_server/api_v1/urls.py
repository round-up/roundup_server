from django.conf.urls import url, include
import views
from rest_framework import routers
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

# users

user_root = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_chk = views.UserViewSet.as_view({
    'get': 'check_password'
})

# groups

group_root = views.GroupViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

group_detail = views.GroupViewSet.as_view({
    'get': 'group_detail',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

group_list_by_user = views.GroupViewSet.as_view({
    'post': 'list_by_user',
})

# group members

group_user_level_root = views.GroupUserLevelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

group_user_level_detail = views.GroupUserLevelViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

group_user_root = views.GroupUsersViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

group_user_detail = views.GroupUsersViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'delete_by_email'
})

# group feeds

home_feed_root = views.GroupFeedsViewSet.as_view({
    'get': 'get_home_feeds',
})

group_feed_root = views.GroupFeedsViewSet.as_view({
    'post': 'create',
})

# United Group

united_group_root = views.UnitedGroupViewSet.as_view({
    'post': 'create',
})

united_group_detail = views.UnitedGroupViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

united_group_join = views.UnitedGroupsBridgeViewSet.as_view({
    'post': 'create',
})


urlpatterns = [
    url(r'^user/$', user_root, name='user_list'),
    url(r'^user/check/', user_chk, name='chk_password'),
    url(r'^user/(?P<pk>[^/]+)/$', user_detail, name='user_detail'),
    url(r'^user/group/(?P<group_leader_email>[^/]+)/$', group_list_by_user, name='group_list_by_user'),
    url(r'^group/$', group_root, name='group_list'),
    url(r'^group/(?P<pk>[^/]+)/$', group_detail, name='group_detail'),
    url(r'^group_user_level/$', group_user_level_root, name='group_user_level_list'),
    url(r'^group_user_level/(?P<pk>[^/]+)/$', group_user_level_detail, name='group_user_level_detail'),
    url(r'^group_user/$', group_user_root, name='group_user_list'),
    url(r'^group_user/(?P<pk>[^/]+)/$', group_user_detail, name='group_user_detail'),
    url(r'^group_feed/$', group_feed_root, name='group_feed_root'),
    url(r'^home_feed/$', home_feed_root, name='home_feed_root'),
    url(r'^united_group/$', united_group_root, name='united_group_root'),
    url(r'^united_group/(?P<pk>[^/]+)/$', united_group_detail, name='united_group_detail'),
    url(r'^united_group/join/$', united_group_join, name='united_group_join'),
]