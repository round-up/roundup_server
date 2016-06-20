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
    'post': 'check_password'
})

# groups

group_root = views.GroupViewSet.as_view({
    #'get': 'list',
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

group_feed_detail = views.GroupFeedsViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

feed_list_by_group = views.GroupFeedsViewSet.as_view({
    'get': 'get_group_feeds',
})

# feed comment

feed_comment_root = views.FeedCommentViewSet.as_view({
    'post': 'add_comment',
    'get': 'get_comment_by_feed_id',
})

feed_comment_detail = views.FeedCommentViewSet.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# feed like

feed_like_root = views.FeedLikeViewSet.as_view({
    'post': 'add_like',
    'get': 'get_like_count',
})

feed_like_detail = views.FeedLikeViewSet.as_view({
    'get': 'get_likes_by_feed_id',
    'delete': 'destroy',
})

# user following

group_user_following_root = views.GroupUserFollowingViewSet.as_view({
    'post': 'create',
    'get': 'list',
})


group_user_following_detail = views.GroupUserFollowingViewSet.as_view({
    'delete': 'destroy',
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

# feed image

feed_image_root = views.FeedImageViewSet.as_view({
    'post': 'add_image_list',
})

# get feeds using group id


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
    url(r'^group_feed/(?P<pk>[^/]+)/$', group_feed_detail, name='group_feed_detail'),
    url(r'^home_feed/(?P<email>[^/]+)$', home_feed_root, name='home_feed_root'),
    url(r'^feed_comment/$', feed_comment_root, name='feed_comment_root'),
    url(r'^feed_comment/(?P<pk>[^/]+)/$', feed_comment_detail, name='feed_comment_detail'),
    url(r'^feed_like/$', feed_like_root, name='feed_like_root'),
    url(r'^feed_like/(?P<pk>[^/]+)/$', feed_like_detail, name='feed_like_detail'),
    url(r'^group_following/$', group_user_following_root, name='group_user_following_root'),
    url(r'^group_following/(?P<pk>[^/]+)/$', group_user_following_detail, name='group_user_following_detail'),
    url(r'^united_group/$', united_group_root, name='united_group_root'),
    url(r'^united_group/(?P<pk>[^/]+)/$', united_group_detail, name='united_group_detail'),
    url(r'^united_group_join/$', united_group_join, name='united_group_join'),
    url(r'^feed_image/$', feed_image_root, name='feed_image_root'),
    url(r'^group_feed/group/(?P<group_id>[^/]+)/(?P<top>[^/]+)/$', feed_list_by_group, name='feed_list_by_group'),
]