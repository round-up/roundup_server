"""roundup_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from api_v1.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'auth_users', UserViewSet)
print router.urls
# print router.urls
# user_insert = UserViewSet.as_view({
#     'post': 'create'
# })
# user_detail = UserViewSet.as_view({
#     'get' : 'retrieve'
# })

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^auth_users/(?P<pk>[0-9]+)/$', user_detail, name='user_detail'),
    # url(r'^auth_users/$', user_insert, name='user_insert'),
    url(r'^api_v1/', include('api_v1.urls', namespace='api_v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]