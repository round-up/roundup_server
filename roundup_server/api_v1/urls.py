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
    'get': 'retrieve',
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

group_feed_root = views.GroupFeedsViewSet.as_view({
    'get': 'list',
    'post': 'create',
})


router = routers.DefaultRouter()
#router.register(r'user', views.UserViewSet)
router.register(r'group_belong', views.GroupBelongViewSet)
#router.register(r'group', views.GroupViewSet)
router.register(r'united_group', views.UnitedGroupViewSet)
#router.register(r'group_user_level', views.GroupUserLevelViewSet)
#router.register(r'group_user', views.GroupUsersViewSet)
#router.register(r'group_bulletin', views.GroupFeedsViewSet)
router.register(r'group_schedule', views.GroupSchedulesViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
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
]