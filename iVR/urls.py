from django.conf.urls import url,patterns
from iVR import views

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^user_detail/',views.user_detail,name='user_detail'),
    url(r'^news/',views.news,name='news'),
    url(r'^news_detail/',views.news_detail,name='news_detail'),
    url(r'^news_comment/',views.news_comment,name='news_comment'),
    url(r'^devices/',views.devices,name='devices'),
    url(r'^device_detail/',views.device_detail,name='device_detail'),
    url(r'^device_review/',views.device_review,name='device_review'),
    url(r'^games/',views.games,name='games'),
    url(r'^game_detail/',views.game_detail,name='game_detail'),
    url(r'^game_review/',views.game_review,name='game_comment'),
    url(r'^videos/',views.videos,name='videos'),
    url(r'^video_detail/',views.video_detail,name='video_detail'),
    url(r'^video_review/',views.video_review,name='video_comment'),
    url(r'^feeds/',views.feeds,name='feeds'),
]
