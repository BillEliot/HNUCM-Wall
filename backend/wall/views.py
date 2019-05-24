from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import *
from datetime import timedelta
import os


@csrf_exempt
def getCaptcha(request):
    receiver = request.POST.get('email')
    captcha = generateCaptcha()

    if sendCaptcha(receiver, captcha):
        request.session['captcha'] = captcha
        request.session.set_expiry(1800)
        return HttpResponse(0)
    else:
        return HttpResponse(1)



@csrf_exempt
def register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    nickname = request.POST.get('nickname')
    bio = request.POST.get('bio')
    _class = request.POST.get('class[0]') + '/' + request.POST.get('class[1]')
    phone = request.POST.get('phone')
    qq = request.POST.get('qq')
    wechat = request.POST.get('wechat')
    captcha = request.POST.get('captcha')

    # check captcha
    session_captcha = request.session.get('captcha', None)
    if not session_captcha or captcha != session_captcha:
        return HttpResponse(1)
    # check email
    if User.objects.filter(email=email).exists():
        return HttpResponse(2)
    # check nickname
    if User.objects.filter(nickname=nickname).exists():
        return HttpResponse(3)

    try:
        User.objects.create(
            email = email,
            password = password,
            nickname = nickname,
            bio = bio,
            _class = _class,
            phone = phone,
            qq = qq,
            wechat = wechat
        )
        return HttpResponse(0)
    except:
        return HttpResponse(4)



@csrf_exempt
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    if (User.objects.filter(email=email).exists()):
        user = User.objects.get(email=email)
        if (user.password == password):
            request.session['uid'] = user.id
            request.session.set_expiry(timedelta(days=7))
            return HttpResponse(0)
        else:
            return HttpResponse(2)
    else:
        return HttpResponse(1)



@csrf_exempt
def getUserBaseInfo(request):
    uid = request.session.get('uid', None)

    if (uid):
        try:
            user = User.objects.get(id=uid)
            return JsonResponse({
                'nickname': user.nickname,
                'avatar': user.avatar.url
            })
        except:
            return HttpResponse(1)
    else:
        return HttpResponse(1)



@csrf_exempt
def searchUser(request):
    user = request.POST.get('user')

    try:
        # email
        if isEmail(user):
            listEmail = []
            for user in User.objects.filter(email__contains=user):
                listEmail.append(user.email)
            return JsonResponse({ 'info': listEmail })
        # nickname
        else:
            listNickname = []
            for user in User.objects.filter(nickname__contains=user):
                listNickname.append(user.nickname)
            return JsonResponse({ 'info': listNickname })
    except:
        return JsonResponse({ 'info': [] })



@csrf_exempt
def uploadLoveImg(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('files')
        name = formatName(file_obj.name)
        f = open(generateLoveImgPath(name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        return HttpResponse(name)



@csrf_exempt
def removeLoveImg(request):
    name = request.POST.get('name')
    
    try:
        os.remove(generateLoveImgPath(name))
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitLove(request):
    anony = request.POST.get('anony')
    userTo = request.POST.get('userTo')
    content = request.POST.get('content')
    images = request.POST.getlist('images[]')


    # get userFrom
    try:
        UserFrom = User.objects.get(id=request.session.get('uid', None))
    except:
        return HttpResponse(1)
    
    # get userTo
    try:
        if (isEmail(userTo)):
            UserTo = User.objects.get(email=userTo)
        else:
            UserTo = User.objects.get(nickname=userTo)
    except:
        UserTo = None

    # create
    try:
        love = Love.objects.create(
            userFrom=UserFrom,
            userTo=UserTo,
            content=content
        )
        if images:
            for image in images:
                love.images.add(Image.objects.create(name='/media/img/loveImg' + image))

        return HttpResponse(0)
    except:
        return HttpResponse(2)



@csrf_exempt
def getLoveList(request):
    index = int(request.POST.get('index'))

    if (index >= Love.objects.all().count()):
        return HttpResponse(1)

    listLove = []
    for love in Love.objects.all()[index:index+9]:
        # cover
        if love.images.count():
            cover = love.images.all()[0].name
        else:
            cover = ''
        # userTo
        if love.userTo:
            userToNickname = love.userTo.nickname
            userToAvatar = love.userTo.avatar.url
            userToBio = love.userTo.bio
        else:
            userToNickname = 'TA'
            userToAvatar = '/media/img/avatar/anony.jpg'
            userToBio = 'TA还没有来呢～'
        listLove.append({
            'userFrom_nickname': love.userFrom.nickname,
            'userFrom_avatar': love.userFrom.avatar.url,
            'userFrom_bio': love.userFrom.bio,
            'userTo_nickname': userToNickname,
            'userTo_avatar': userToAvatar,
            'userTo_bio': userToBio,
            'content': love.content,
            'cover': cover
        })
    return JsonResponse({ 'info': listLove })
