from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from iVR.models import User, UserProfile, Feed, News, Device, Video, Game
from iVR.models import FeedLike, FeedComment, NewsComment, DeviceReview, VideoReview, GameReview
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)

                context_dict['success'] = 0
                context_dict['error_message'] = 'User already exists.'

            except ObjectDoesNotExist:
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

@csrf_exempt
def login(request):
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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

def user_detail(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET['username']

        try:
            user = User.objects.get(username=username)
            userProfile = UserProfile.objects.get(user=user)

            feed_list = Feed.objects.filter(user=user).order_by('-id')

            user_dict = {}
            user_dict['username'] =getattr(user, 'username')
            user_dict['picture'] = getattr(userProfile, 'picture').url
            user_dict['feedsnumber'] = len(feed_list)

            context_dict['user'] = user_dict

        except ObjectDoesNotExist:
            pass

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

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

def news_comment(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET.get('username')
        newsid = request.GET.get('newsid')
        content = request.GET['content']

        try:
            user = User.objects.get(username=username)

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

def device_review(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET.get('username')
        deviceid = request.GET.get('deviceid')
        score = (int)(request.GET.get('score'))
        content = request.GET['content']

        try:
            user = User.objects.get(username=username)

            try:
                device = Device.objects.get(id=deviceid)

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

def game_review(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET.get('username')
        gameid = request.GET.get('gameid')
        score = (int)(request.GET.get('score'))
        content = request.GET['content']

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

def video_review(request):
    context_dict = {}

    if request.method == 'GET':
        username = request.GET.get('username')
        videoid = request.GET.get('videoid')
        score = (int)(request.GET.get('score'))
        content = request.GET['content']

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
                context_dict['error_message'] = 'video not exist.'

        except ObjectDoesNotExist:
            context_dict['success'] = 0
            context_dict['error_message'] = 'User not exist.'

    else:
        context_dict['success'] = 0
        context_dict['error_message'] = 'Request Error.'

    return HttpResponse(json.dumps(context_dict), content_type="application/json")

def feeds(request):
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


    context_dict = {}
    context_dict['feeds'] = list

    return HttpResponse(json.dumps(context_dict), content_type="application/json")
