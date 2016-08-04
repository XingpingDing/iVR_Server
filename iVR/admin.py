from django.contrib import admin
from iVR.models import UserProfile, Feed, News, Device, Video, Game
from iVR.models import FeedLike, FeedComment, NewsComment, DeviceReview, VideoReview, GameReview, Follow

admin.site.register(UserProfile)
admin.site.register(Feed)
admin.site.register(News)
admin.site.register(Device)
admin.site.register(Video)
admin.site.register(Game)
admin.site.register(FeedLike)
admin.site.register(FeedComment)
admin.site.register(NewsComment)
admin.site.register(DeviceReview)
admin.site.register(VideoReview)
admin.site.register(GameReview)
admin.site.register(Follow)



