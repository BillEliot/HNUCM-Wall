from django.db.models.fields import DateField
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files import File as F
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from .models import *
from utils.utils import *
import os, random, datetime, pytz, math, requests, hashlib, calendar, csv, string
import json


@csrf_exempt
def not_login(request):
    return JsonResponse({ 'code': 302, 'path': '/login' })



@csrf_exempt
def getBanners(request):
    data = []
    for banner in Banner.objects.all():
        data.append({
            'imageUrl': banner.imageUrl,
            'linkUrl': banner.linkUrl
        })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': data
    })



@csrf_exempt
def getCaptcha(request):
    receiver = request.GET.get('email')
    captcha = generateCaptcha()

    try:
        if sendCaptcha(receiver, captcha):
            request.session['captcha'] = captcha
            request.session.set_expiry(1800)
            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '发送失败, 请稍后重试或联系管理员' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getSMSCaptcha(request):
    pass



@csrf_exempt
def getPermissionGroupMembers(request):
    group = request.GET.get('group')

    try:
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': list(User.objects.filter(groups__name=group).values('id', 'username'))
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def register(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    bio = request.POST.get('bio')
    gender = request.POST.get('gender')
    _class = request.POST.get('class[0]') + '/' + request.POST.get('class[1]')
    last_name = request.POST.get('last_name') if request.POST.get('last_name') else ''
    first_name = request.POST.get('first_name') if request.POST.get('first_name') else ''
    #phone = request.POST.get('phone')
    qq = request.POST.get('qq')
    wechat = request.POST.get('wechat')
    captcha = request.POST.get('captcha')

    try:
        # check captcha
        session_captcha = request.session.get('captcha', None)
        if not session_captcha or captcha != session_captcha:
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '验证码错误或过期' })
        # check email
        if User.objects.filter(email=email).exists():
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '电子邮件已存在' })
        # check username
        if username == 'Anony' or username == 'anony':
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '非法昵称' })
        if User.objects.filter(username=username).exists():
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '昵称已存在' })
        
        User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            bio = bio,
            gender = gender,
            _class = _class,
            #phone = phone,
            qq = qq,
            wechat = wechat
        )

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



# Pending
@csrf_exempt
def registerWX(request):
    openid = requests.POST.get('openid')
    email = request.POST.get('email')
    password = request.POST.get('password')
    username = request.POST.get('username')
    bio = request.POST.get('bio')
    gender = requests.POST.get('gender')
    _class = request.POST.get('class')
    #phone = request.POST.get('phone')
    qq = request.POST.get('qq')
    wechat = request.POST.get('wechat')

    # check username
    if username == 'Anony' or username == 'anony':
        return HttpResponse(3)
    if User.objects.filter(username=username).exists():
        return HttpResponse(4)

    try:
        User.objects.create(
            openid = openid,
            email = email,
            password = password,
            username = username,
            bio = bio,
            _class = _class,
            #phone = phone,
            qq = qq,
            wechat = wechat
        )
        return HttpResponse(0)
    except:
        return HttpResponse(5)



@csrf_exempt
def loginView(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    isRemember = request.POST.get('isRemember')

    User_Agent = request.headers['User-Agent']
    if 'UE4' in User_Agent:
        ue_json = json.loads(request.body.decode('utf-8'))
        email = ue_json['email']
        password = ue_json['password']

    if (User.objects.filter(email=email).exists()):
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if isRemember:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)

            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '密码错误' })
    else:
        return JsonResponse({ 'code': 500 })



# Pending
@csrf_exempt
def loginWX(request):
    code = request.POST.get('code')

    query = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx432cc355bf1c49c4&secret=8610be32becb59dab068e5d1c31bb069&js_code=%s&grant_type=authorization_code' % code
    info = requests.get(query).json()
    openid = info['openid']
    try:
        user = User.objects.get(openid=openid)
        return JsonResponse({
            'openid': openid,
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar.url,
            'unreadCount': user.messages.filter(isRead=False).count(),
        })
    except:
        return JsonResponse({
            'openid': openid,
            'id': -1,
            'username': '赶快登陆吧～',
            'avatar': '/media/img/avatar/anony.jpg',
            'unreadCount': 0,
        })



@csrf_exempt
def logoutView(request):
    logout(request)
    return HttpResponse(0)



@csrf_exempt
def getUserBaseInfo(request):
    if request.user.is_authenticated:
        try:
            return JsonResponse({
                'code': 200,
                'status': 'success',
                'data': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'avatar': request.user.avatar.url,
                    'unreadCount': request.user.messages.filter(isRead=False).count(),
                    'isAdmin': request.user.is_staff
                }
            })
        except:
            return JsonResponse({ 'code': 500 })
    else:
        return JsonResponse({
                'code': 200,
                'status': 'success',
                'data': {
                    'id': -1,
                    'username': '赶快登陆吧～',
                    'avatar': '/media/img/avatar/anony.jpg',
                    'isAdmin': False
                }
            })



@csrf_exempt
def getUserProfile(request):
    _id = request.GET.get('id')

    try:
        user = User.objects.get(id=_id)
        # loves
        loves = []
        for love in Love.objects.filter(userFrom=user):
            # not anonymous
            if not love.isAnony:
                # registered
                set_userTo = love.userTo.all()

                uid = -1
                avatar = ''
                if set_userTo.count() == 1:
                    uid = set_userTo[0].id
                    avatar = set_userTo[0].avatar.url
                usernames = list(set_userTo.values_list('username', flat=True))

                # not registered
                usernames += love.nameTo.split(';')

                loves.append({
                    'id': love.id,
                    'userTo_id': uid,
                    'userTo_username': '/'.join(usernames),
                    'userTo_avatar': avatar,
                    'content': love.content,
                    'date': love.date
                })
        # loses
        loses = []
        for lose in Lose.objects.filter(user=user):
            loses.append({
                'id': lose.id,
                'isFound': lose.isFound,
                'name': lose.name,
                'description': lose.description,
                'date': lose.publicDate
            })
        # deals
        deals = []
        for deal in Deal.objects.filter(user=user):
            deals.append({
                'id': deal.id,
                'isSold': deal.isSold,
                'name': deal.name,
                'description': deal.description,
                'date': deal.date
            })
        # helps
        helps = []
        for _help in Help.objects.filter(user=user):
            helps.append({
                'id': _help.id,
                'title': _help.title,
                'content': _help.content,
                'date': _help.date
            })
        # articles
        articles = []
        for article in Article.objects.filter(user=user):
            if article.isAdopted:
                articles.append({
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'tags': article.tags.split(';'),
                    'neededCoin': article.neededCoin,
                    'publicDate': article.publicDate,
                    'editDate': article.editDate
                })
        # is following
        isFollowing = False
        if request.user.is_authenticated and request.user.id != _id:
            iisFollowing = user in request.user.followings.all()
        # following list
        followings = []
        for following in user.following.all():
            followings.append({
                'id': following.id,
                'username': following.username,
                'avatar': following.avatar.url,
                'bio': following.bio,
                'auth': following.auth.split(';') if following.auth else None,
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar.url,
                'email': user.email,
                'bio': user.bio,
                'phone': user.phone[:3] + '****' + user.phone[-4:] + '(已认证)' if user.phone else '未认证',
                'qq': user.qq,
                'wechat': user.wechat,
                'gender': user.gender,
                'class': user._class,
                'coin': user.coin,
                'auth': user.auth.split(';') if user.auth else None,
                'loves': loves,
                'loses': loses,
                'deals': deals,
                'helps': helps,
                'articles': articles,
                'isFollowing': isFollowing,
                'followings': followings
            }
        })
    except(User.DoesNotExist):
        return JsonResponse({ 'code': 400 })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def uploadAvatar(request):
    avatar = request.FILES.get('avatar')

    try:
        # Encode the filename if the platform is web
        name, suffix = avatar.name.split('.')
        avatar.name = formatName(name, suffix)

        if avatar:
            avatar_path = settings.BASE_DIR + '/media/img/avatar/' + avatar.name
            avatar_file = open(avatar_path, 'wb+')
            # save file
            for chunk in avatar.chunks():
                avatar_file.write(chunk)
            avatar_file.close()
            # remove original avatar
            if request.user.avatar.url != '/media/img/avatar/default.png' and os.path.exists(settings.BASE_DIR + request.user.avatar.url):
                os.remove(settings.BASE_DIR + request.user.avatar.url)
            request.user.avatar = 'img/avatar/' + avatar.name
            request.user.save()
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def bindWX(request):
    openid = request.POST.get('openid')
    email = request.POST.get('email')
    password = hashlib.new('md5', request.POST.get('password').encode('utf8')).hexdigest()
    
    try:
        user = User.objects.get(email=email)
        if user.password == password:
            user.openid = openid
            user.save()
            return JsonResponse({
                'openid': openid,
                'unreadCount': user.messages.filter(isRead=False).count(),
            })
        else:
            return HttpResponse(1)
    except:
        return HttpResponse(2)



@csrf_exempt
@login_required
def follow(request):
    id_follow = request.GET.get('ud')

    try:
        user_follow = User.objects.get(id=id_follow)
        if user_follow not in request.user.following.all():
            request.user.following.add(user_follow)
            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 400 })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def unFollow(request):
    id_follow = request.GET.get('id')

    try:
        user_follow = User.objects.get(id=id_follow)
        if user_follow in request.user.following.all():
            request.user.following.remove(user_follow)
            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 400 })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def checkBoundEMail(request):
    email = request.GET.get('email')

    try:
        if User.objects.filter(email=email).exists():
            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '邮箱不存在' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def updateUser(request):
    username = request.POST.get('username')
    bio = request.POST.get('bio')
    _class = request.POST.get('class')
    gender = request.POST.get('gender')
    qq = request.POST.get('qq')
    wechat = request.POST.get('wechat')

    try:
        request.user.username = username
        request.user.bio = bio
        request.user._class = _class
        request.user.gender = gender
        request.user.qq = qq
        request.user.wechat = wechat

        request.user.save()
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def changePassword(request):
    originPassword = request.POST.get('originPassword')
    password = request.POST.get('password')

    try:
        if request.user.check_password(originPassword):
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '密码错误' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def findpassword(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    captcha = request.POST.get('captcha')

    try:
        if captcha == request.session.get('captcha', None):
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return JsonResponse({ 'code': 200, 'status': 'success' })
        else:
            return JsonResponse({ 'code': 200, 'status': 'error', 'message': '验证码错误或过期' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getMessage(request):
    messageList = []
    try:
        for message in request.user.messages.all():
            messageList.append({
                'user': { 'id': message.user.id, 'username': message.user.username, 'bio': message.user.bio, 'avatar': message.user.avatar.url },
                'type': message._type,
                'from': message._from,
                'messageID': message.messageID,
                'commentContent': message.commentContent,
                'date': message.date
            })
            if not message.isRead:
                message.isRead = True
                message.save()
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': messageList
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def searchUser(request):
    user = request.GET.get('user')

    try:
        # username
        listusername = []
        for user in User.objects.filter(username__contains=user):
            listusername.append(user.username)
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listusername
        })
    except:
        return JsonResponse({ 'code': 500 })



# Pending
@csrf_exempt
def signUp(request):
    auth = request.POST.get('auth')
    
    try:
        if not request.user.auth:
            request.user.auth = auth
            request.user.save()
            return HttpResponse(0)
        elif auth not in request.user.auth:
            request.user.auth = request.user.auth + ';' + auth
            request.user.save()
            return HttpResponse(0)
        else:
            return HttpResponse(1)
    except:
        return HttpResponse(2)



@csrf_exempt
def canSign_JinGui(request):
    auth = '金匮打卡'

    try:
        if auth in request.user.auth:
            return HttpResponse(0)
        else:
            return HttpResponse(1)
    except:
        return HttpResponse(2)



@csrf_exempt
def IsFirstSignToday_JinGui(request):
    if not request.user.is_authenticated:
        return HttpResponse(1)

    try:
        today = datetime.datetime.now()
        date_1 = today.replace(hour=0, minute=0, second=0, microsecond=0)
        date_2 = date_1 + datetime.timedelta(days=1)

        JinGui = Activity_JinGui.objects.filter(date__range=[date_1, date_2]).filter(user=request.user)
        if JinGui.exists():
            return HttpResponse(JinGui[0].content)
        else:
            return HttpResponse('')
    except:
        return HttpResponse(2)



# Pending
@csrf_exempt
def sign_JinGui(request):
    content = request.POST.get('content')
    cover = request.POST.get('cover')
    if not cover == '':
        cover = 'img/JinGui/' + cover
    else:
        cover = 'img/JinGui/default.png'

    try:
        if content == '':
            return HttpResponse(1)
        else:
            today = datetime.datetime.now()
            date_1 = today.replace(hour=0, minute=0, second=0, microsecond=0)
            date_2 = date_1 + datetime.timedelta(days=1)

            if Activity_JinGui.objects.filter(date__range=[date_1, date_2]).filter(user=request.user).exists():
                jingui = Activity_JinGui.objects.filter(date__range=[date_1, date_2]).get(user=request.user)
                jingui.content = content
                jingui.cover = cover
                jingui.save()
            else:
                Activity_JinGui.objects.create(
                    user = request.user,
                    content = content,
                    cover = cover
                )
            return HttpResponse(0)
    except:
        return HttpResponse(2)



# Pending
@csrf_exempt
def getStatistics_JinGui(request):
    date = request.POST.get('date')
    
    if not date:
        today = datetime.datetime.now()
    else:
        today = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_1 = today.replace(hour=0, minute=0, second=0, microsecond=0)
    date_2 = date_1 + datetime.timedelta(days=1)

    listStatistics = []
    try:
        for item in Activity_JinGui.objects.filter(date__range=[date_1, date_2]):
            listStatistics.append({
                'user': { 'uid': item.user.id, 'avatar': item.user.avatar.url, 'username': item.user.username, 'bio': item.user.bio },
                'content': item.content,
                'cover': item.cover.url,
                'audio': item.audio.url,
                'date': item.date
            })
        return JsonResponse({ 'info': listStatistics })
    except:
        return HttpResponse(1)



# Pending
@csrf_exempt
def getStatistics_JinGui_unsign(request):
    date = request.POST.get('date')
    
    if not date:
        today = datetime.datetime.now()
    else:
        today = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_1 = today.replace(hour=0, minute=0, second=0, microsecond=0)
    date_2 = date_1 + datetime.timedelta(days=1)

    listStatistics_unsign = []
    try:
        for user in User.objects.all():
            if u'金匮打卡' in str(user.auth):
                if not Activity_JinGui.objects.filter(date__range=[date_1, date_2]).filter(user=user).exists():
                    listStatistics_unsign.append({
                        'uid': user.id,
                        'avatar': user.avatar.url,
                        'username': user.username,
                        'bio': user.bio
                    })
        return JsonResponse({ 'info': listStatistics_unsign })
    except:
        return HttpResponse(1)



# Pending
@csrf_exempt
def getSignStatus(request):
    uid = request.POST.get('uid')
    dates = request.POST.getlist('dates[]')

    signStatus = {}
    try:
        user = User.objects.get(id=uid)
        for date in dates:
            date_1 = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
            date_2 = date_1 + datetime.timedelta(days=1)

            if date_1 > datetime.datetime.today():
                signStatus[date] = -1
            elif Activity_JinGui.objects.filter(user=user).filter(date__range=[date_1, date_2]).exists():
                signStatus[date] = 1
            else:
                signStatus[date] = 0
        return JsonResponse({ 'info': signStatus })
    except:
        return HttpResponse(1)



@csrf_exempt
@login_required
def uploadImage(request):
    try:
        file_obj = request.FILES.get('image')
        name = formatName(file_obj.name, 'jpg')
        directory = request.POST.get('directory')

        f = open(generateUploadPath('/img/' + directory, name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'url': '/media/img/' + directory + '/' + name,
                'name': name
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeImage(request):
    name = request.GET.get('name')
    directory = request.GET.get('directory')

    try:
        os.remove(settings.BASE_DIR + '/media/img/' + directory + '/' + name)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def uploadImg_markdown(request):
    try:
        file_obj = request.FILES.get('image')
        name = formatName(file_obj.name, 'jpg')
        f = open(generateUploadPath('/img/markdown/', name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        return JsonResponse({ 'code': 200, 'status': 'success', 'data': '/media/img/markdown/' + name })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeImg_markdown(request):
    url = request.POST.get('url')
    url = '/media/img/markdown/' + url[url.rfind('/')+1:]

    try:
        os.remove(settings.BASE_DIR + url)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def uploadImg_JinGui(request):
    file_obj = request.FILES.get('image')
    name = formatName(file_obj.name, 'jpg')
    f = open(generateUploadPath('/img/JinGui/', name), 'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse(name)



# Pending
@csrf_exempt
def removeImg_JinGui(request):
    url = request.POST.get('url')
    url = '/media/img/JinGui/' + url[url.rfind('/')+1:]

    try:
        os.remove(settings.BASE_DIR + url)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def uploadAudio_JinGui(request):
    try:
        # Get the audio
        file_obj = request.FILES.get('audio')
        name = formatName(file_obj.name, 'mp3')
        f = open(generateUploadPath('/audio/JinGui/', name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        # Sign
        today = datetime.datetime.now()
        date_1 = today.replace(hour=0, minute=0, second=0, microsecond=0)
        date_2 = date_1 + datetime.timedelta(days=1)

        if Activity_JinGui.objects.filter(date__range=[date_1, date_2]).filter(user=request.user).exists():
            jingui = Activity_JinGui.objects.filter(date__range=[date_1, date_2]).get(user=request.user)
            # remove the last audio
            if os.path.exists(settings.BASE_DIR + jingui.audio.url):
                os.remove(settings.BASE_DIR + jingui.audio.url)
            jingui.audio = 'audio/JinGui/' + name
            jingui.save()
        else:
            jingui = Activity_JinGui.objects.create(user=request.user)
            jingui.audio = 'audio/JinGui/' + name
            jingui.save()

        return HttpResponse(name)
    except:
        return HttpResponse(1)



# Pending
@csrf_exempt
def detail_JinGui(request):
    uid = request.GET.get('uid', None)
    if not uid:
        return HttpResponse(1)
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d')

    date_1 = date.replace(hour=0, minute=0, second=0, microsecond=0)
    date_2 = date_1 + datetime.timedelta(days=1)
    try:
        user = User.objects.get(id=uid)
        JinGui = Activity_JinGui.objects.filter(date__range=[date_1, date_2]).get(user=user)
        return JsonResponse({
            'user': { 'uid': user.id, 'username': user.username, 'bio': user.bio, 'avatar': user.avatar.url, 'auth': user.auth.split(';') if user.auth else None },
            'content': JinGui.content,
            'audio': JinGui.audio.url,
            'date': JinGui.date
        })
    except:
        return HttpResponse(2)



@csrf_exempt
def searchLoveItem(request):
    name = request.GET.get('name')
    _object = request.GET.get('object')

    loves = []
    listLove = []
    try:
        if _object == 'from':
            loves = Love.objects.filter(userFrom__username__contains=name)
        elif _object == 'to':
            loves = Love.objects.filter(userTo__username__contains=name) | Love.objects.filter(nameTo__contains=name)

        for love in loves:
            # cover
            cover = Image.objects.filter(love=love).first().image.url
            # userFrom
            if love.isAnony and _object == 'from':
                continue
            elif love.isAnony and _object == 'to':
                userFromID = -1
                userFromusername = 'Anony'
                userFromAvatar = '/media/img/avatar/anony.jpg'
                userFromBio = 'TA匿名了呢～'
            else:
                userFromID = love.userFrom.id
                userFromusername = love.userFrom.username
                userFromAvatar = love.userFrom.avatar.url
                userFromBio = love.userFrom.bio
            # userTo
            userTos = list(love.userTo.values('id', 'username', 'avatar', 'bio'))
            for user in love.nameTo.split(';'):
                userTos.append({
                    'id': -1,
                    'username': user,
                    'avatar': 'img/avatar/anony.jpg',
                    'bio': 'TA还没有来呢～'
                })
            # is thumbsUp
            if request.user.is_authenticated:
                isThumbsUp = request.user in love.thumbsUpUser.all()
            else:
                isThumbsUp = False
            
            listLove.append({
                'id': love.id,
                'userFrom_id': userFromID,
                'userFrom_username': userFromusername,
                'userFrom_avatar': userFromAvatar,
                'userFrom_bio': userFromBio,
                'userTo': userTos,
                'content': love.content,
                'cover': cover,
                'thumbsUp': love.thumbsUpUser.count(),
                'comments': Comment.objects.filter(love=love).count(),
                'isThumbsUp': isThumbsUp
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listLove
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchLoseItem(request):
    name = request.GET.get('name')

    listLose = []
    try:
        for lose in Lose.objects.filter(name__contains=name):
            # cover
            cover = Image.objects.filter(lose=lose).first().image.url
            listLose.append({
                'id': lose.id,
                'isFound': lose.isFound,
                'avatar': lose.user.avatar.url,
                'publicDate': lose.publicDate,
                'loseDate': lose.loseDate,
                'name': lose.name,
                'description': lose.description,
                'cover': cover
            })
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listLose
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchDealItem(request):
    name = request.GET.get('name')

    listDeal = []
    try:
        for deal in Deal.objects.filter(name__contains=name):
            # cover
            cover = Image.objects.filter(deal=deal).first().image.url
            listDeal.append({
                'id': deal.id,
                'isSold': deal.isSold,
                'user': {
                    'id': deal.user.id,
                    'username': deal.user.username,
                    'avatar': deal.user.avatar.url
                },
                'name': deal.name,
                'price': deal.price,
                'new': deal.new,
                'description': deal.description,
                'cover': cover
            })
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listDeal
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchArticle(request):
    name = request.GET.get('value')
    page_number = request.GET.get('page_number')

    listArticle = []
    try:
        page = Paginator(Article.objects.filter(title__contains=name), 10)
        for article in page.page(page_number).object_list:
            if article.isAdopted:
                listArticle.append({
                    'id': article.id,
                    'user': { 'id': article.user.id, 'avatar': article.user.avatar.url, 'username': article.user.username, 'bio': article.user.bio, 'auth': article.user.auth.split(';') if article.user.auth else None },
                    'title': article.title,
                    'tags': article.tags.split(';'),
                    'content': article.content[:50] + '...' if len(article.content) > 50 else article.content,
                    'neededCoin': article.neededCoin,
                    'publicDate': article.publicDate,
                    'editDate': article.editDate,
                    'comments': Comment.objects.filter(article=article).count(),
                    'thumbsUp': article.thumbsUpUser.count(),
                })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'list': listArticle,
                'total': page.count
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchArticleByUser(request):
    username = request.GET.get('value')
    page_number = request.GET.get('page_number')

    listArticle = []
    try:
        page = Paginator(Article.objects.filter(user__username__contains=username), 10)
        for article in page.page(page_number).object_list:
            if article.isAdopted:
                listArticle.append({
                    'id': article.id,
                    'user': { 'id': article.user.id, 'avatar': article.user.avatar.url, 'username': article.user.username, 'bio': article.user.bio, 'auth': article.user.auth.split(';') if article.user.auth else None },
                    'title': article.title,
                    'tags': article.tags.split(';'),
                    'content': article.content[:50] + '...' if len(article.content) > 50 else article.content,
                    'neededCoin': article.neededCoin,
                    'publicDate': article.publicDate,
                    'editDate': article.editDate,
                    'comments': Comment.objects.filter(article=article).count(),
                    'thumbsUp': article.thumbsUpUser.count(),
                })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'list': listArticle,
                'total': page.count
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchArticleByTag(request):
    tags = request.GET.getlist('value[]')
    page_number = request.GET.get('page_number')

    allArticles = Article.objects.all()
    for tag in tags:
        allArticles = allArticles.filter(tags__contains=tag)

    listArticle = []
    try:
        page = Paginator(allArticles, 10)
        for article in page.page(page_number).object_list:
            if article.isAdopted:
                listArticle.append({
                    'id': article.id,
                    'user': { 'id': article.user.id, 'avatar': article.user.avatar.url, 'username': article.user.username, 'bio': article.user.bio, 'auth': article.user.auth.split(';') if article.user.auth else None },
                    'title': article.title,
                    'tags': article.tags.split(';'),
                    'content': article.content[:50] + '...' if len(article.content) > 50 else article.content,
                    'neededCoin': article.neededCoin,
                    'publicDate': article.publicDate,
                    'editDate': article.editDate,
                    'comments': Comment.objects.filter(article=article).count(),
                    'thumbsUp': article.thumbsUpUser.count(),
                })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'list': listArticle,
                'total': page.count
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitLove(request):
    _id = request.POST.get('id')
    isEdit = request.POST.get('isEdit')
    isAnony = True if request.POST.get('isAnony') == 'true' else False
    userTos = request.POST.getlist('userTo[]')
    content = request.POST.get('content')
    images = request.POST.getlist('images[]')

    try:
        # get userTo
        listUserTo = []
        nameTo = ''
        for userTo in userTos:
            user = User.objects.filter(username=userTo)
            if user.exists():
                listUserTo.append(user[0])
            else:
                if len(nameTo) == 0:
                    nameTo = userTo
                else:
                    nameTo = nameTo + userTo + ';'

        # create or modify
        if isEdit:
            love = Love.objects.get(id=_id)
            if request.user != love.userFrom:
                return JsonResponse({ 'code': 403 })

            love.isAnony = isAnony
            love.nameTo = nameTo
            love.content = content

            love.userTo.clear()
            Image.objects.filter(love=love).delete()
            love.save()
        else:
            love = Love.objects.create(
                isAnony=isAnony,
                userFrom=request.user,
                nameTo=nameTo,
                content=content
            )
        # userTos
        for userTo in listUserTo:
            love.userTo.add(userTo)
        # images
        for image in images:
            Image.objects.create(
                image = 'img/wall/' + image,
                love = love
            )

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeLove(request):
    _id = request.GET.get('id')

    try:
        love = Love.objects.get(id=_id)
        if love.userFrom != request.user:
            return JsonResponse({ 'code': 403 })
        else:
            love.delete()
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitLose(request):
    _id = request.POST.get('id')
    isEdit = request.POST.get('isEdit')
    loseDate = request.POST.get('loseDate')
    name = request.POST.get('name')
    description = request.POST.get('description')
    images = request.POST.getlist('images[]')

    try:
        if isEdit:
            lose = Lose.objects.get(id=_id)
            if request.user != lose.user:
                return JsonResponse({ 'code': 403 })

            lose.loseDate = loseDate
            lose.name = name
            lose.description = description

            Image.objects.filter(lose=lose).delete()
            lose.save()
        else:
            lose = Lose.objects.create(
                user = request.user,
                loseDate=loseDate,
                name=name,
                description=description
            )
        
        for image in images:
            Image.objects.create(
                image = 'img/wall/' + image,
                lose = lose
            )

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeLose(request):
    _id = request.GET.get('id')

    try:
        lose = Lose.objects.get(id=_id)
        if lose.user != request.user:
            return JsonResponse({ 'code': 403 })
        else:
            lose.delete()
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitDeal(request):
    _id = request.POST.get('id')
    isEdit = request.POST.get('isEdit')
    name = request.POST.get('name')
    price = request.POST.get('price')
    new = request.POST.get('new')
    description = request.POST.get('description')
    images = request.POST.getlist('images[]')

    try:
        if isEdit:
            deal = Deal.objects.get(id=_id)
            if request.user != deal.user:
                return JsonResponse({ 'code': 403 })

            deal.name = name
            deal.price = price
            deal.new = new
            deal.description = description
            
            Image.objects.filter(deal=deal).delete()
            deal.save()
        else:
            deal = Deal.objects.create(
                user = request.user,
                name = name,
                price = price,
                new = new,
                description = description
            )

        for image in images:
            Image.objects.create(
                image = 'img/wall/' + image,
                deal = deal
            )
        
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBankUpdateMessage(requests):
    messages = []
    for message in Bank_UpdateMessage.objects.all():
        messages.append(message.date.strftime("%Y-%m-%d %H:%M:%S") + '-' + message.content)

    return JsonResponse({ 'info': messages })



@csrf_exempt
def getBankSubjects(requests):
    subjects = []
    try:
        for subject in Bank_Subject.objects.all():
            tempSubject = {
                'key': subject.name,
                'subjectType': subject.subjectType
            }
            tempChapter = []
            for chapter in Bank_Chapter.objects.filter(subject=subject):
                tempChapter.append({
                    'key': str(chapter.id),
                    'title': chapter.name,
                    'isTestPaper': chapter.isTestPaper
                })
            tempSubject['chapters'] = tempChapter
            subjects.append(tempSubject)
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': subjects
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitBank(request):
    _type = request.POST.get('type')
    chapters = request.POST.getlist('chapters[]')
    numQuestion = int(request.POST.get('numQuestion'))
    freSingleA = float(request.POST.get('singleA')) / 100.0
    freSingleB = float(request.POST.get('singleB')) / 100.0
    freMultiple = float(request.POST.get('multiple')) / 100.0
    freBlank = float(request.POST.get('blank')) / 100.0
    freJudge = float(request.POST.get('judge')) / 100.0
    freTerm = float(request.POST.get('term')) / 100.0
    freQA = float(request.POST.get('qa')) / 100.0
    freCase = float(request.POST.get('case')) / 100.0
    
    questions_singleA = []
    questions_singleB = []
    questions_multiple = []
    questions_blank = []
    questions_judge = []
    questions_term = []
    questions_qa = []
    questions_case = []
    try:
        if _type == 'total':
            for chapter in chapters:
                allQuestions = Bank_Chapter.objects.get(id=int(chapter)).bank_set.all()
                singleA = allQuestions.filter(questionType='singleA')
                singleB = allQuestions.filter(questionType='singleB')
                multiple = allQuestions.filter(questionType='multiple')
                blank = allQuestions.filter(questionType='blank')
                judge = allQuestions.filter(questionType='judge')
                term = allQuestions.filter(questionType='term')
                qa = allQuestions.filter(questionType='qa')
                case = allQuestions.filter(questionType='case')

                questions_singleA.extend(list(singleA.values()[0:int(singleA.count()*freSingleA)]))
                questions_singleB.extend(list(singleB.values()[0:int(singleB.count()*freSingleB)]))
                questions_multiple.extend(list(multiple.values()[0:int(multiple.count()*freMultiple)]))
                questions_blank.extend(list(blank.values()[0:int(blank.count()*freBlank)]))
                questions_judge.extend(list(judge.values()[0:int(judge.count()*freJudge)]))
                questions_term.extend(list(term.values()[0:int(term.count()*freTerm)]))
                questions_qa.extend(list(qa.values()[0:int(qa.count()*freQA)]))
                questions_case.extend(list(case.values()[0:int(case.count()*freCase)]))
        elif _type == 'random':
            for index, chapter in enumerate(chapters):
                allQuestions = Bank_Chapter.objects.get(id=int(chapter)).bank_set.all()
                if index == 0:
                    singleA = allQuestions.filter(questionType='singleA')
                    singleB = allQuestions.filter(questionType='singleB')
                    multiple = allQuestions.filter(questionType='multiple')
                    blank = allQuestions.filter(questionType='blank')
                    judge = allQuestions.filter(questionType='judge')
                    term = allQuestions.filter(questionType='term')
                    qa = allQuestions.filter(questionType='qa')
                    case = allQuestions.filter(questionType='case')
                else:
                    singleA = singleA | allQuestions.filter(questionType='singleA')
                    singleB = singleB | allQuestions.filter(questionType='singleB')
                    multiple = multiple | allQuestions.filter(questionType='multiple')
                    blank = blank | allQuestions.filter(questionType='blank')
                    judge = judge | allQuestions.filter(questionType='judge')
                    term = term | allQuestions.filter(questionType='term')
                    qa = qa | allQuestions.filter(questionType='qa')
                    case = case | allQuestions.filter(questionType='case')
            # random all questions
            singleA = list(singleA.values())
            singleB = list(singleB.values())
            multiple = list(multiple.values())
            blank = list(blank.values())
            judge = list(judge.values())
            term = list(term.values())
            qa = list(qa.values())
            case = list(case.values())

            random.shuffle(singleA)
            random.shuffle(singleB)
            random.shuffle(multiple)
            random.shuffle(blank)
            random.shuffle(judge)
            random.shuffle(term)
            random.shuffle(qa)
            random.shuffle(case)

            questions_singleA.extend(singleA[0:math.ceil(numQuestion*freSingleA)])
            questions_singleB.extend(singleB[0:math.ceil(numQuestion*freSingleB)])
            questions_multiple.extend(multiple[0:math.ceil(numQuestion*freMultiple)])
            questions_blank.extend(blank[0:math.ceil(numQuestion*freBlank)])
            questions_judge.extend(judge[0:math.ceil(numQuestion*freJudge)])
            questions_term.extend(term[0:math.ceil(numQuestion*freTerm)])
            questions_qa.extend(qa[0:math.ceil(numQuestion*freQA)])
            questions_case.extend(case[0:math.ceil(numQuestion*freCase)])

        # remove answers
        for question in questions_singleA:
            question['answer'] = ''
        for question in questions_singleB:
            question['answer'] = ''
        for question in questions_multiple:
            question['answer'] = ''
        for question in questions_blank:
            question['answer'] = ''
        for question in questions_judge:
            question['answer'] = ''
        for question in questions_term:
            question['answer'] = ''
        for question in questions_qa:
            question['answer'] = ''
        for question in questions_case:
            question['answer'] = ''

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'singleA': questions_singleA,
                'singleB': questions_singleB,
                'multiple': questions_multiple,
                'blank': questions_blank,
                'judge': questions_judge,
                'term': questions_term,
                'qa': questions_qa,
                'case': questions_case
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def handExam(request):
    subject = request.POST.get('subject')

    questions = json.loads(request.body.decode('utf8')) # Compatible with 3.5 or lower
    singleA = questions['singleA']
    singleB = questions['singleB']
    multiple = questions['multiple']
    judge = questions['judge']
    blank = questions['blank']
    term = questions['term']
    qa = questions['qa']
    case = questions['case']
    subject = questions['subject']

    allQuestions = len(singleA) + len(singleB) + len(multiple) + len(judge) + len(blank) + len(term) + len(qa) + len(case)
    correctQuestions = 0
    try:
        for question in singleA:
            answer = Bank.objects.get(id=question['id']).answer
            if answer == question['answer']:
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in singleB:
            answer = Bank.objects.get(id=question['id']).answer
            if answer == ''.join(question['answer']):
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in multiple:
            answer = Bank.objects.get(id=question['id']).answer
            question['answer'].sort()
            if answer == ''.join(question['answer']):
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in judge:
            answer = Bank.objects.get(id=question['id']).answer
            if answer == str(question['answer']):
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
                if answer == 'True':
                    question['correctAnswer'] = True
                else:
                    question['correctAnswer'] = False
        for question in blank:
            answer = Bank.objects.get(id=question['id']).answer
            if Bank.objects.get(id=question['id']).isBlankSeq:
                if answer == ';'.join(question['answer']):
                    question['isCorrect'] = True
                    correctQuestions += 1
                else:
                    question['isCorrect'] = False
                    question['correctAnswer'] = answer
            else:
                temp = True
                for correctAnswer in answer.split(';'):
                    if not correctAnswer in question['answer']:
                        question['isCorrect'] = False
                        temp = False
                        question['correctAnswer'] = answer
                        break
                if temp == True:
                    question['isCorrect'] = True
                    correctQuestions += 1
        for question in term:
            answer = Bank.objects.get(id=question['id']).answer
            if question['answer'] != '':
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
            question['correctAnswer'] = answer
        for question in qa:
            answer = Bank.objects.get(id=question['id']).answer
            if question['answer'] != '':
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
            question['correctAnswer'] = answer
        for question in case:
            answer = Bank.objects.get(id=question['id']).answer
            if question['answer'] != '':
                question['isCorrect'] = True
                correctQuestions += 1
            else:
                question['isCorrect'] = False
            question['correctAnswer'] = answer
        # Statistical Results
        Bank_Statistics.objects.create(
            user=request.user,
            subject=subject,
            allQuestions=allQuestions,
            correctQuestions=correctQuestions
        )

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'singleA': singleA,
                'singleB': singleB,
                'multiple': multiple,
                'judge': judge,
                'blank': blank,
                'term': term,
                'qa': qa,
                'case': case,
                'allQuestions': allQuestions,
                'correctQuestions': correctQuestions
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def saveBankResult(request):
    subject = request.POST.get('subject')
    json_serialization = request.POST.get('json_serialization')
    allQuestions = int(request.POST.get('allQuestions'))
    correctQuestions = int(request.POST.get('correctQuestions'))

    try:
        Bank_Result.objects.create(
            user = request.user,
            subject = Bank_Subject.objects.get(name=subject),
            json_serialization = json_serialization,
            allQuestions = allQuestions,
            correctQuestions = correctQuestions
        )
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getBankResult(request):
    try:
        _list = []
        for result in Bank_Result.objects.filter(user=request.user):
            _list.append({
                'id': result.id,
                'subject': result.subject.name,
                'json_serialization': result.json_serialization,
                'correctQuestions': result.correctQuestions,
                'allQuestions': result.allQuestions,
                'date': result.date
            })
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': _list
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeBankResult(request):
    _id = request.GET.get('id')

    try:
        Bank_Result.objects.get(id=_id).delete()
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def clearBankResult(request):
    try:
        Bank_Result.objects.filter(user=request.user).delete()

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBriefBankStatistics(request):
    briefBankStatisticsList = []

    for statistics in Bank_Statistics.objects.all()[:5]:
        briefBankStatisticsList.append({
            'user': { 'username': statistics.user.username },
            'subject': statistics.subject,
            'allQuestions': statistics.allQuestions,
            'correctQuestions': statistics.correctQuestions
        })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': briefBankStatisticsList
    })



@csrf_exempt
def getBankStatistics(request):
    bankStatisticsList = []

    for statistics in Bank_Statistics.objects.all():
        bankStatisticsList.append({
            'key': statistics.id,
            'user': { 'id': statistics.user.id, 'username': statistics.user.username },
            'subject': statistics.subject,
            'allQuestions': statistics.allQuestions,
            'correctQuestions': statistics.correctQuestions,
            'date': statistics.date.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': bankStatisticsList
    })



@csrf_exempt
def searchQuestion(request):
    title = request.GET.get('title')
    questions = []

    answer = ''
    try:
        for question in Bank.objects.filter(title__contains=title):
            if question.questionType == 'singleA' or question.questionType == 'singleB':
                if question.answer == 'A':
                    answer = question.A
                elif question.answer == 'B':
                    answer = question.B
                elif question.answer == 'C':
                    answer = question.C
                elif question.answer == 'D':
                    answer = question.D
                elif question.answer == 'E':
                    answer = question.E
            elif question.questionType == 'multiple':
                for ans in question.answer:
                    if ans == 'A':
                        answer = answer + question.A + '——'
                    elif ans == 'B':
                        answer = answer + question.B + '——'
                    elif ans == 'C':
                        answer = answer + question.C + '——'
                    elif ans == 'D':
                        answer = answer + question.D + '——'
                    elif ans == 'E':
                        answer = answer + question.E + '——'
                answer = answer[:-2]
            elif question.questionType == 'judge':
                if question.answer == 'True':
                    answer = '正确'
                else:
                    answer = '错误'
            else:
                answer = question.answer

            questions.append({
                'id': question.id,
                'title': question.title,
                'chapter': question.chapter.name,
                'subject': question.chapter.subject.name,
                'answer': answer
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': questions
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getErrorBook(request):
    try:
        errorBook = []
        for bank in request.user.errorBook.all():
            errorBook.append({
                'id': bank.id,
                'title': bank.title,
                'A': bank.A,
                'B': bank.B,
                'C': bank.C,
                'D': bank.D,
                'E': bank.E,
                'questionType': bank.questionType,
                'answer': bank.answer,
                'subject': bank.chapter.subject.name,
                'chapter': bank.chapter.name
            })
        return JsonResponse({ 'code': 200, 'status': 'success', 'data': errorBook })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def addErrorBook(request):
    _id = request.GET.get('id')

    try:
        bank = Bank.objects.get(id=_id)

        if request.user.errorBook.filter(id=_id).exists():
            return JsonResponse({ 'code': 200, 'status': 'warning', 'message': '这道题目已经在错题本中了，请前往【错题本】查看' })
        else:
            request.user.errorBook.add(bank)
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeErrorBook(request):
    _id = request.GET.get('id')

    try:
        bank = Bank.objects.get(id=_id)

        if request.user.errorBook.filter(id=_id).exists():
            request.user.errorBook.remove(bank)
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def clearErrorBook(request):
    try:
        request.user.errorBook.clear()

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getFileSubjects(request):
    subjects = []
    for subject in File_Subject.objects.all():
        subjects.append({
            'name': subject.name,
            'subjectType': subject.subjectType
        })
    
    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': subjects
    })



@csrf_exempt
def getFileList(request):
    subject = request.GET.get('subject')
    keyword = request.GET.get('keyword')

    fileList = []
    fileSize = 0
    try:
        for file in File.objects.filter(subject=File_Subject.objects.get(name=subject)).filter(name__contains=keyword):

            with open(settings.BASE_DIR + file._file.url, 'r') as f:
                ff = F(f)
                fileSize = ff.size

            fileList.append({
                'id': file.id,
                'name': file.name,
                'url': file._file.url,
                'type': file._type,
                'size': sizeFormat(fileSize),
                'sizeSort': fileSize,
                'date': file.date,
                'downloadCount': file.downloadCount,
                'viewCount': file.viewCount
            })
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': fileList
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def addFileViewCount(request):
    _id = request.GET.get('id')

    f = File.objects.get(id=_id)
    f.viewCount += 1
    f.save()

    return JsonResponse({ 'code': 200, 'status': 'success' })



@csrf_exempt
def addFileDownloadCount(request):
    _id = request.GET.get('id')

    f = File.objects.get(id=_id)
    f.downloadCount += 1
    f.save()

    return JsonResponse({ 'code': 200, 'status': 'success' })



@csrf_exempt
@login_required
def submitArticle(request):
    _id = request.POST.get('id')
    isEdit = request.POST.get('isEdit')
    title = request.POST.get('title')
    tags = request.POST.getlist('tags[]')
    content = request.POST.get('content')
    neededCoin = request.POST.get('neededCoin')

    try:
        if isEdit:
            article = Article.objects.get(id=_id)
            if article.user != request.user:
                return JsonResponse({ 'code': 403 })

            article.title = title
            article.tags = ';'.join(tags)
            article.content = content
            article.neededCoin = neededCoin
            article.save()
        else:
            Article.objects.create(
                user = request.user,
                title = title,
                tags = ';'.join(tags),
                content = content,
                neededCoin = neededCoin
            )
        
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeArticle(request):
    _id = request.GET.get('id')

    try:
        article = Article.objects.get(id=_id)
        if article.user != request.user:
            return JsonResponse({ 'code': 403 })
        else:
            article.delete()
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitHelp(request):
    _id = request.POST.get('id')
    isEdit = request.POST.get('isEdit')
    title = request.POST.get('title')
    content = request.POST.get('content')

    try:
        if isEdit:
            _help = Help.objects.get(id=_id)
            _help.title = title
            _help.content = content
            _help.save()
        else:
            Help.objects.create(
                user = request.user,
                title = title,
                content = content
            )
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeHelp(request):
    _id = request.GET.get('id')

    try:
        _help = Help.objects.get(id=_id)
        if _help.user != request.user:
            return JsonResponse({ 'code': 403 })
        else:
            _help.delete()
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBriefWallList(request):
    loves = Love.objects.values('id', 'content', 'date')
    loses = Lose.objects.values('id', 'description', 'publicDate')
    deals = Deal.objects.values('id', 'description', 'date')
    helps = Help.objects.values('id', 'content', 'date')

    index_love = 0
    index_lose = 0
    index_deal = 0
    index_help = 0

    listWall = []
    for i in range(5):
        latestDate = max(
            loves[index_love]['date'] if index_love < len(loves) else datetime.datetime(1970, 1, 1, 8, 0, 0, 0),
            loses[index_lose]['publicDate'] if index_lose < len(loses) else datetime.datetime(1970, 1, 1, 8, 0, 0, 0),
            deals[index_deal]['date'] if index_deal < len(deals) else datetime.datetime(1970, 1, 1, 8, 0, 0, 0),
            helps[index_help]['date'] if index_help < len(helps) else datetime.datetime(1970, 1, 1, 8, 0, 0, 0),
        )
        if index_love < len(loves) and latestDate == loves[index_love]['date']:
            listWall.append({
                'type': 'love',
                'id': loves[index_love]['id'],
                'content': loves[index_love]['content'][:10] + '...' if len(loves[index_love]['content']) > 10 else loves[index_love]['content']
            })
            index_love += 1
        elif index_lose < len(loses) and latestDate == loses[index_lose]['publicDate']:
            listWall.append({
                'type': 'lose',
                'id': loses[index_lose]['id'],
                'content': loses[index_lose]['description'][:10] + '...' if len(loses[index_lose]['description']) > 10 else loses[index_lose]['description']
            })
            index_lose += 1
        elif index_deal < len(deals) and latestDate == deals[index_deal]['date']:
            listWall.append({
                'type': 'deal',
                'id': deals[index_deal]['id'],
                'content': deals[index_deal]['description'][:10] + '...' if len(deals[index_deal]['description']) > 10 else deals[index_deal]['description']
            })
            index_deal += 1
        elif index_help < len(helps) and latestDate == helps[index_help]['date']:
            listWall.append({
                'type': 'help',
                'id': helps[index_help]['id'],
                'content': helps[index_help]['content'][:10] + '...' if len(helps[index_help]['content']) > 10 else helps[index_help]['content']
            })
            index_help += 1
    
    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': listWall
    })



@csrf_exempt
def getLoveList(request):
    filterType = request.GET.get('filterType')
    order = request.GET.get('order')
    page_number = int(request.GET.get('page_number'))

    try:
        listLove = []
        if filterType == 'date':
            if order == 'positive':
                page = Paginator(Love.objects.order_by('date'), 10)
            elif order == 'reverse':
                page = Paginator(Love.objects.order_by('-date'), 10)
        elif filterType == 'thumbsUp':
            if order == 'positive':
                page = Paginator(Love.objects.annotate(numThumbsUp = Count('thumbsUpUser')).order_by('numThumbsUp'), 10)
            elif order == 'reverse':
                page = Paginator(Love.objects.annotate(numThumbsUp = Count('thumbsUpUser')).order_by('-numThumbsUp'), 10)
        else:
            page = Paginator(Love.objects.all(), 10)

        if page_number > page.num_pages or page.count == 0:
            return JsonResponse({ 'code': 200, 'status': 'none' })

        # top
        if page_number == 1:
            top_love = Love.objects.filter(isTop=True).first()
            if top_love:
                # userFrom
                if top_love.isAnony:
                    userFromID = -1
                    userFromusername = 'Anony'
                    userFromAvatar = '/media/img/avatar/anony.jpg'
                    userFromBio = 'TA匿名了呢～'
                else:
                    userFromID = top_love.userFrom.id
                    userFromusername = top_love.userFrom.username
                    userFromAvatar = top_love.userFrom.avatar.url
                    userFromBio = top_love.userFrom.bio
                # userTo
                userTos = list(top_love.userTo.values('id', 'username', 'avatar', 'bio'))
                if top_love.nameTo:
                    for user in top_love.nameTo.split(';'):
                        userTos.append({
                            'id': -1,
                            'username': user,
                            'avatar': 'img/avatar/anony.jpg',
                            'bio': 'TA还没有来呢～'
                        })
                # is thumbsUp
                if request.user.is_authenticated:
                    isThumbsUp = request.user in top_love.thumbsUpUser.all()
                else:
                    isThumbsUp = False

                top = {
                    'id': top_love.id,
                    'userFrom_id': userFromID,
                    'userFrom_username': userFromusername,
                    'userFrom_avatar': userFromAvatar,
                    'userFrom_bio': userFromBio,
                    'userTo': userTos,
                    'content': top_love.content,
                    'images': list(Image.objects.filter(love=top_love).values_list('image', flat=True)),
                    'thumbsUp': top_love.thumbsUpUser.count(),
                    'comments': Comment.objects.filter(love=top_love).count(),
                    'isThumbsUp': isThumbsUp,
                    'date': top_love.date
                }
            else:
                top = {
                    'id': -1,
                    'userFrom_id': -1,
                    'userFrom_avatar': '/media/img/avatar/anony.jpg',
                    'userTo': [{
                        'id': -1,
                        'username': '还没来哦～',
                        'avatar': 'img/avatar/anony.jpg',
                        'bio': '向TA表白吧～'
                    }],
                    'content': 'Wait for a confession'
                }

        # list
        for love in page.page(page_number).object_list:
            # userFrom
            if love.isAnony:
                userFromID = -1
                userFromusername = 'Anony'
                userFromAvatar = '/media/img/avatar/anony.jpg'
                userFromBio = 'TA匿名了呢～'
            else:
                userFromID = love.userFrom.id
                userFromusername = love.userFrom.username
                userFromAvatar = love.userFrom.avatar.url
                userFromBio = love.userFrom.bio
            # userTo
            userTos = list(love.userTo.values('id', 'username', 'avatar', 'bio'))
            if love.nameTo:
                for user in love.nameTo.split(';'):
                    userTos.append({
                        'id': -1,
                        'username': user,
                        'avatar': 'img/avatar/anony.jpg',
                        'bio': 'TA还没有来呢～'
                    })
            # is thumbsUp
            if request.user.is_authenticated:
                isThumbsUp = request.user in love.thumbsUpUser.all()
            else:
                isThumbsUp = False
            listLove.append({
                'id': love.id,
                'userFrom_id': userFromID,
                'userFrom_username': userFromusername,
                'userFrom_avatar': userFromAvatar,
                'userFrom_bio': userFromBio,
                'userTo': userTos,
                'content': love.content,
                'images': list(Image.objects.filter(love=love).values_list('image', flat=True)),
                'thumbsUp': love.thumbsUpUser.count(),
                'comments': Comment.objects.filter(love=love).count(),
                'isThumbsUp': isThumbsUp,
                'date': love.date
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'top': top,
                'list': listLove
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getLoseList(request):
    filterType = request.GET.get('filterType')
    order = request.GET.get('order')
    page_number = int(request.GET.get('page_number'))

    try:
        listLose = []
        if filterType == 'loseTime':
            if order == 'positive':
                page = Paginator(Lose.objects.order_by('loseDate'), 10)
            elif order == 'reverse':
                page = Paginator(Lose.objects.order_by('-loseDate'), 10)
        elif filterType == 'publicTime':
            if order == 'positive':
                page = Paginator(Lose.objects.order_by('publicDate'), 10)
            elif order == 'reverse':
                page = Paginator(Lose.objects.order_by('-publicDate'), 10)
        elif filterType == 'isFound':
            if order == 'positive':
                page = Paginator(Lose.objects.order_by('isFound'), 10)
            elif order == 'reverse':
                page = Paginator(Lose.objects.order_by('-isFound'), 10)
        else:
            page = Paginator(Lose.objects.all(), 10)

        if page_number > page.num_pages or page.count == 0:
            return JsonResponse({ 'code': 200, 'status': 'none' })

        # list
        for lose in page.page(page_number).object_list:
            # cover
            cover = Image.objects.filter(lose=lose).first().image.url
            listLose.append({
                'id': lose.id,
                'isFound': lose.isFound,
                'avatar': lose.user.avatar.url,
                'publicDate': lose.publicDate,
                'loseDate': lose.loseDate,
                'name': lose.name,
                'description': lose.description,
                'cover': cover
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listLose
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getDealList(request):
    filterType = request.GET.get('filterType')
    order = request.GET.get('order')
    page_number = int(request.GET.get('page_number'))
    
    try:
        listDeal = []
        if filterType == 'date':
            if order == 'positive':
                page = Paginator(Deal.objects.order_by('date'), 10)
            elif order == 'reverse':
                page = Paginator(Deal.objects.order_by('-date'), 10)
        elif filterType == 'new':
            if order == 'positive':
                page = Paginator(Deal.objects.order_by('new'), 10)
            elif order == 'reverse':
                page = Paginator(Deal.objects.order_by('-new'), 10)
        elif filterType == 'price':
            if order == 'positive':
                page = Paginator(Deal.objects.order_by('price'), 10)
            elif order == 'reverse':
                page = Paginator(Deal.objects.order_by('-price'), 10)
        elif filterType == 'isSold':
            if order == 'positive':
                page = Paginator(Deal.objects.order_by('isSold'), 10)
            elif order == 'reverse':
                page = Paginator(Deal.objects.order_by('-isSold'), 10)
        else:
            page = Paginator(Deal.objects.all(), 10)

        if page_number > page.num_pages or page.count == 0:
            return JsonResponse({ 'code': 200, 'status': 'none' })

        # list
        for deal in page.page(page_number).object_list:
            # cover
            cover = Image.objects.filter(deal=deal).first().image.url
            listDeal.append({
                'id': deal.id,
                'isSold': deal.isSold,
                'user': {
                    'id': deal.user.id,
                    'username': deal.user.username,
                    'avatar': deal.user.avatar.url
                },
                'name': deal.name,
                'price': deal.price,
                'new': deal.new,
                'description': deal.description,
                'cover': cover
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listDeal
            })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBriefArticleList(request):
    try:
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': list(Article.objects.values('id', 'title')[:5])
        })
    except:
        return JsonResponse({ 'code': 500 })




@csrf_exempt
def getArticleList(request):
    filterType = request.GET.get('filterType')
    order = request.GET.get('order')
    page_number = int(request.GET.get('page_number'))

    try:
        listArticle = []
        if filterType == 'date':
            if order == 'positive':
                page = Paginator(Article.objects.filter(isAdopted=True).order_by('publicDate'), 10)
            elif order == 'reverse':
                page = Paginator(Article.objects.filter(isAdopted=True).order_by('-publicDate'), 10)
        elif filterType == 'thumbsUp':
            if order == 'positive':
                page = Paginator(Article.objects.filter(isAdopted=True).annotate(numThumbsUp = Count('thumbsUpUser')).order_by('numThumbsUp'), 10)
            elif order == 'reverse':
                page = Paginator(Article.objects.filter(isAdopted=True).annotate(numThumbsUp = Count('thumbsUpUser')).order_by('-numThumbsUp'), 10)
        elif filterType == 'coin':
            if order == 'positive':
                page = Paginator(Article.objects.filter(isAdopted=True).order_by('neededCoin'), 10)
            elif order == 'reverse':
                page = Paginator(Article.objects.filter(isAdopted=True).order_by('-neededCoin'), 10)
        else:
            page = Paginator(Article.objects.all(), 10)

        if page_number > page.num_pages or page.count == 0:
            return JsonResponse({ 'code': 200, 'status': 'none' })

        for article in page.page(page_number).object_list:
            if article.isAdopted:
                listArticle.append({
                    'id': article.id,
                    'user': { 'id': article.user.id, 'avatar': article.user.avatar.url, 'username': article.user.username, 'bio': article.user.bio, 'auth': article.user.auth.split(';')[:2] if article.user.auth else None },
                    'title': article.title,
                    'tags': article.tags.split(';'),
                    'content': article.content[:50] + '...' if len(article.content) > 50 else article.content,
                    'neededCoin': article.neededCoin,
                    'publicDate': article.publicDate,
                    'editDate': article.editDate,
                    'comments': Comment.objects.filter(article=article).count(),
                    'thumbsUp': article.thumbsUpUser.count(),
                    'viewCount': article.viewCount
                })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'list': listArticle,
                'total': page.count
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getHelpList(request):
    page_number = int(request.GET.get('page_number'))

    try:
        listHelp = []
        page = Paginator(Help.objects.all(), 10)

        if page_number > page.num_pages or page.count == 0:
            return JsonResponse({ 'code': 200, 'status': 'none' })

        for _help in page.page(page_number).object_list:
            listHelp.append({
                'id': _help.id,
                'user': { 'id': _help.user.id, 'avatar': _help.user.avatar.url, 'username': _help.user.username },
                'title': _help.title,
                'content': _help.content[:10] + '...' if len(_help.content) > 10 else _help.content,
                'date': _help.date,
                'comments': Comment.objects.filter(_help=_help).count()
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listHelp
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getHelpDetail(request):
    _id = request.GET.get('id')

    try:
        _help = Help.objects.get(id=_id)
        # comments
        comments = []
        for comment in Comment.objects.filter(_help=_help):
            comments.append({
                'id': comment.user.id,
                'avatar': comment.user.avatar.url,
                'username': comment.user.username,
                'content': comment.content,
                'date': comment.date
            })
        # is own help
        isOwnHelp = False
        if _help.user == request.user:
            isOwnHelp = True

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': _help.id,
                'user': { 'id': _help.user.id, 'avatar': _help.user.avatar.url, 'username': _help.user.username, 'bio': _help.user.bio, 'auth': _help.user.auth.split(';') if _help.user.auth else None },
                'title': _help.title,
                'content': _help.content,
                'date': _help.date,
                'comments': comments,
                'isOwnHelp': isOwnHelp
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getLoveDetail(request):
    _id = request.GET.get('id')

    try:
        love = Love.objects.get(id=_id)
        # userFrom
        if love.isAnony:
            userFromID = -1
            userFromusername = 'Anony'
            userFromAvatar = '/media/img/avatar/anony.jpg'
            userFromBio = 'TA匿名了呢～'
        else:
            userFromID = love.userFrom.id
            userFromusername = love.userFrom.username
            userFromAvatar = love.userFrom.avatar.url
            userFromBio = love.userFrom.bio
        # userTo
        userTos = list(love.userTo.values('id', 'username', 'avatar', 'bio'))
        if love.nameTo:
            for user in love.nameTo.split(';'):
                userTos.append({
                    'id': -1,
                    'username': user,
                    'avatar': 'img/avatar/anony.jpg',
                    'bio': 'TA还没有来呢～'
                })
        # is thumbsUp
        if request.user.is_authenticated:
            isThumbsUp = request.user in love.thumbsUpUser.all()
        else:
            isThumbsUp = False
        # comments
        comments = list(Comment.objects.filter(love=love).values('user', 'content', 'date'))
        # is own love
        isOwnLove = False
        if love.userFrom == request.user:
            isOwnLove = True

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': love.id,
                'userFrom_id': userFromID,
                'userFrom_username': userFromusername,
                'userFrom_avatar': userFromAvatar,
                'userFrom_bio': userFromBio,
                'userTo': userTos,
                'content': love.content,
                'images': list(Image.objects.filter(love=love).values_list('image', flat=True)),
                'thumbsUp': love.thumbsUpUser.count(),
                'isThumbsUp': isThumbsUp,
                'comments': comments,
                'isOwnLove': isOwnLove
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getLoseDetail(request):
    _id = request.GET.get('id')

    try:
        lose = Lose.objects.get(id=_id)
        # comments
        comments = []
        for comment in Comment.objects.filter(lose=lose):
            comments.append({
                'id': comment.user.id,
                'avatar': comment.user.avatar.url,
                'username': comment.user.username,
                'content': comment.content,
                'date': comment.date
            })
        # is own lose
        isOwnLose = False
        if lose.user == request.user:
            isOwnLose = True

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': lose.id,
                'isFound': lose.isFound,
                'user': {
                    'id': lose.user.id,
                    'username': lose.user.username,
                    'bio': lose.user.bio,
                    'avatar': lose.user.avatar.url,
                    'auth': lose.user.auth.split(';') if lose.user.auth else None,
                    'phone': lose.user.phone[:3] + '****' + lose.user.phone[-4:] + '(已认证)' if lose.user.phone else '未认证',
                    'qq': lose.user.qq,
                    'wechat': lose.user.wechat,
                },
                'publicDate': lose.publicDate,
                'loseDate': lose.loseDate,
                'name': lose.name,
                'description': lose.description,
                'images': list(Image.objects.filter(lose=lose).values_list('image', flat=True)),
                'comments': comments,
                'isOwnLose': isOwnLose
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getDealDetail(request):
    _id = request.GET.get('id')

    try:
        deal = Deal.objects.get(id=_id)
        # comments
        comments = []
        for comment in Comment.objects.filter(deal=deal):
            comments.append({
                'id': comment.user.id,
                'avatar': comment.user.avatar.url,
                'username': comment.user.username,
                'content': comment.content,
                'date': comment.date
            })
        # is own deal
        isOwnDeal = False
        if deal.user == request.user:
            isOwnDeal = True

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': deal.id,
                'isSold': deal.isSold,
                'user': {
                    'id': deal.user.id,
                    'username': deal.user.username,
                    'bio': deal.user.bio,
                    'avatar': deal.user.avatar.url,
                    'auth': deal.user.auth.split(';') if deal.user.auth else None,
                    'phone': deal.user.phone[:3] + '****' + deal.user.phone[-4:] + '(已认证)' if deal.user.phone else '未认证',
                    'qq': deal.user.qq,
                    'wechat': deal.user.wechat,
                },
                'name': deal.name,
                'price': deal.price,
                'new': deal.new,
                'description': deal.description,
                'images': list(Image.objects.filter(deal=deal).values_list('image', flat=True)),
                'comments': comments,
                'isOwnDeal': isOwnDeal
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def removeDeal(request):
    _id = request.GET.get('id')

    try:
        deal = Deal.objects.get(id=_id)
        if deal.user != request.user:
            return JsonResponse({ 'code': 403 })
        else:
            deal.delete()
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def dealChange(request):
    _id = request.GET.get('id')
    isDone = request.GET.get('isDone')

    try:
        deal = Deal.objects.get(id=_id)
        if deal.user != request.user:
            return JsonResponse({ 'code': 403 })
        else:
            if isDone:
                deal.isSold = True
            else:
                deal.isSold = False

            deal.save()
            return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getArticleDetail(request):
    _id = request.GET.get('id')

    try:
        article = Article.objects.get(id=_id)
        if not article.isAdopted:
            return JsonResponse({ 'code': 403 })

        # is thumbsUp
        if request.user.is_authenticated:
            isThumbsUp = request.user in article.thumbsUpUser.all()
        else:
            isThumbsUp = False
        # is own article
        isOwnArticle = False
        if request.user == article.user:
            isOwnArticle = True
        # comments
        comments = []
        for comment in Comment.objects.filter(article=article):
            comments.append({
                'id': comment.user.id,
                'avatar': comment.user.avatar.url,
                'username': comment.user.username,
                'content': comment.content,
                'date': comment.date
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': article.id,
                'user': { 'id': article.user.id, 'username': article.user.username, 'bio': article.user.bio, 'avatar': article.user.avatar.url, 'auth': article.user.auth.split(';') if article.user.auth else None },
                'title': article.title,
                'tags': article.tags.split(';'),
                'content': article.content,
                'publicDate': article.publicDate,
                'editDate': article.editDate,
                'neededCoin': article.neededCoin,
                'comments': comments,
                'thumbsUp': article.thumbsUpUser.count(),
                'isThumbsUp': isThumbsUp,
                'isOwnArticle': isOwnArticle
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def thumbsUpLove(request):
    _id = request.POST.get('id')
    isThumbsUp = True if request.POST.get('isThumbsUp') == 'true' else False

    try:
        love = Love.objects.get(id=_id)
        if isThumbsUp:
            love.thumbsUpUser.add(request.user)
            # message
            message = Message.objects.create(
                user=request.user,
                _type='thumbsUp',
                _from='love',
                messageID=_id
            )
            if request.user != love.userFrom:
                love.userFrom.messages.add(message)
            for userTo in love.userTo.all():
                if request.user != userTo:
                    userTo.messages.add(message)
        else:
            love.thumbsUpUser.remove(request.user)
            love.userFrom.messages.remove(Message.objects.get(messageID=_id))
            for userTo in love.userTo.all():
                userTo.messages.remove(Message.objects.get(messageID=_id))
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def thumbsUpArticle(request):
    _id = request.POST.get('id')
    isThumbsUp = True if request.POST.get('isThumbsUp') == 'true' else False

    try:
        article = Article.objects.get(id=_id)
        if isThumbsUp:
            article.thumbsUpUser.add(request.user)
            # message
            message = Message.objects.create(
                user=request.user,
                _type='thumbsUp',
                _from='article',
                messageID=_id
            )
            if request.user != article.user:
                article.user.messages.add(message)
        else:
            article.thumbsUpUser.remove(request.user)
            article.user.messages.remove(Message.objects.get(messageID=_id))
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getNumQuestion(request):
    subject = request.GET.get('subject')
    strChapters = request.GET.getlist('chapters[]')

    try:
        quantity = 0
        subject = Bank_Subject.objects.get(name=subject)
        for strChapter in strChapters:
            chapter = Bank_Chapter.objects.filter(subject=subject).get(id=int(strChapter))
            quantity += chapter.bank_set.count()

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': quantity
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitLoveComment(request):
    _id = request.POST.get('id')
    content = request.POST.get('content')

    try:
        # comment
        love = Love.objects.get(id=_id)
        comment = Comment.objects.create(user=request.user, content=content, love=love)
        # message
        message = Message.objects.create(
            user=request.user,
            _type='comment',
            _from='love',
            messageID=_id,
            commentContent=content,
        )
        if request.user != love.userFrom:
            love.userFrom.messages.add(message)
        for userTo in love.userTo.all():
            if request.user != userTo:
                userTo.messages.add(message)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitLoseComment(request):
    _id = request.POST.get('id')
    content = request.POST.get('content')

    try:
        # comment
        lose = Lose.objects.get(id=_id)
        comment = Comment.objects.create(user=request.user, content=content, lose=lose)
        # message
        message = Message.objects.create(
            user=request.user,
            _type='comment',
            _from='lose',
            messageID=_id,
            commentContent=content,
        )
        if request.user != lose.user:
            lose.user.messages.add(message)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitDealComment(request):
    _id = request.POST.get('id')
    content = request.POST.get('content')

    try:
        # comment
        deal = Deal.objects.get(id=_id)
        comment = Comment.objects.create(user=request.user, content=content, deal=deal)
        # message
        message = Message.objects.create(
            user=request.user,
            _type='comment',
            _from='deal',
            messageID=_id,
            commentContent=content,
        )
        if request.user != deal.user:
            deal.user.messages.add(message)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitArticleComment(request):
    _id = request.POST.get('id')
    content = request.POST.get('content')

    try:
        # comment
        article = Article.objects.get(id=_id)
        comment = Comment.objects.create(user=request.user, content=content, article=article)
        # message
        message = Message.objects.create(
            user=request.user,
            _type='comment',
            _from='article',
            messageID=_id,
            commentContent=content,
        )
        article.user.messages.add(message)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def addArticleViewCount(request):
    _id = request.GET.get('id')

    try:
        article = Article.objects.get(id=_id)
        article.viewCount += 1
        article.save()

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def submitHelpComment(request):
    _id = request.POST.get('id')
    content = request.POST.get('content')

    try:
        # comment
        _help = Help.objects.get(id=_id)
        comment = Comment.objects.create(user=request.user, content=content, _help=_help)
        # message
        message = Message.objects.create(
            user=request.user,
            _type='comment',
            _from='help',
            messageID=_id,
            commentContent=content,
        )
        if request.user != _help.user:
            _help.user.messages.add(message)
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



# Pending
@csrf_exempt
def getClubDetail(request):
    name = request.GET.get('name')

    try:
        club = Club.objects.get(name=name)
        return JsonResponse({
            'name': club.name,
            'description': club.description,
            'president_uid': club.president.id,
            'president_name': club.president.username,
            'president_avatar': club.president.avatar,
            'vicePresident_uid': club.vicePresident.id,
            'vicePresident_name': club.vicePresident.username,
            'vicePresident_avatar': club.vicePresident.avatar,
            'presidentAssistant_uid': club.presidentAssistant.id,
            'presidentAssistant_name': club.presidentAssistant.username,
            'presidentAssistant_avatar': club.presidentAssistant.avatar,
            'planDirector_uid': club.planDirector.id,
            'planDirector_name': club.planDirector.username,
            'planDirector_avatar': club.planDirector.avatar,
            'financeDirector_uid': club.financeDirector.id,
            'financeDirector_name': club.financeDirector.username,
            'financeDirector_avatar': club.financeDirector.avatar,
            'feedbackDirector_uid': club.feedbackDirector.id,
            'feedbackDirector_name': club.feedbackDirector.username,
            'feedbackDirector_avatar': club.feedbackDirector.avatar,
            'ITDirector_uid': club.ITDirector.id,
            'ITDirector_name': club.ITDirector.username,
            'ITDirector_avatar': club.ITDirector.avatar,
            'propagandaDirector_uid': club.propagandaDirector.id,
            'propagandaDirector_name': club.propagandaDirector.username,
            'propagandaDirector_avatar': club.propagandaDirector.avatar,
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getBriefHotList(request):
    try:
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': list(Hot.objects.values('id', 'title', '_type')[:5])
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getHotList(request):
    try:
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': list(Hot.objects.values('id', 'title', 'date', '_type'))
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getHotDetail(request):
    _id = request.GET.get('id')

    try:
        hot = Hot.objects.get(id=_id)
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': hot.id,
                'title': hot.title,
                'type': hot._type,
                'content': hot.content,
                'date': hot.date
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@permission_required('wall.delete_hot')
def deleteHot(request):
    _id = request.GET.get('id')

    try:
        hot = Hot.objects.get(id=_id)
        hot.delete()
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@permission_required('wall.add_hot')
@permission_required('wall.change_hot')
def addHot(request):
    _id = request.POST.get('id')
    title = request.POST.get('title')
    _type = request.POST.get('type')
    content = request.POST.get('content')

    try:
        if Hot.objects.filter(id=_id).exists():
            hot = Hot.objects.get(id=_id)
            hot.title = title
            hot.type = _type
            hot.content = content
            hot.save()
        else:
            Hot.objects.create(
                title = title,
                _type = _type,
                content = content
            )
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBriefLectureList(request):
    try:
        listLecture = []
        for lecture in Lecture.objects.defer('lecturerInfo', 'startDate', 'endDate').all()[:5]:
            startDate = lecture.startDate
            endDate = lecture.endDate
            currentDate = datetime.datetime.now()

            if currentDate < startDate:
                state = '未开始'
            elif currentDate > endDate:
                state = '已结束'
            elif currentDate >= startDate and currentDate <= endDate:
                state = '进行中'

            listLecture.append({
                'id': lecture.id,
                'title': lecture.title,
                'lecturer': lecture.lecturer,
                'state': state
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listLecture
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getLectureList(request):
    listLecture = []
    try:
        for lecture in Lecture.objects.all():
            startDate = lecture.startDate
            endDate = lecture.endDate
            currentDate = datetime.datetime.now()

            if currentDate < startDate:
                state = '未开始'
            elif currentDate > endDate:
                state = '已结束'
            elif currentDate >= startDate and currentDate <= endDate:
                state = '进行中'

            listLecture.append({
                'id': lecture.id,
                'title': lecture.title,
                'lecturer': lecture.lecturer,
                'lecturerInfo': lecture.lecturerInfo,
                'address': lecture.address,
                'startDate': lecture.startDate,
                'endDate': lecture.endDate,
                'state': state
            })
        return JsonResponse({ 'code': 200, 'status': 'success', 'data': listLecture })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getLectureDetail(request):
    _id = request.GET.get('id')

    try:
        lecture = Lecture.objects.get(id=_id)
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': lecture.id,
                'title': lecture.title,
                'lecturer': lecture.lecturer,
                'lecturerInfo': lecture.lecturerInfo,
                'address': lecture.address,
                'startDate': lecture.startDate,
                'endDate': lecture.endDate
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@permission_required('wall.add_lecture')
@permission_required('wall.change_lecture')
def addLecture(request):
    _id = request.POST.get('id')
    title = request.POST.get('title')
    lecturer = request.POST.get('lecturer')
    lecturerInfo = request.POST.get('lecturerInfo')
    address = request.POST.get('address')
    startDate = datetime.datetime.strptime(request.POST.get('startDate'), '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d %H:%M:%S')

    try:
        if Lecture.objects.filter(id=_id).exists():
            lecture = Lecture.objects.get(id=_id)
            lecture.title = title
            lecture.lecturer = lecturer
            lecture.lecturerInfo = lecturerInfo
            lecture.address = address
            lecture.startDate = startDate
            lecture.endDate = endDate
            lecture.save()
        else:
            Lecture.objects.create(
                title = title,
                lecturer = lecturer,
                lecturerInfo = lecturerInfo,
                address = address,
                startDate = startDate,
                endDate = endDate
            )
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@permission_required('wall.delete_lecture')
def deleteLecture(request):
    _id = request.GET.get('id')
    try:
        Lecture.objects.get(id=_id).delete()
        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBriefMatchList(request):
    try:
        listMatch = []
        for match in Match.objects.defer('title', 'startDate', 'endDate', 'totalBonus').all()[:5]:
            startDate = match.startDate
            endDate = match.endDate
            currentDate = datetime.datetime.now()

            if currentDate < startDate:
                state = '未开始'
            elif currentDate > endDate:
                state = '已结束'
            elif currentDate >= startDate and currentDate <= endDate:
                state = '进行中'

            listMatch.append({
                'id': match.id,
                'title': match.title,
                'state': state,
                'totalBonus': match.totalBonus
            })

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': listMatch
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getMatchList(request):
    listMatch = []
    try:
        for match in Match.objects.all():
            startDate = match.startDate
            endDate = match.endDate
            currentDate = datetime.datetime.now()

            if currentDate < startDate:
                state = '未开始'
            elif currentDate > endDate:
                state = '已结束'
            elif currentDate >= startDate and currentDate <= endDate:
                state = '进行中'

            listMatch.append({
                'id': match.id,
                'title': match.title,
                'startDate': match.startDate,
                'endDate': match.endDate,
                'state': state,
                'totalBonus': match.totalBonus
            })
        return JsonResponse({ 'code': 200, 'status': 'success', 'data': listMatch })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getMatchDetail(request):
    _id = request.GET.get('id')

    try:
        match = Match.objects.get(id=_id)
        files = []
        for _file in CommonFile.objects.filter(match=match):
            files.append({
                'name': _file.name,
                'type': _file._type,
                'url': _file._file.url
            })
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'id': match.id,
                'title': match.title,
                'description': match.description,
                'requirement': match.requirement,
                'prizeDescription': match.prizeDescription,
                'startDate': match.startDate,
                'endDate': match.endDate,
                'totalBonus': match.totalBonus,
                'files': files
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



# Pending
@csrf_exempt
def getUserList(request):
    listUser = []
    try:
        for user in User.objects.all():
            listUser.append({
                'key': user.id,
                'email': user.email,
                'username': user.username,
                'bio': user.bio,
                'class': user._class,
                'phone': user.phone,
                'qq': user.qq,
                'wechat': user.wechat,
                'coin': user.coin,
                'isAdmin': user.is_staff,
                'auth': user.auth
            })
        return JsonResponse({ 'info': listUser })
    except:
        return HttpResponse(1)



@csrf_exempt
def getBankChapters(request):
    subject = request.GET.get('subject')
    
    try:
        chapters = []
        for chapter in Bank_Chapter.objects.filter(subject=Bank_Subject.objects.get(name=subject)):
            chapters.append(chapter.name)
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': chapters
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@permission_required('wall.add_bank')
def uploadBank(request):
    try:
        # save the csv file
        file_obj = request.FILES.get('uploadBank')
        fileName, suffix = file_obj.name.split('.')
        name = "latestBank.csv"
        f = open(generateUploadPath('/', name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        # write the data of csv to BANK
        subject = request.POST.get('subject')
        chapter = request.POST.get('chapter')

        with open(generateUploadPath('/', name), 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                Bank.objects.create(
                    title = line[0],
                    A = line[1],
                    B = line[2],
                    C = line[3],
                    D = line[4],
                    E = line[5],
                    questionType = line[6],
                    isBlankSeq = line[7],
                    answer = line[8],
                    chapter = Bank_Chapter.objects.filter(subject=Bank_Subject.objects.get(name=subject)).get(name=chapter)
                )

        # update infomation of the uploader
        comment = request.POST.get('comment')

        Bank_UploadHistory.objects.create(
            comment = subject + '/' + chapter + '/' + fileName + '/' + comment,
            user = request.user
        )

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getBankUploadHistory(request):
    historyList = []
    for history in Bank_UploadHistory.objects.all():
        historyList.append({
            'comment': history.comment,
            'user': { 'username': history.user.username, 'avatar': history.user.avatar.url },
            'date': history.date
        })

    return JsonResponse({ 'info': historyList })



@csrf_exempt
def getFileUploadHistory(request):
    historyList = []
    for history in File_UploadHistory.objects.all():
        historyList.append({
            'comment': history.comment,
            'user': { 'username': history.user.username, 'avatar': history.user.avatar.url },
            'date': history.date
        })

    return JsonResponse({ 'info': historyList })



@csrf_exempt
@permission_required('wall.add_file')
def uploadFile(request):
    try:
        # save the file
        file_obj = request.FILES.get('uploadFile')
        originName, suffix = file_obj.name.split('.')
        name = originName + ''.join(random.choice(string.ascii_letters + string.digits))
        encryptedName = hashlib.new('md5', name.encode('utf8')).hexdigest() + '.' + suffix

        f = open(generateUploadPath('/file/', encryptedName), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        
        # write the file info to FILE
        subject = request.POST.get('subject')
        fileType = {
            'doc': 'word',
            'docx': 'word',
            'xls': 'excel',
            'xlsx': 'excel',
            'csv': 'excel',
            'ppt': 'ppt',
            'pptx': 'ppt',
            'pdf': 'pdf'
        }
        File.objects.create(
            name=originName,
            _file='file/' + encryptedName,
            _type=fileType[suffix],
            subject=File_Subject.objects.get(name=subject)
        )

        # update infomation of the uploader
        comment = request.POST.get('comment')

        File_UploadHistory.objects.create(
            comment = name + '/' + comment,
            user = request.user
        )

        return JsonResponse({ 'code': 200, 'status': 'success' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getUserDetail(request):
    try:
        return JsonResponse({
            'email': request.user.email,
            'username': request.user.username,
            'bio': request.user.bio,
            'class': request.user._class.split('/'),
            #'phone': request.user.phone,
            'qq': request.user.qq,
            'wechat': request.user.wechat,
            'coin': request.user.coin,
            'isAdmin': request.user.is_staff,
            'auth': request.user.auth
        })
    except:
        return HttpResponse(1)



# Pending
@csrf_exempt
def updateUserAdmin(request):
    uid = request.POST.get('uid', None)
    email = request.POST.get('email')
    username = request.POST.get('username')
    bio = request.POST.get('bio')
    _class = request.POST.get('class[0]') + '/' + request.POST.get('class[1]')
    phone = request.POST.get('phone')
    qq = request.POST.get('qq')
    wechat = request.POST.get('wechat')
    coin = request.POST.get('coin')
    isAdmin = True if request.POST.get('isAdmin') == 'true' else False
    auth = request.POST.get('auth')

    try:
        if User.objects.filter(id=uid).exists():
            user = User.objects.get(id=uid)
            user.email = email
            user.username = username
            user.bio = bio
            user._class = _class
            user.phone = phone
            user.qq = qq
            user.wechat = wechat
            user.coin = coin
            user.is_staff = isAdmin
            user.auth = auth

            user.save()
            return HttpResponse(0)
    except:
        return HttpResponse(1)



# Pending
@csrf_exempt
def deleteUser(request):
    _id = request.POST.get('id')
    try:
        user = User.objects.get(id=_id)
        user.delete()
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def getAllMedicine_Type(request):
    _type = request.GET.get('type')
    subType = request.GET.get('subType')

    allMedicine = []
    for medicine in Medicine.objects.filter(_type=_type).filter(subType=subType):
        allMedicine.append({
            'name': medicine.name,
            'image': medicine.image.url
        })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': allMedicine
    })



@csrf_exempt
def getAllMedicine_Flavor(request):
    flavors = request.GET.getlist('flavors[]')

    if not flavors:
        return JsonResponse({ 'code': 200, 'status': 'none' })

    allMedicine = []
    for medicine in Medicine.objects.all():
        isTag = True
        for flavor in flavors:
            if flavor not in medicine.flavor:
                isTag = False
                break
        if isTag:
            allMedicine.append({
                'name': medicine.name,
                'image': medicine.image.url
            })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': allMedicine
    })



@csrf_exempt
def getAllMedicine_Channel(request):
    channels = request.GET.getlist('channels[]')

    if not channels:
        return JsonResponse({ 'code': 200, 'status': 'none' })
    
    allMedicine = []
    for medicine in Medicine.objects.all():
        isTag = True
        for channel in channels:
            if channel not in medicine.channel:
                isTag = False
                break
        if isTag:
            allMedicine.append({
                'name': medicine.name,
                'image': medicine.image.url
            })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': allMedicine
    })



@csrf_exempt
def getMedicineDetail(request):
    name = request.GET.get('name')
    User_Agent = request.headers['User-Agent']

    try:
        if 'UE4' in User_Agent:
            ue_json = json.loads(request.body.decode('utf-8'))
            name = ue_json['name']

        medicine = Medicine.objects.get(name=name)
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': {
                'name': medicine.name,
                'flavor': medicine.flavor,
                'channel': medicine.channel,
                'function': medicine.function,
                'application': medicine.application,
                'image': medicine.image.url,
                'type': medicine._type,
                'subType': medicine.subType,
                'highlight': medicine.highlight,
                'toxicity': medicine.toxicity,
                'relevantMedicine': ';'.join(list(medicine.relevantMedicine.all().values_list('name', flat=True)))
            }
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchMedicine(request):
    keyword = request.GET.get('keyword')

    try:
        _list = []
        if keyword != '':
            for medicine in Medicine.objects.filter(name__contains=keyword):
                _list.append({
                    'name': medicine.name,
                    'flavor': medicine.flavor,
                    'channel': medicine.channel,
                    'type': medicine._type + '/' + medicine.subType,
                })
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': _list
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def autoComplete_searchMedicine(request):
    keyword = request.GET.get('keyword')
    User_Agent = request.headers['User-Agent']

    try:
        if 'UE4' in User_Agent:
            ue_json = json.loads(request.body.decode('utf-8'))
            keyword = ue_json['keyword']

        _list = []
        if keyword != '':
            _list = list(Medicine.objects.filter(name__contains=keyword).values_list('name', flat=True))
        else:
            _list = []

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': _list
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def IsSetMedicineReciteSetting(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'code': 200,
            'status': 'false'
        })
    if not Medicine_Recite.objects.filter(user=request.user).exists():
        return JsonResponse({
            'code': 200,
            'status': 'false'
        })
    
    recite = Medicine_Recite.objects.get(user=request.user)
    # a new day
    if datetime.date.today() > recite.lastReciteDate:
        recite.lastReciteDate = datetime.date.today()
        # recite
        if recite.allUnrecitedMedicine.count() > int(recite.everydayAmount):
            recite.todayWillReciteAmount = recite.everydayAmount
            recite.todayUnrecitedMedicine.set(recite.allUnrecitedMedicine.all()[:int(recite.everydayAmount)])
        else:
            recite.todayWillReciteAmount = recite.allUnrecitedMedicine.count()
            recite.todayUnrecitedMedicine.set(recite.allUnrecitedMedicine.all())
        # review
        randomAllReviewMedicine = list(recite.allReviewMedicine.all())
        random.shuffle(randomAllReviewMedicine)
        if recite.allReviewMedicine.count() > int(recite.everydayAmount) / 2:
            recite.todayWillReviewAmount = int(recite.everydayAmount / 2)
            recite.todayReviewMedicine.set(randomAllReviewMedicine[:int(recite.everydayAmount / 2)])
        else:
            recite.todayWillReviewAmount = recite.allReviewMedicine.count()
            recite.todayReviewMedicine.set(randomAllReviewMedicine)
        recite.save()

    

    return JsonResponse({
            'code': 200,
            'status': 'true',
            'data': {
                'signDays': Medicine_Recite_Log.objects.filter(user=request.user).count(),
                'chapters': recite.chapters,
                'recitedAmount': recite.totalAmount - recite.allUnrecitedMedicine.count(),
                'everydayAmount': recite.everydayAmount,
                'totalAmount': recite.totalAmount,
                'todayWillReciteAmount': recite.todayWillReciteAmount,
                'todayWillReviewAmount': recite.todayWillReviewAmount,
                'todayUnlearnedAmount': recite.todayUnrecitedMedicine.count() + recite.todayReviewMedicine.count()
            }
        })



@csrf_exempt
def getNumMedicine(request):
    strChapters = request.GET.getlist('chapters[]')

    try:
        quantity = 0
        for strChapter in strChapters:
            quantity += Medicine.objects.filter(_type=strChapter).count()

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': quantity
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getPlanChapters_Medicine(request):
    recite = Medicine_Recite.objects.get(user=request.user)

    maxChapters = 0
    for chapter in recite.chapters.split(';'):
        maxChapters += Medicine.objects.filter(_type=chapter).count()

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': {
            'chapters': recite.chapters.split(';'),
            'maxChapters': maxChapters,
            'currentAmount': recite.everydayAmount,
            'isRandom': recite.isRandom
        }
    })



@csrf_exempt
@login_required
def submitReciteSetting_Medicine(request):
    chapters = request.POST.getlist('chapters[]')
    amount = int(request.POST.get('amount'))
    isRandom = True if request.POST.get('isRandom') == 'true' else False

    isChangeChapter = False
    try:
        # Create or Update
        if not Medicine_Recite.objects.filter(user=request.user).exists():
            recite = Medicine_Recite.objects.create(user=request.user)
        else:
            recite = Medicine_Recite.objects.get(user=request.user)
            if recite.chapters == ';'.join(chapters):
                isChangeChapter = False
                recite.everydayAmount = amount
            else:
                isChangeChapter = True
                recite.allUnrecitedMedicine.clear()
                recite.allReviewMedicine.clear()

            recite.todayUnrecitedMedicine.clear()
            recite.todayReviewMedicine.clear()

        if isChangeChapter:
            for chapter in chapters:
                recite.allUnrecitedMedicine.add(*Medicine.objects.filter(_type=chapter))

            recite.totalAmount = recite.allUnrecitedMedicine.count()

        recite.isRandom = isRandom
        recite.chapters = ';'.join(chapters)
        recite.everydayAmount = amount

        # recite
        if isRandom:
            randomAllUnrecitedMedicine = list(recite.allUnrecitedMedicine.all())
            random.shuffle(randomAllUnrecitedMedicine)
            recite.allUnrecitedMedicine.set(randomAllUnrecitedMedicine)
        else:
            recite.allUnrecitedMedicine.clear()
            for chapter in chapters:
                recite.allUnrecitedMedicine.add(*Medicine.objects.filter(_type=chapter))
                randomAllUnrecitedMedicine = recite.allUnrecitedMedicine.all()
        
        if recite.allUnrecitedMedicine.count() > int(recite.everydayAmount):
            recite.todayWillReciteAmount = recite.everydayAmount
            recite.todayUnrecitedMedicine.set(randomAllUnrecitedMedicine[:int(recite.everydayAmount)])
        else:
            recite.todayWillReciteAmount = recite.allUnrecitedMedicine.count()
            recite.todayUnrecitedMedicine.set(randomAllUnrecitedMedicine)

        # review
        randomAllReviewMedicine = list(recite.allReviewMedicine.all())
        random.shuffle(randomAllReviewMedicine)
        if recite.allReviewMedicine.count() > int(recite.everydayAmount) / 2:
            recite.todayWillReviewAmount = recite.everydayAmount / 2
            recite.todayReviewMedicine.set(randomAllReviewMedicine[:int(recite.everydayAmount / 2)])
        else:
            recite.todayWillReviewAmount = recite.allReviewMedicine.count()
            recite.todayReviewMedicine.set(randomAllReviewMedicine)
        recite.save()
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def getReciteMedicine(request):
    recite = Medicine_Recite.objects.get(user=request.user)

    try:
        data = []
        # Check date first
        if recite.lastReciteDate < datetime.date.today():
            return JsonResponse({
                'code': 200,
                'status': 'nextDay'
            })

        # Review first
        if recite.todayReviewMedicine.count() > 0:
            medicines = [reciteThrough.medicine for reciteThrough in recite.todayReviewMedicine.through.objects.filter(medicine_recite=recite).order_by('id')]
            M = medicines[:10] if recite.todayReviewMedicine.count() >= 10 else medicines

            for medicine in M:
                data.append({
                    'name': medicine.name,
                    'flavor': medicine.flavor,
                    'channel': medicine.channel,
                    'function': medicine.function,
                    'application': medicine.application,
                    'type': medicine._type,
                    'subType': medicine.subType,
                    'highlight': medicine.highlight,
                    'toxicity': medicine.toxicity,
                    'isReview': True
                })
        # Then new medicine
        else:
            medicines = [reciteThrough.medicine for reciteThrough in recite.todayUnrecitedMedicine.through.objects.filter(medicine_recite=recite).order_by('id')]
            M = medicines[:10] if recite.todayUnrecitedMedicine.count() >= 10 else medicines

            for medicine in M:
                data.append({
                    'name': medicine.name,
                    'flavor': medicine.flavor,
                    'channel': medicine.channel,
                    'function': medicine.function,
                    'application': medicine.application,
                    'type': medicine._type,
                    'subType': medicine.subType,
                    'highlight': medicine.highlight,
                    'toxicity': medicine.toxicity,
                    'isReview': False
                })
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'bank': data,
            'todayReviewAmount': recite.todayWillReviewAmount - recite.todayReviewMedicine.count(),
            'todayReciteAmount': recite.todayWillReciteAmount - recite.todayUnrecitedMedicine.count()
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def recite_remember_medicine(request):
    name = request.POST.get('name')
    isReview = True if request.POST.get('isReview') == 'true' else False

    try:
        recite = Medicine_Recite.objects.get(user=request.user)
        medicine = Medicine.objects.get(name=name)

        if isReview:
            # today
            recite.todayReviewMedicine.remove(medicine)
        else:
            # all
            recite.allUnrecitedMedicine.remove(medicine)
            recite.allReviewMedicine.add(medicine)
            # today
            recite.todayUnrecitedMedicine.remove(medicine)
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def recite_forget_medicine(request):
    name = request.POST.get('name')
    isReview = True if request.POST.get('isReview') == 'true' else False

    try:
        recite = Medicine_Recite.objects.get(user=request.user)
        medicine = Medicine.objects.get(name=name)

        if not isReview:
            # all
            recite.allReviewMedicine.add(medicine)
            recite.allUnrecitedMedicine.remove(medicine)
            # today
            recite.todayUnrecitedMedicine.remove(medicine)
            recite.todayReviewMedicine.add(medicine)
            recite.todayWillReviewAmount = recite.todayWillReviewAmount + 1

            recite.save()
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def recite_forgetUndo_medicine(request):
    name = request.POST.get('name')
    isReview = True if request.POST.get('isReview') == 'true' else False

    try:
        recite = Medicine_Recite.objects.get(user=request.user)
        medicine = Medicine.objects.get(name=name)
        
        # today
        recite.todayReviewMedicine.add(medicine)
        if not isReview:
            recite.todayWillReviewAmount = recite.todayWillReviewAmount + 1

        recite.save()
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def recite_trash_medicine(request):
    name = request.POST.get('name')
    isReview = True if request.POST.get('isReview') == 'true' else False

    try:
        recite = Medicine_Recite.objects.get(user=request.user)
        medicine = Medicine.objects.get(name=name)

        #all
        recite.allUnrecitedMedicine.remove(medicine)
        recite.allReviewMedicine.remove(medicine)
        
        #today
        if isReview:
            recite.todayReviewMedicine.remove(medicine)
        else:
            recite.todayUnrecitedMedicine.remove(medicine)
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def recite_trashMore_medicine(request):
    name = request.POST.get('name')

    try:
        recite = Medicine_Recite.objects.get(user=request.user)
        medicine = Medicine.objects.get(name=name)

        #all
        recite.allReviewMedicine.remove(medicine)
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def recite_restore_medicine(request):
    name = request.POST.get('name')
    isReview = True if request.POST.get('isReview') == 'true' else False

    try:
        recite = Medicine_Recite.objects.get(user=request.user)
        medicine = Medicine.objects.get(name=name)

        #today
        if isReview:
            recite.allReviewMedicine.add(medicine)
            recite.todayReviewMedicine.add(medicine)
        else:
            recite.allUnrecitedMedicine.add(medicine)
            recite.todayUnrecitedMedicine.add(medicine)
        
        return JsonResponse({
            'code': 200,
            'status': 'success'
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
@login_required
def canSign_reciteMedicine(request):
    recite = Medicine_Recite.objects.get(user=request.user)

    # Not enter the home page first whereas log page directly
    if not Medicine_Recite.objects.filter(user=request.user, lastReciteDate=datetime.date.today()).exists():
        return JsonResponse({
            'code': 200,
            'status': 'false',
            'signDays': Medicine_Recite_Log.objects.filter(user=request.user).count()
        })

    if Medicine_Recite_Log.objects.filter(user=request.user).filter(date=datetime.date.today()).exists():
        return JsonResponse({
            'code': 200,
            'status': 'done',
            'signDays': Medicine_Recite_Log.objects.filter(user=request.user).count()
        })

    if recite.todayUnrecitedMedicine.count() == 0 and recite.todayReviewMedicine.count() == 0:
        return JsonResponse({
            'code': 200,
            'status': 'true',
            'signDays': Medicine_Recite_Log.objects.filter(user=request.user).count()
        })
    else:
        return JsonResponse({
            'code': 200,
            'status': 'false',
            'signDays': Medicine_Recite_Log.objects.filter(user=request.user).count()
        })



@csrf_exempt
@login_required
def sign_reciteMedicine(request):
    recite = Medicine_Recite.objects.get(user=request.user)
    if recite.todayUnrecitedMedicine.count() == 0 and recite.todayReviewMedicine.count() == 0:
        if Medicine_Recite_Log.objects.filter(date=datetime.date.today()).exists():
            return JsonResponse({
                'code': 200,
                'status': 'warning',
                'message': '您已经打过卡了'
            })
        else:
            Medicine_Recite_Log.objects.create(user=request.user, date=datetime.date.today())
            return JsonResponse({
                'code': 200,
                'status': 'success',
            })
    else:
        return JsonResponse({
            'code': 200,
            'status': 'error',
            'message': '不具备打卡资格'
        })



@csrf_exempt
@login_required
def getSignLog_reciteMedicine(request):
    dates = request.POST.getlist('dates[]')
    
    try:
        signLog = {}
        for date in dates:
            if Medicine_Recite_Log.objects.filter(user=request.user).filter(date=datetime.datetime.strptime(date, "%Y-%m-%d")).exists():
                signLog[date] = True
            else:
                signLog[date] = False
        
        return JsonResponse({
                'code': 200,
                'status': 'success',
                'data': signLog
            })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getAllPrescription(request):
    _type = request.GET.get('type')

    allPrescription = []
    for prescription in Prescription.objects.filter(_type=_type):
        allPrescription.append({
            'name': prescription.name,
            'function': prescription.function,
            'application': prescription.application
        })

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': allPrescription
    })



@csrf_exempt
def getPrescriptionDetail(request):
    name = request.GET.get('name')
    User_Agent = request.headers['User-Agent']

    if 'UE4' in User_Agent:
        ue_json = json.loads(request.body.decode('utf-8'))
        name = ue_json['name']

    prescription = Prescription.objects.get(name=name)

    prescriptionDetail = {
        'name': prescription.name,
        'song': prescription.song,
        'medicine': [medicineThrough.medicine.name for medicineThrough in prescription.medicine.through.objects.filter(prescription=prescription).order_by('id')],
        'function': prescription.function,
        'application': prescription.application,
        'type': prescription._type
    }

    return JsonResponse({
        'code': 200,
        'status': 'success',
        'data': prescriptionDetail
    })



@csrf_exempt
def searchPrescription(request):
    keyword = request.GET.get('keyword')

    try:
        _list = []
        if keyword != '':
            for prescription in Prescription.objects.filter(name__contains=keyword):
                _list.append({
                    'name': prescription.name,
                    'function': prescription.function,
                    'type': prescription._type
                })
        
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': _list
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def autoComplete_searchPrescription(request):
    keyword = request.POST.get('keyword')
    User_Agent = request.headers['User-Agent']

    if 'UE4' in User_Agent:
        ue_json = json.loads(request.body.decode('utf-8'))
        keyword = ue_json['keyword']

    info = []
    if keyword != '':
        for prescription in Prescription.objects.filter(name__contains=keyword):
            info.append(prescription.name)
    
    return JsonResponse({ 'info': info })



@csrf_exempt
def getAllAcupoint_Channel(request):
    channel = request.GET.get('channel')

    try:
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': list(Acupoint.objects.filter(channel=channel).values())
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getAllAcupoint_Type(request):
    _type = request.GET.get('type')

    try:
        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': list(Acupoint.objects.filter(_type__contains=_type).values())
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def getAcupointDetail(request):
    name = request.GET.get('name')
    User_Agent = request.headers['User-Agent']

    try:
        if 'UE4' in User_Agent:
            ue_json = json.loads(request.body.decode('utf-8'))
            name = ue_json['name']

        acupoint = Acupoint.objects.get(name=name)
        acupointDetail = {
            'name': acupoint.name,
            'location': acupoint.location,
            'function': acupoint.function,
            'type': acupoint._type,
            'channel': acupoint.channel
        }

        return JsonResponse({
            'code': 200,
            'status': 'success',
            'data': acupointDetail
        })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def searchAcupoint(request):
    keyword = request.GET.get('keyword')

    try:
        if keyword != '':
            return JsonResponse({
                'code': 200,
                'status': 'success',
                'data': list(Acupoint.objects.filter(name__contains=keyword).values('name', 'location', '_type', 'channel'))
            })
        return JsonResponse({ 'code': 200, 'status': 'none' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def autoComplete_searchAcupoint(request):
    keyword = request.GET.get('keyword')

    try:
        if keyword != '':
            return JsonResponse({
                'code': 200,
                'status': 'success',
                'data': list(Acupoint.objects.filter(name__contains=keyword).values_list('name', flat=True))
            })
        return JsonResponse({ 'code': 200, 'status': 'none' })
    except:
        return JsonResponse({ 'code': 500 })



@csrf_exempt
def addNewLog_VirtualDiagnosis(request):
    User_Agent = request.headers['User-Agent']

    if 'UE4' in User_Agent:
        ue_json = json.loads(request.body.decode('utf-8'))

        email = ue_json['email']
        
        patient_name = ue_json['patient_name']
        patient_gender = ue_json['patient_gender']
        patient_age = ue_json['patient_age']
        patient_chiefcomplaint = ue_json['patient_chiefcomplaint']
        patient_coldhot = ue_json['patient_coldhot']
        patient_sweat = ue_json['patient_sweat']
        patient_pain = ue_json['patient_pain']
        patient_body = ue_json['patient_body']
        patient_eareye = ue_json['patient_eareye']
        patient_sleep = ue_json['patient_sleep']
        patient_flavor = ue_json['patient_flavor']
        patient_excretion = ue_json['patient_excretion']
        patient_face = ue_json['patient_face']
        patient_tongue = ue_json['patient_tongue']
        patient_vein = ue_json['patient_vein']

        player_diagnosis = ue_json['player_diagnosis']
        player_syndrome = ue_json['player_syndrome']
        player_method = ue_json['player_method']
        player_prescription = ue_json['player_prescription']
        player_acupoints = ue_json['player_acupoints']

        ref_diagnosis = ue_json['ref_diagnosis']
        ref_syndrome = ue_json['ref_syndrome']
        ref_method = ue_json['ref_method']
        ref_prescription = ue_json['ref_prescription']
        ref_acupoints = ue_json['ref_acupoints']

    try:
        Statistics_VirtualDiagnosis.objects.create(
            user = User.objects.get(email=email),

            patient_name = patient_name,
            patient_gender = patient_gender,
            patient_age = patient_age,
            patient_chiefcomplaint = patient_chiefcomplaint,
            patient_coldhot = patient_coldhot,
            patient_sweat = patient_sweat,
            patient_pain = patient_pain,
            patient_body = patient_body,
            patient_eareye = patient_eareye,
            patient_sleep = patient_sleep,
            patient_flavor = patient_flavor,
            patient_excretion = patient_excretion,
            patient_face = patient_face,
            patient_tongue = patient_tongue,
            patient_vein = patient_vein,

            player_diagnosis = player_diagnosis,
            player_syndrome = player_syndrome,
            player_method = player_method,
            player_prescription = player_prescription,
            player_acupoints = player_acupoints,

            ref_diagnosis = ref_diagnosis,
            ref_syndrome = ref_syndrome,
            ref_method = ref_method,
            ref_prescription = ref_prescription,
            ref_acupoints = ref_acupoints
        )
        return HttpResponse(1)
    except:
        return HttpResponse(0)



@csrf_exempt
def getLog_VirtualDiagnosis(request):
    info = []
    if request.user.is_authenticated:
        for log in Statistics_VirtualDiagnosis.objects.filter(user=request.user):
            info.append({
                'key': log.id,
                'patient_name': log.patient_name,
                'patient_gender': log.patient_gender,
                'patient_age': log.patient_age,
                'date': log.date
            })
        return JsonResponse({ 'info': info })
    else:
        return HttpResponse(1)



@csrf_exempt
def getLogDetail_VirtualDiagnosis(request):
    _id = request.GET.get('id')

    info = []
    if request.user.is_authenticated:
        log = Statistics_VirtualDiagnosis.objects.filter(user=request.user).get(id=_id)
        return JsonResponse({
            'patient_name': log.patient_name,
            'patient_gender': log.patient_gender,
            'patient_age': log.patient_age,
            'patient_chiefcomplaint': log.patient_chiefcomplaint,
            'patient_coldhot': log.patient_coldhot,
            'patient_sweat': log.patient_sweat,
            'patient_pain': log.patient_pain,
            'patient_body': log.patient_body,
            'patient_eareye': log.patient_eareye,
            'patient_sleep': log.patient_sleep,
            'patient_flavor': log.patient_flavor,
            'patient_excretion': log.patient_excretion,
            'patient_face': log.patient_face,
            'patient_tongue': log.patient_tongue,
            'patient_vein': log.patient_vein,

            'player_diagnosis': log.player_diagnosis,
            'player_syndrome': log.player_syndrome,
            'player_method': log.player_method,
            'player_prescription' : log.player_prescription,
            'player_acupoints': log.player_acupoints,

            'ref_diagnosis': log.ref_diagnosis,
            'ref_syndrome': log.ref_syndrome,
            'ref_method': log.ref_method,
            'ref_prescription': log.ref_prescription,
            'ref_acupoints': log.ref_acupoints,
            'date': log.date
        })
    else:
        return HttpResponse(1)

