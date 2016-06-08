from django.conf.urls import url, include
import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

user_list = views.UserViewSet.as_view({
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


router = routers.DefaultRouter()
#router.register(r'user', views.UserViewSet)
router.register(r'group_belong', views.GroupBelongViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'united_group', views.UnitedGroupViewSet)
router.register(r'group_user_level', views.GroupUserLevelViewSet)
router.register(r'group_user', views.GroupUsersViewSet)
router.register(r'group_bulletin', views.GroupBulletinsViewSet)
router.register(r'group_schedule', views.GroupSchedulesViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^user/$', user_list, name='user_list'),
    url(r'^user/check/', user_chk, name='chk_password'),
    url(r'^user/(?P<pk>[^/]+)/$', user_detail, name='user_detail'),
]