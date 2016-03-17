from django.conf.urls import url, include
import views
from rest_framework import routers

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
]