from django.shortcuts import render
from iVR.forms import ImageUploadForm, FeedAddTextForm, FeedAddTextPlusPictureForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from iVR.models import User, UserProfile, Feed, News, Device, Video, Game
from iVR.models import FeedLike, FeedComment, NewsComment, DeviceReview, VideoReview, GameReview, Follow
from django.views.decorators.csrf import csrf_exempt
import json

# User register
@csrf_exempt
def register(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Check whether user is exist
            try:
                user = User.objects.get(username=username)

                context_dict['success'] = 0
                context_dict['error_message'] = 'User already exists.'

            except ObjectDoesNotExist:
                # Save user to database
                user = User.objects.create(username=username)
                user.set_password(password)
                user.save()
                userprofile = UserProfile.objects.create(user=user)

                context_dict['success'] = 1
        else:
            context_dict['success'] = 0
            context_dict['error_message'] = 'Invalid register details.'
    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Wrong Register.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# User login
@csrf_exempt
def login(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check whether user is valid
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                context_dict['success'] = 1

                userProfile = UserProfile.objects.get(user=user)

                dict = {}
                dict['username'] = getattr(user, 'username')
                dict['picture'] = getattr(userProfile, 'picture').url

                context_dict['user'] = dict

            else:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Your account is disabled.'

        else:
            context_dict['success'] = 0
            context_dict['error_message'] = 'Invalid login details.'
    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Wrong Login.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get user detail information
def user_detail(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET['username']

        try:
            user = User.objects.get(username=username)
            userProfile = UserProfile.objects.get(user=user)

            feed_list = Feed.objects.filter(user=user).order_by('-id')
            following_list = Follow.objects.filter(user=user).order_by('-id')
            follower_list = Follow.objects.filter(followeduser=user).order_by('-id')

            user_dict = {}
            user_dict['username'] = getattr(user, 'username')
            user_dict['picture'] = getattr(userProfile, 'picture').url
            user_dict['feedsnumber'] = len(feed_list)
            user_dict['followingnumber'] = len(following_list)
            user_dict['followersnumber'] = len(follower_list)

            context_dict['user'] = user_dict

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Upload profile picture
@csrf_exempt
def upload_profilepicture(request):
   context_dict = {}

   if request.method == 'POST':
       # Data from ImageUploadForm
       form = ImageUploadForm(request.POST, request.FILES)
       if form.is_valid():
           username = form.cleaned_data['username']

           # If user exists, then update profile picture
           try:
               user = User.objects.get(username=username)
               userProfile = UserProfile.objects.get(user=user)

               userProfile.picture = form.cleaned_data['pic']
               userProfile.save()

               picture = getattr(userProfile, 'picture').url

               context_dict['success'] = 1
               context_dict['picture'] = picture
           except ObjectDoesNotExist:
               context_dict['success'] = 0
               context_dict['error_message'] = 'User not exist.'
       else:
           context_dict['success'] = 0
           context_dict['error_message'] = 'Invalid data.'
   else:
       context_dict['success'] = 0
       context_dict['error_message'] = 'Request Error.'

   return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get news list
def news(request):
    news_list = News.objects.all().order_by('-id')

    list = []

    for ob in news_list:
        dict = {}
        for attr in [f.name for f in ob._meta.fields]:
            if attr == 'picture':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'date':
                dict[attr] = getattr(ob, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif attr == 'content':
                pass
            else:
                dict[attr] = getattr(ob, attr)
        list.append(dict)


    context_dict = {}
    context_dict['news'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get news detail of a specific piece of news
def news_detail(request):
    context_dict = {}

    if request.method == 'GET':
        newsid = request.GET['newsid']

        try:
            news = News.objects.get(id=newsid)

            news_dict = {}

            for attr in [f.name for f in news._meta.fields]:
                if attr == 'picture':
                    news_dict[attr] = getattr(news, attr).url
                elif attr == 'date':
                    news_dict[attr] = getattr(news, attr).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    news_dict[attr] = getattr(news, attr)

            context_dict['news'] = news_dict

            # Get comment list
            comment_list = NewsComment.objects.filter(news=news).order_by('-id')
            comments = []

            for ob in comment_list:
                comment_dict = {}

                username = ob.user.username
                date = ob.date.strftime('%Y-%m-%d %H:%M:%S')
                content = ob.content

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.user)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                comment_dict['username'] = username
                comment_dict['picture'] = picture
                comment_dict['date'] = date
                comment_dict['content'] = content

                comments.append(comment_dict)

            context_dict['comments'] = comments

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# comment on a piece of news
@csrf_exempt
def news_comment(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        newsid = request.POST.get('newsid')
        content = request.POST.get('content')

        try:
            user = User.objects.get(username=username)

            # Check whteher news exist
            # if news exist, then save comment to database
            try:
                news = News.objects.get(id=newsid)

                news.commentsnumber = news.commentsnumber + 1
                news.save()

                newscomment = NewsComment.objects.create(news=news,user=user,content=content)

                context_dict['success'] = 1
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'News not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get device list
def devices(request):
    devices_list = Device.objects.all().order_by('-id')

    list = []

    for ob in devices_list:
        dict = {}
        for attr in [f.name for f in ob._meta.fields]:
            if attr == 'picture1':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'picture2':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'picture3':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'devicedescription':
                pass
            else:
                dict[attr] = getattr(ob, attr)
        list.append(dict)


    context_dict = {}
    context_dict['devices'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get detail of a specific device
def device_detail(request):
    context_dict = {}

    if request.method == 'GET':
        deviceid = request.GET['deviceid']

        try:
            device = Device.objects.get(id=deviceid)

            device_dict = {}

            for attr in [f.name for f in device._meta.fields]:
                if attr == 'picture1':
                    device_dict[attr] = getattr(device, attr).url
                elif attr == 'picture2':
                    device_dict[attr] = getattr(device, attr).url
                elif attr == 'picture3':
                    device_dict[attr] = getattr(device, attr).url
                else:
                    device_dict[attr] = getattr(device, attr)

            context_dict['device'] = device_dict

            # Get review list of this device
            review_list = DeviceReview.objects.filter(device=device).order_by('-id')
            reviews = []

            for ob in review_list:
                review_dict = {}

                username = ob.user.username
                date = ob.date.strftime('%Y-%m-%d %H:%M:%S')
                content = ob.content
                score = ob.score

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.user)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                review_dict['username'] = username
                review_dict['picture'] = picture
                review_dict['date'] = date
                review_dict['content'] = content
                review_dict['score'] = score

                reviews.append(review_dict)

            context_dict['reviews'] = reviews

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Review on a device
@csrf_exempt
def device_review(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        deviceid = request.POST.get('deviceid')
        score = (int)(request.POST.get('score'))
        content = request.POST.get('content')

        try:
            user = User.objects.get(username=username)

            try:
                device = Device.objects.get(id=deviceid)

                # Caculate average score of this device
                device.score = (device.score * device.reviewsnumber + score) / (device.reviewsnumber + 1)
                device.reviewsnumber = device.reviewsnumber + 1
                device.save()

                devicereview = DeviceReview.objects.create(device=device,user=user,score=score,content=content)

                context_dict['success'] = 1
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Device not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Search for a device
def device_search(request):
    context_dict = {}

    searchcontent = request.GET['searchcontent']

    list = []
    if searchcontent:
        # Get the device list whose name contain search content
        devices_list = Device.objects.filter(name__icontains=searchcontent)

        for ob in devices_list:
            dict = {}
            for attr in [f.name for f in ob._meta.fields]:
                if attr == 'picture1':
                    dict[attr] = getattr(ob, attr).url
                elif attr == 'picture2':
                    dict[attr] = getattr(ob, attr).url
                elif attr == 'picture3':
                    dict[attr] = getattr(ob, attr).url
                elif attr == 'devicedescription':
                    pass
                else:
                    dict[attr] = getattr(ob, attr)
            list.append(dict)

    context_dict['devices'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get game list
def games(request):
    games_list = Game.objects.all().order_by('-id')

    list = []

    for ob in games_list:
        dict = {}
        for attr in [f.name for f in ob._meta.fields]:
            if attr == 'picture1':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'picture2':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'picture3':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'gamedescription':
                pass
            else:
                dict[attr] = getattr(ob, attr)
        list.append(dict)


    context_dict = {}
    context_dict['games'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get detail of a specific game
def game_detail(request):
    context_dict = {}

    if request.method == 'GET':
        gameid = request.GET['gameid']

        try:
            game = Game.objects.get(id=gameid)

            game_dict = {}

            for attr in [f.name for f in game._meta.fields]:
                if attr == 'picture1':
                    game_dict[attr] = getattr(game, attr).url
                elif attr == 'picture2':
                    game_dict[attr] = getattr(game, attr).url
                elif attr == 'picture3':
                    game_dict[attr] = getattr(game, attr).url
                else:
                    game_dict[attr] = getattr(game, attr)

            context_dict['game'] = game_dict

            review_list = GameReview.objects.filter(game=game).order_by('-id')
            reviews = []

            for ob in review_list:
                review_dict = {}

                username = ob.user.username
                date = ob.date.strftime('%Y-%m-%d %H:%M:%S')
                content = ob.content
                score = ob.score

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.user)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                review_dict['username'] = username
                review_dict['picture'] = picture
                review_dict['date'] = date
                review_dict['content'] = content
                review_dict['score'] = score

                reviews.append(review_dict)

            context_dict['reviews'] = reviews

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Review on a game
@csrf_exempt
def game_review(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        gameid = request.POST.get('gameid')
        score = (int)(request.POST.get('score'))
        content = request.POST.get('content')

        try:
            user = User.objects.get(username=username)

            try:
                game = Game.objects.get(id=gameid)

                game.score = (game.score * game.reviewsnumber + score) / (game.reviewsnumber + 1)
                game.reviewsnumber = game.reviewsnumber + 1
                game.save()

                gamereview = GameReview.objects.create(game=game,user=user,score=score,content=content)

                context_dict['success'] = 1
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Game not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get video list
def videos(request):
    videos_list = Video.objects.all().order_by('-id')

    list = []

    for ob in videos_list:
        dict = {}
        for attr in [f.name for f in ob._meta.fields]:
            if attr == 'picture1':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'picture2':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'picture3':
                dict[attr] = getattr(ob, attr).url
            elif attr == 'videodescription':
                pass
            else:
                dict[attr] = getattr(ob, attr)
        list.append(dict)


    context_dict = {}
    context_dict['videos'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get detail of a specific video
def video_detail(request):
    context_dict = {}

    if request.method == 'GET':
        videoid = request.GET['videoid']

        try:
            video = Video.objects.get(id=videoid)

            video_dict = {}

            for attr in [f.name for f in video._meta.fields]:
                if attr == 'picture1':
                    video_dict[attr] = getattr(video, attr).url
                elif attr == 'picture2':
                    video_dict[attr] = getattr(video, attr).url
                elif attr == 'picture3':
                    video_dict[attr] = getattr(video, attr).url
                else:
                    video_dict[attr] = getattr(video, attr)

            context_dict['video'] = video_dict

            review_list = VideoReview.objects.filter(video=video).order_by('-id')
            reviews = []

            for ob in review_list:
                review_dict = {}

                username = ob.user.username
                date = ob.date.strftime('%Y-%m-%d %H:%M:%S')
                content = ob.content
                score = ob.score

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.user)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                review_dict['username'] = username
                review_dict['picture'] = picture
                review_dict['date'] = date
                review_dict['content'] = content
                review_dict['score'] = score

                reviews.append(review_dict)

            context_dict['reviews'] = reviews

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Review on a video
@csrf_exempt
def video_review(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        videoid = request.POST.get('videoid')
        score = (int)(request.POST.get('score'))
        content = request.POST.get('content')

        try:
            user = User.objects.get(username=username)

            try:
                video = Video.objects.get(id=videoid)

                video.score = (video.score * video.reviewsnumber + score) / (video.reviewsnumber + 1)
                video.reviewsnumber = video.reviewsnumber + 1
                video.save()

                videoreview = VideoReview.objects.create(video=video,user=user,score=score,content=content)

                context_dict['success'] = 1
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Video not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get feed list
def feeds(request):
    context_dict = {}

    if request.method == 'GET':
        feeds_list = []

        if "username" in request.GET:

            username = request.GET['username']
            try:
                user = User.objects.get(username=username)
                feeds_list = Feed.objects.filter(user=user).order_by('-id')
            except ObjectDoesNotExist:
                pass
        else:
            feeds_list = Feed.objects.all().order_by('-id')

        list = []

        for ob in feeds_list:
            dict = {}
            for attr in [f.name for f in ob._meta.fields]:
                if attr == 'user':
                    user = getattr(ob, attr)
                    userprofile = UserProfile.objects.get(user=user)

                    dict['username'] = user.username
                    dict['userpicture'] = userprofile.picture.url
                elif attr == 'picture':
                    dict[attr] = getattr(ob, attr).url
                elif attr == 'date':
                    dict[attr] = getattr(ob, attr).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    dict[attr] = getattr(ob, attr)
            list.append(dict)

        context_dict['feeds'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get feed list which posted by the users your are following
def feeds_following(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET['username']

        try:
            user = User.objects.get(username=username)
            following_list = Follow.objects.filter(user=user)

            followinguser_list = []
            for ob in following_list:
                followinguser_list.append(ob.followeduser)

            feeds_list = Feed.objects.filter(user__in=followinguser_list).order_by('-id')

            list = []

            for ob in feeds_list:
                dict = {}
                for attr in [f.name for f in ob._meta.fields]:
                    if attr == 'user':
                        user = getattr(ob, attr)
                        userprofile = UserProfile.objects.get(user=user)

                        dict['username'] = user.username
                        dict['userpicture'] = userprofile.picture.url
                    elif attr == 'picture':
                        dict[attr] = getattr(ob, attr).url
                    elif attr == 'date':
                        dict[attr] = getattr(ob, attr).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        dict[attr] = getattr(ob, attr)
                list.append(dict)

            context_dict['feeds'] = list

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get detail of a specific feed
def feed_detail(request):
    context_dict = {}

    if request.method == 'GET':
        feedid = request.GET['feedid']

        try:
            feed = Feed.objects.get(id=feedid)

            dict = {}

            for attr in [f.name for f in feed._meta.fields]:
                if attr == 'user':
                    user = getattr(feed, attr)
                    userprofile = UserProfile.objects.get(user=user)

                    dict['username'] = user.username
                    dict['userpicture'] = userprofile.picture.url
                elif attr == 'picture':
                    dict[attr] = getattr(feed, attr).url
                elif attr == 'date':
                    dict[attr] = getattr(feed, attr).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    dict[attr] = getattr(feed, attr)

            context_dict['feed'] = dict

            comment_list = FeedComment.objects.filter(feed=feed).order_by('-id')
            comments = []

            for ob in comment_list:
                comment_dict = {}

                username = ob.user.username
                date = ob.date.strftime('%Y-%m-%d %H:%M:%S')
                content = ob.content

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.user)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                comment_dict['username'] = username
                comment_dict['picture'] = picture
                comment_dict['date'] = date
                comment_dict['content'] = content

                comments.append(comment_dict)

            context_dict['comments'] = comments

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Comment on feed
@csrf_exempt
def feed_comment(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        feedid = request.POST.get('feedid')
        content = request.POST.get('content')

        try:
            user = User.objects.get(username=username)

            try:
                feed = Feed.objects.get(id=feedid)

                feed.commentsnumber = feed.commentsnumber + 1
                feed.save()

                feedcomment = FeedComment.objects.create(feed=feed,user=user,content=content)

                context_dict['success'] = 1
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Feed not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Like a feed
@csrf_exempt
def feed_like(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        feedid = request.POST.get('feedid')

        try:
            user = User.objects.get(username=username)

            try:
                feed = Feed.objects.get(id=feedid)

                # Check whether already liked this feed
                try:
                    feedlike = FeedLike.objects.get(feed=feed,user=user)

                    context_dict['success'] = 0
                    context_dict['error_message'] = 'Already liked'
                except ObjectDoesNotExist:
                    feed.likesnumber = feed.likesnumber + 1
                    feed.save()

                    feedlike = FeedLike.objects.create(feed=feed,user=user)

                    context_dict['success'] = 1
                    context_dict['likesnumber'] = feed.likesnumber
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Feed not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Add a feed
@csrf_exempt
def feed_add(request):
   context_dict = {}

   if request.method == 'POST':

       for key in request.POST:
           print(key)
       # Check form type
       # if has filename, then type is text plus picture
       # otherwise type is text
       if "isPic" in request.POST:
           form = FeedAddTextPlusPictureForm(request.POST, request.FILES)
           if form.is_valid():
               username = form.cleaned_data['username']

               try:
                   user = User.objects.get(username=username)
                   content = form.cleaned_data['content']
                   picture = form.cleaned_data['pic']

                   feed = Feed.objects.create(user=user,content=content,picture=picture)
                   context_dict['success'] = 1
               except ObjectDoesNotExist:
                   context_dict['success'] = 0
                   context_dict['error_message'] = 'User not exist.'
           else:
               context_dict['success'] = 0
               context_dict['error_message'] = 'Invalid data.'
       else:
           form = FeedAddTextForm(request.POST, request.FILES)
           if form.is_valid():
               username = form.cleaned_data['username']

               try:
                   user = User.objects.get(username=username)
                   content = form.cleaned_data['content']

                   feed = Feed.objects.create(user=user,content=content)
                   context_dict['success'] = 1
               except ObjectDoesNotExist:
                   context_dict['success'] = 0
                   context_dict['error_message'] = 'User not exist.'
           else:
               context_dict['success'] = 0
               context_dict['error_message'] = 'Invalid data.'

   else:
       context_dict['success'] = 0
       context_dict['error_message'] = 'Request Error.'

   return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Follow a user
@csrf_exempt
def follow(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        followedusername = request.POST.get('followedusername')

        try:
            user = User.objects.get(username=username)

            try:
                followeduser = User.objects.get(username=followedusername)

                try:
                    follow = Follow.objects.get(user=user,followeduser=followeduser)

                    context_dict['success'] = 0
                    context_dict['error_message'] = 'Already followed'
                except ObjectDoesNotExist:
                    follow = Follow.objects.create(user=user,followeduser=followeduser)

                    context_dict['success'] = 1
            except ObjectDoesNotExist:
                context_dict['success'] = 0
                context_dict['error_message'] = 'Followed user not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get the user list that you are following
def followings(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)

            following_list = Follow.objects.filter(user=user).order_by('-id')

            list = []

            for ob in following_list:
                following_dict = {}

                username = ob.followeduser.username

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.followeduser)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                following_dict['username'] = username
                following_dict['picture'] = picture

                list.append(following_dict)

            context_dict['followings'] = list

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

# Get the user list that following you
def followers(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)

            follower_list = Follow.objects.filter(followeduser=user).order_by('-id')

            list = []

            for ob in follower_list:
                follower_dict = {}

                username = ob.user.username

                picture = ''
                try:
                    userProfile = UserProfile.objects.get(user=ob.user)
                    picture = userProfile.picture.url
                except ObjectDoesNotExist:
                    pass

                follower_dict['username'] = username
                follower_dict['picture'] = picture

                list.append(follower_dict)

            context_dict['followers'] = list

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")