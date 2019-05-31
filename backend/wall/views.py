from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from utils.utils import *
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
    if nickname == 'Anony' or nickname == 'anony':
        return HttpResponse(3)
    if User.objects.filter(nickname=nickname).exists():
        return HttpResponse(4)

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
        return HttpResponse(5)



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
def logout(request):
    del request.session['uid']
    return HttpResponse(0)



@csrf_exempt
def getUserBaseInfo(request):
    uid = request.session.get('uid', None)

    if (uid):
        try:
            user = User.objects.get(id=uid)
            return JsonResponse({
                'uid': uid,
                'nickname': user.nickname,
                'avatar': user.avatar.url
            })
        except:
            return HttpResponse(1)
    else:
        return JsonResponse({
                'uid': -1,
                'nickname': '赶快登陆吧～',
                'avatar': '/media/img/avatar/anony.jpg'
            })



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
def getUserProfile(request):
    uid = request.POST.get('uid')

    try:
        user = User.objects.get(id=uid)
        # comments
        comments = []
        for comment in user.comments.all():
            comments.append({
                'uid': comment.user.id,
                'avatar': comment.user.avatar.url,
                'nickname': comment.user.nickname,
                'content': comment.content
            })
        # loves
        loves = []
        for love in Love.objects.filter(userFrom=user):
            # not anonymous
            if not love.isAnony:
                # userTo
                if love.userTo:
                    userToID = love.userTo.id
                    userToNickname = love.userTo.nickname
                    userToAvatar = love.userTo.avatar
                else:
                    userToID = -1
                    userToNickname = "Anony"
                    userToAvatar = '/media/img/avatar/anony.jpg'

                loves.append({
                    'userTo_uid': userToID,
                    'userTo_nickname': userToNickname,
                    'userTo_avatar': userToAvatar,
                    'content': love.content
                })
        # loses
        loses = []
        for lose in Lose.objects.filter(user=user):
            loses.append({
                'id': lose.id,
                'isFound': lose.isFound,
                'name': lose.name,
                'description': lose.description
            })
        # deals
        deals = []
        for deal in Deal.objects.filter(user=user):
            deals.append({
                'id': deal.id,
                'isSold': deal.isSold,
                'name': deal.name,
                'description': deal.description
            })

        return JsonResponse({
            'uid': user.id,
            'nickname': user.nickname,
            'avatar': user.avatar.url,
            'email': user.email,
            'bio': user.bio,
            'phone': user.phone,
            'qq': user.qq,
            'wechat': user.wechat,
            'class': user._class,
            'comments': comments,
            'loves': loves,
            'loses': loses,
            'deals': deals
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def uploadLoveImg(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('files')
        name = formatName(file_obj.name)
        f = open(generateUploadPath('/img/loveImg/', name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        return HttpResponse(name)



@csrf_exempt
def removeLoveImg(request):
    name = request.POST.get('name')
    
    try:
        os.remove(generateUploadPath('/img/loveImg', name))
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def uploadLoseImg(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('files')
        name = formatName(file_obj.name)
        f = open(generateUploadPath('/img/loseImg/', name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        return HttpResponse(name)



@csrf_exempt
def removeLoseImg(request):
    name = request.POST.get('name')
    
    try:
        os.remove(generateUploadPath('/img/loseImg/', name))
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def uploadDealImg(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('files')
        name = formatName(file_obj.name)
        f = open(generateUploadPath('/img/dealImg/', name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        return HttpResponse(name)



@csrf_exempt
def removeDealImg(request):
    name = request.POST.get('name')
    
    try:
        os.remove(generateUploadPath('/img/dealImg/', name))
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitLove(request):
    isAnony = request.POST.get('anony')
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
            isAnony=isAnony,
            userFrom=UserFrom,
            userTo=UserTo,
            nameTo=userTo,
            content=content
        )
        if images:
            for image in images:
                love.images.add(Image.objects.create(name='/media/img/loveImg/' + image))

        return HttpResponse(0)
    except:
        return HttpResponse(2)



@csrf_exempt
def submitLose(request):
    uid = request.POST.get('uid')
    date = request.POST.get('date')
    name = request.POST.get('name')
    description = request.POST.get('description')
    images = request.POST.getlist('images[]')

    try:
        lose = Lose.objects.create(
            user = User.objects.get(id=uid),
            date=date,
            name=name,
            description=description
        )
        if images:
            for image in images:
                lose.images.add(Image.objects.create(name='/media/img/loseImg/' + image))

        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitDeal(request):
    uid = request.POST.get('uid')
    name = request.POST.get('name')
    price = request.POST.get('price')
    new = request.POST.get('new')
    description = request.POST.get('description')
    images = request.POST.getlist('images[]')

    try:
        deal = Deal.objects.create(
            user=User.objects.get(id=uid),
            name=name,
            price=price,
            new=new,
            description=description
        )
        if images:
            for image in images:
                deal.images.add(Image.objects.create(name='/media/img/dealImg/' + image))
        
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def getLoveList(request):
    index = int(request.POST.get('index'))

    if (index >= Love.objects.count()):
        return JsonResponse({ 'info': [] })

    listLove = []
    for love in Love.objects.all()[index:index+9]:
        # cover
        if love.images.count():
            cover = love.images.first().name
        else:
            cover = ''
        # userFrom
        if love.isAnony:
            userFromID = -1
            userFromNickname = 'Anony'
            userFromAvatar = '/media/img/avatar/anony.jpg'
            userFromBio = 'TA匿名了呢～'
        else:
            userFromID = love.userFrom.id
            userFromNickname = love.userFrom.nickname
            userFromAvatar = love.userFrom.avatar.url
            userFromBio = love.userFrom.bio
        # userTo
        if love.userTo:
            userToID = love.userTo.id
            userToNickname = love.userTo.nickname
            userToAvatar = love.userTo.avatar.url
            userToBio = love.userTo.bio
        else:
            userToID = -1
            userToNickname = 'Anony'
            userToAvatar = '/media/img/avatar/anony.jpg'
            userToBio = 'TA还没有来呢～'
        # is thumbsUp
        uid = request.session.get('uid', None)
        if uid:
            user = User.objects.get(id=uid)
            isThumbsUp = love.thumbsUpUser.filter(id=user.id).exists()
        else:
            isThumbsUp = False
        listLove.append({
            'id': love.id,
            'userFrom_uid': userFromID,
            'userFrom_nickname': userFromNickname,
            'userFrom_avatar': userFromAvatar,
            'userFrom_bio': userFromBio,
            'userTo_uid': userToID,
            'userTo_nickname': userToNickname,
            'userTo_avatar': userToAvatar,
            'userTo_bio': userToBio,
            'nameTo': love.nameTo,
            'content': love.content,
            'cover': cover,
            'thumbsUp': love.thumbsUpUser.count(),
            'comments': love.comments.count(),
            'isThumbsUp': isThumbsUp
        })
    return JsonResponse({ 'info': listLove })



@csrf_exempt
def getLoseList(request):
    index = int(request.POST.get('index'))

    if (index >= Lose.objects.count()):
        return JsonResponse({ 'info': [] })

    listLose = []
    for lose in Lose.objects.all()[index:index+9]:
        # cover
        if lose.images.count():
            cover = lose.images.first().name
        else:
            cover = ''

        listLose.append({
            'id': lose.id,
            'isFound': lose.isFound,
            'avatar': lose.user.avatar.url,
            'date': lose.date,
            'name': lose.name,
            'description': lose.description,
            'cover': cover
        })
    return JsonResponse({ 'info': listLose })



@csrf_exempt
def getDealList(request):
    index = int(request.POST.get('index'))

    if (index >= Deal.objects.count()):
        return JsonResponse({ 'info': [] })
    
    listDeal = []
    for deal in Deal.objects.all()[index:index+9]:
        # cover
        if deal.images.count():
            cover = deal.images.first().name
        else:
            cover = ''
        
        listDeal.append({
            'id': deal.id,
            'isSold': deal.isSold,
            'avatar': deal.user.avatar.url,
            'name': deal.name,
            'price': deal.price,
            'new': deal.new,
            'description': deal.description,
            'cover': cover
        })

    return JsonResponse({ 'info': listDeal })



@csrf_exempt
def getLoveDetail(request):
    _id = request.POST.get('id')

    try:
        love = Love.objects.get(id=_id)
        # userFrom
        if love.isAnony:
            userFromNickname = 'Anony'
            userFromAvatar = '/media/img/avatar/anony.jpg'
            userFromBio = 'TA匿名了呢～'
        else:
            userFromNickname = love.userFrom.nickname
            userFromAvatar = love.userFrom.avatar.url
            userFromBio = love.userFrom.bio
        # userTo
        if love.userTo:
            userToNickname = love.userTo.nickname
            userToAvatar = love.userTo.avatar.url
            userToBio = love.userTo.bio
        else:
            userToNickname = 'Anony'
            userToAvatar = '/media/img/avatar/anony.jpg'
            userToBio = 'TA还没有来呢～'
        # is thumbsUp
        uid = request.session.get('uid', None)
        if uid:
            user = User.objects.get(id=uid)
            isThumbsUp = love.thumbsUpUser.filter(id=user.id).exists()
        else:
            isThumbsUp = False
        # comments
        comments = []
        for comment in love.comments.all():
            comments.append({
                'uid': comment.user.id,
                'avatar': comment.user.avatar.url,
                'nickname': comment.user.nickname,
                'content': comment.content
            })

        return JsonResponse({
            'id': love.id,
            'userFrom_nickname': userFromNickname,
            'userFrom_avatar': userFromAvatar,
            'userFrom_bio': userFromBio,
            'userTo_nickname': userToNickname,
            'userTo_avatar': userToAvatar,
            'userTo_bio': userToBio,
            'nameTo': love.nameTo,
            'content': love.content,
            'images': list(love.images.all().values_list('name', flat=True)),
            'thumbsUp': love.thumbsUpUser.count(),
            'isThumbsUp': isThumbsUp,
            'comments': comments
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getLoseDetail(request):
    _id = request.POST.get('id')

    try:
        lose = Lose.objects.get(id=_id)
        # comments
        comments = []
        for comment in lose.comments.all():
            comments.append({
                'uid': comment.user.id,
                'avatar': comment.user.avatar.url,
                'nickname': comment.user.nickname,
                'content': comment.content
            })
        
        return JsonResponse({
            'id': lose.id,
            'isFound': lose.isFound,
            'uid': lose.user.id,
            'nickname': lose.user.nickname,
            'bio': lose.user.bio,
            'avatar': lose.user.avatar.url,
            'date': lose.date,
            'name': lose.name,
            'description': lose.description,
            'images': list(lose.images.all().values_list('name', flat=True)),
            'comments': comments
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getDealDetail(request):
    _id = request.POST.get('id')

    try:
        deal = Deal.objects.get(id=_id)
        # comments
        comments = []
        for comment in deal.comments.all():
            comments.append({
                'uid': comment.user.id,
                'avatar': comment.user.avatar.url,
                'nickname': comment.user.nickname,
                'content': comment.content
            })
        
        return JsonResponse({
            'id': deal.id,
            'isSold': deal.isSold,
            'uid': deal.user.id,
            'nickname': deal.user.nickname,
            'bio': deal.user.bio,
            'avatar': deal.user.avatar.url,
            'name': deal.name,
            'price': deal.price,
            'new': deal.new,
            'description': deal.description,
            'images': list(deal.images.all().values_list('name', flat=True)),
            'comments': comments
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def thumbsUp(request):
    _id = request.POST.get('id')
    isThumbsUp = request.POST.get('isThumbsUp')

    uid = request.session.get('uid', None)
    if uid:
        user = User.objects.get(id=uid)
        try:
            love = Love.objects.get(id=_id)
            if (isThumbsUp):
                love.thumbsUpUser.add(user)
            else:
                love.thumbsUpUser.remove(user)
            return HttpResponse(0)
        except:
            return HttpResponse(1)
    else:
        return HttpResponse(1)



@csrf_exempt
def submitUserComment(request):
    uidTo = request.POST.get('uidTo')
    uidFrom = request.POST.get('uidFrom')
    content = request.POST.get('content')

    try:
        userTo = User.objects.get(id=uidTo)
        userFrom = User.objects.get(id=uidFrom)
        comment = Comment.objects.create(user=userFrom, content=content)
        userTo.comments.add(comment)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitLoveComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        love = Love.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        love.comments.add(comment)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitLoseComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        lose = Lose.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        lose.comments.add(comment)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitDealComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        deal = Deal.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        deal.comments.add(comment)
        return HttpResponse(0)
    except:
        return HttpResponse(1)
