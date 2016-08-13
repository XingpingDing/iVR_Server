from django.conf.urls import url,patterns
from iVR import views

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^user_detail/',views.user_detail,name='user_detail'),
    url(r'^upload_profilephoto/',views.upload_profilephoto,name='upload_profilephoto'),

    url(r'^news/',views.news,name='news'),
    url(r'^news_detail/',views.news_detail,name='news_detail'),
    url(r'^news_comment/',views.news_comment,name='news_comment'),

    url(r'^devices/',views.devices,name='devices'),
    url(r'^device_detail/',views.device_detail,name='device_detail'),
    url(r'^device_review/',views.device_review,name='device_review'),
    url(r'^device_search/',views.device_search,name='device_search'),

    url(r'^games/',views.games,name='games'),
    url(r'^game_detail/',views.game_detail,name='game_detail'),
    url(r'^game_review/',views.game_review,name='game_comment'),

    url(r'^videos/',views.videos,name='videos'),
    url(r'^video_detail/',views.video_detail,name='video_detail'),
    url(r'^video_review/',views.video_review,name='video_comment'),

    url(r'^feeds/',views.feeds,name='feeds'),
    url(r'^feeds_following/',views.feeds_following,name='feeds_following'),
    url(r'^feed_detail/',views.feed_detail,name='feed_detail'),
    url(r'^feed_comment/',views.feed_comment,name='feed_comment'),
    url(r'^feed_like/',views.feed_like,name='feed_like'),

    url(r'^follow/',views.follow,name='follow'),
    url(r'^followings/',views.followings,name='followings'),
    url(r'^followers/',views.followers,name='followers'),
]
