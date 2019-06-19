from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import *
from utils.utils import *
from datetime import timedelta
import os, random

import json

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
        # nickname
        listNickname = []
        for user in User.objects.filter(nickname__contains=user):
            listNickname.append(user.nickname)
        return JsonResponse({ 'info': listNickname })
    except:
        return JsonResponse({ 'info': [] })



@csrf_exempt
def searchLoveItem(request):
    name = request.POST.get('name')
    _object = request.POST.get('object')

    loves = []
    listLove = []
    try:
        if _object == 'from':
            loves = Love.objects.filter(userFrom__nickname__contains=name)
        elif _object == 'to':
            loves = Love.objects.filter(userTo__nickname__contains=name)
            loves = loves | Love.objects.filter(nameTo__contains=name)

        for love in loves:
            # cover
            if love.images.count():
                cover = love.images.first().name
            else:
                cover = ''
            # userFrom
            if love.isAnony and _object == 'from':
                continue
            elif love.isAnony and _object == 'to':
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
            userTos = []
            if love.userTo:
                for user in love.userTo.all():
                    userTos.append({
                        'uid': user.id,
                        'nickname': user.nickname,
                        'avatar': user.avatar.url,
                        'bio': user.bio
                    })
            if love.nameTo:
                for user in love.nameTo.split(';'):
                    if user:
                        userTos.append({
                            'uid': -1,
                            'nickname': user,
                            'avatar': '/media/img/avatar/anony.jpg',
                            'bio': 'TA还没有来呢～'
                        })
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
                'userTo': userTos,
                'content': love.content,
                'cover': cover,
                'thumbsUp': love.thumbsUpUser.count(),
                'comments': love.comments.count(),
                'isThumbsUp': isThumbsUp
            })
            
        return JsonResponse({ 'info': listLove })
    except:
        return HttpResponse(1)



@csrf_exempt
def searchLoseItem(request):
    name = request.POST.get('name')

    listLose = []
    try:
        for lose in Lose.objects.filter(name__contains=name):
            # cover
            if lose.images.count():
                cover = lose.images.first().name
            else:
                cover = ''

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
        
        return JsonResponse({ 'info': listLose })
    except:
        return HttpResponse(1)



@csrf_exempt
def searchDealItem(request):
    name = request.POST.get('name')

    listDeal = []
    try:
        for deal in Deal.objects.filter(name__contains=name):
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
    except:
        return HttpResponse(1)



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
                if love.userTo:
                    for userTo in love.userTo.all():
                        loves.append({
                            'userTo_uid': userTo.id,
                            'userTo_nickname': userTo.nickname,
                            'userTo_avatar': userTo.avatar.url,
                            'content': love.content
                        })
                if love.nameTo:
                    for userTo in love.nameTo.split(';'):
                        if userTo:
                            loves.append({
                                'userTo_uid': -1,
                                'userTo_nickname': userTo,
                                'userTo_avatar': '/media/img/avatar/anony.jpg',
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
            'coin': user.coin,
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
    isAnony = True if request.POST.get('isAnony') == 'true' else False
    userTos = request.POST.getlist('userTo[]')
    content = request.POST.get('content')
    images = request.POST.getlist('images[]')

    try:
        # get userFrom
        UserFrom = User.objects.get(id=request.session.get('uid', None))
        # get userTo
        listUserTo = []
        nameTo = ''
        for userTo in userTos:
            user = User.objects.filter(nickname=userTo)
            if user.exists():
                listUserTo.append(user[0])
            else:
                nameTo = nameTo + userTo + ';'
    except:
        return HttpResponse(1)
    # create
    try:
        love = Love.objects.create(
            isAnony=isAnony,
            userFrom=UserFrom,
            nameTo=nameTo,
            content=content
        )
        # userTos
        for userTo in listUserTo:
            love.userTo.add(userTo)
        # images
        for image in images:
            love.images.add(Image.objects.create(name='/media/img/loveImg/' + image))

        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitLose(request):
    uid = request.POST.get('uid')
    loseDate = request.POST.get('loseDate')
    name = request.POST.get('name')
    description = request.POST.get('description')
    images = request.POST.getlist('images[]')

    try:
        lose = Lose.objects.create(
            user = User.objects.get(id=uid),
            loseDate=loseDate,
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
def submitBank(request):
    _type = request.POST.get('type')
    banks = request.POST.getlist('banks[]')
    numQuestion = request.POST.get('numQuestion')
    freSingleA = float(request.POST.get('singleA')) / 100.0
    freSingleB = float(request.POST.get('singleB')) / 100.0
    freMultiple = float(request.POST.get('multiple')) / 100.0
    freBlank = float(request.POST.get('blank')) / 100.0
    freJudge = float(request.POST.get('judge')) / 100.0
    freQA = float(request.POST.get('qa')) / 100.0
    
    questions_singleA = []
    questions_singleB = []
    questions_multiple = []
    questions_blank = []
    questions_judge = []
    questions_qa = []
    try:
        if (_type == 'total'):
            for bank in banks:
                allQuestions = Bank.objects.filter(bank=bank)
                singleA = allQuestions.filter(questionType='singleA')
                singleB = allQuestions.filter(questionType='singleB')
                multiple = allQuestions.filter(questionType='multiple')
                blank = allQuestions.filter(questionType='blank')
                judge = allQuestions.filter(questionType='judge')
                qa = allQuestions.filter(questionType='qa')

                questions_singleA.extend(list(singleA[0:int(singleA.count()*freSingleA)].values()))
                questions_singleB.extend(list(singleB[0:int(singleB.count()*freSingleB)].values()))
                questions_multiple.extend(list(multiple[0:int(multiple.count()*freMultiple)].values()))
                questions_blank.extend(list(blank[0:int(blank.count()*freMultiple)].values()))
                questions_judge.extend(list(judge[0:int(judge.count()*freJudge)].values()))
                questions_qa.extend(list(qa[0:int(qa.count()*freQA)].values()))
        elif (_type == 'random'):
            singleA, singleB, multiple, blank, judge, qa = []
            for bank in banks:
                allQuestions = Bank.objects.filter(bank=bank)
                singleA.extend(allQuestions.filter(questionType='singleA'))
                singleB.extend(allQuestions.filter(questionType='singleB'))
                multiple.extend(allQuestions.filter(questionType='multiple'))
                blank.extend(allQuestions.filter(questionType='blank'))
                judge.extend(allQuestions.filter(questionType='judge'))
                qa.extend(allQuestions.filter(questionType='qa'))
            # random all questions
            random.shuffle(singleA)
            random.shuffle(singleB)
            random.shuffle(multiple)
            random.shuffle(blank)
            random.shuffle(judge)
            random.shuffle(qa)
            
            questions_singleA.extend(list(singleA[0:int(numQuestion*freSingleA)].values()))
            questions_singleB.extend(list(singleB[0:int(numQuestion*freSingleB)].values()))
            questions_multiple.extend(list(multiple[0:int(numQuestion*freMultiple)].values()))
            questions_blank.extend(list(blank[0:int(numQuestion*freMultiple)].values()))
            questions_judge.extend(list(judge[0:int(numQuestion*freJudge)].values()))
            questions_qa.extend(list(qa[0:int(numQuestion*freQA)].values()))

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
        for question in questions_qa:
            question['answer'] = ''

        return JsonResponse({
            'singleA': questions_singleA,
            'singleB': questions_singleB,
            'multiple': questions_multiple,
            'blank': questions_blank,
            'judge': questions_judge,
            'qa': questions_qa
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def handExam(request):
    questions = json.loads(request.body)
    singleA = questions['singleA']
    singleB = questions['singleB']
    multiple = questions['multiple']
    judge = questions['judge']
    blank = questions['blank']

    print(singleA)
    print(multiple)
    print(judge)
    print(blank)

    return HttpResponse(0)

    try:
        questions = []
        for question in singleA:
            answer = Bank.objects.get(id=question.id)
            if answer == question.answer:
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in singleB:
            pass
        for question in multiple:
            answer = Bank.objects.get(id=question.id)
            answer = ''.join(answer.sort())
            if answer == question.answer:
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in judge:
            answer = Bank.objects.get(id=question.id)
            if answer == question.answer:
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in blank:
            pass
    except:
        return HttpResponse(1)



@csrf_exempt
def submitArticle(request):
    uid = request.POST.get('uid')
    title = request.POST.get('title')
    tags = request.POST.getlist('tages[]')
    content = request.POST.get('content')
    neededCoin = request.POST.get('neededCoin')

    try:
        Article.objects.create(
            user = User.objects.get(id=uid),
            title = title,
            tags = ';'.join(tags),
            content = content,
            neededCoin = neededCoin
        )
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def getLoveList(request):
    filterType = request.POST.get('filterType')
    order = request.POST.get('order')
    index = int(request.POST.get('index'))

    if (index >= Love.objects.count()):
        return JsonResponse({ 'info': [] })

    loves = []
    listLove = []
    if filterType == 'date':
        if order == 'positive':
            loves = Love.objects.order_by('date')[index:index+9]
        elif order == 'reverse':
            loves = Love.objects.order_by('-date')[index:index+9]
    elif filterType == 'thumbsUp':
        if order == 'positive':
            loves = Love.objects.annotate(numThumbsUp = Count('thumbsUpUser')).order_by('numThumbsUp')[index:index+9]
        elif order == 'reverse':
            loves = Love.objects.annotate(numThumbsUp = Count('thumbsUpUser')).order_by('-numThumbsUp')[index:index+9]
    else:
        loves = Love.objects.all()[index:index+9]

    for love in loves:
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
        userTos = []
        if love.userTo:
            for user in love.userTo.all():
                userTos.append({
                    'uid': user.id,
                    'nickname': user.nickname,
                    'avatar': user.avatar.url,
                    'bio': user.bio
                })
        if love.nameTo:
            for user in love.nameTo.split(';'):
                if user:
                    userTos.append({
                        'uid': -1,
                        'nickname': user,
                        'avatar': '/media/img/avatar/anony.jpg',
                        'bio': 'TA还没有来呢～'
                    })
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
            'userTo': userTos,
            'content': love.content,
            'cover': cover,
            'thumbsUp': love.thumbsUpUser.count(),
            'comments': love.comments.count(),
            'isThumbsUp': isThumbsUp
        })

    return JsonResponse({ 'info': listLove })



@csrf_exempt
def getLoseList(request):
    filterType = request.POST.get('filterType')
    order = request.POST.get('order')
    index = int(request.POST.get('index'))

    if (index >= Lose.objects.count()):
        return JsonResponse({ 'info': [] })

    loses = []
    listLose = []
    if filterType == 'loseTime':
        if order == 'positive':
            loses = Lose.objects.order_by('loseDate')[index:index+9]
        elif order == 'reverse':
            loses = Lose.objects.order_by('-loseDate')[index:index+9]
    elif filterType == 'publicTime':
        if order == 'positive':
            loses = Lose.objects.order_by('publicDate')[index:index+9]
        elif order == 'reverse':
            loses = Lose.objects.order_by('-publicDate')[index:index+9]
    elif filterType == 'isFound':
        if order == 'positive':
            loses = Lose.objects.order_by('isFound')[index:index+9]
        elif order == 'reverse':
            loses = Lose.objects.order_by('-isFound')[index:index+9]
    else:
        loses = Lose.objects.all()[index:index+9]

    for lose in loses:
        # cover
        if lose.images.count():
            cover = lose.images.first().name
        else:
            cover = ''

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

    return JsonResponse({ 'info': listLose })



@csrf_exempt
def getDealList(request):
    filterType = request.POST.get('filterType')
    order = request.POST.get('order')
    index = int(request.POST.get('index'))

    if (index >= Deal.objects.count()):
        return JsonResponse({ 'info': [] })
    
    deals = []
    listDeal = []
    if filterType == 'date':
        if order == 'positive':
            deals = Deal.objects.order_by('date')[index:index+9]
        elif order == 'reverse':
            deals = Deal.objects.order_by('-date')[index:index+9]
    elif filterType == 'new':
        if order == 'positive':
            deals = Deal.objects.order_by('new')[index:index+9]
        elif order == 'reverse':
            deals = Deal.objects.order_by('-new')[index:index+9]
    elif filterType == 'price':
        if order == 'positive':
            deals = Deal.objects.order_by('price')[index:index+9]
        elif order == 'reverse':
            deals = Deal.objects.order_by('-price')[index:index+9]
    elif filterType == 'isSold':
        if order == 'positive':
            deals = Deal.objects.order_by('isSold')[index:index+9]
        elif order == 'reverse':
            deals = Deal.objects.order_by('-isSold')[index:index+9]
    else:
        deals = Deal.objects.all()[index:index+9]

    for deal in deals:
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
def getArticleList(request):
    index = int(request.POST.get('index')) - 1

    listArtcile = []
    try:
        allArticles = Article.objects.all()
        for article in allArticles[index:index+9]:
            listArtcile.append({
                'id': article.id,
                'uid': article.user.id,
                'avatar': article.user.avatar.url,
                'nickname': article.user.nickname,
                'bio': article.user.bio,
                'title': article.title,
                'tags': article.tags.split(';')[:-1],
                'content': article.content,
                'neededCoin': article.neededCoin,
                'publicDate': article.publicDate,
                'editDate': article.editDate,
                'comments': article.comments.count(),
                'thumbsUp': article.thumbsUpUser.count(),
            })

        return JsonResponse({
            'list': listArtcile,
            'total': allArticles.count()
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getLoveDetail(request):
    _id = request.POST.get('id')

    try:
        love = Love.objects.get(id=_id)
        # userFrom
        if love.isAnony:
            userFromUID = -1
            userFromNickname = 'Anony'
            userFromAvatar = '/media/img/avatar/anony.jpg'
            userFromBio = 'TA匿名了呢～'
        else:
            userFromUID = love.userFrom.id
            userFromNickname = love.userFrom.nickname
            userFromAvatar = love.userFrom.avatar.url
            userFromBio = love.userFrom.bio
        # userTo
        userTos = []
        if love.userTo:
            for user in love.userTo.all():
                userTos.append({
                    'uid': user.id,
                    'nickname': user.nickname,
                    'avatar': user.avatar.url,
                    'bio': user.bio
                })
        if love.nameTo:
            for user in love.nameTo.split(';'):
                if user:
                    userTos.append({
                        'uid': -1,
                        'nickname': user,
                        'avatar': '/media/img/avatar/anony.jpg',
                        'bio': 'TA还没有来呢～'
                    })
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
            'userFrom_uid': userFromUID,
            'userFrom_nickname': userFromNickname,
            'userFrom_avatar': userFromAvatar,
            'userFrom_bio': userFromBio,
            'userTo': userTos,
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
            'publicDate': lose.publicDate,
            'loseDate': lose.loseDate,
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
def getArticleDetail(request):
    _id = request.POST.get('id')

    try:
        article = Article.objects.get(id=_id)
        # is thumbsUp
        uid = request.session.get('uid', None)
        if uid:
            user = User.objects.get(id=uid)
            isThumbsUp = article.thumbsUpUser.filter(id=user.id).exists()
        else:
            isThumbsUp = False
        # comments
        comments = []
        for comment in article.comments.all():
            comments.append({
                'uid': comment.user.id,
                'avatar': comment.user.avatar.url,
                'nickname': comment.user.nickname,
                'content': comment.content
            })

        return JsonResponse({
            'id': article.id,
            'uid': article.user.id,
            'nickname': article.user.nickname,
            'bio': article.user.bio,
            'avatar': article.user.avatar.url,
            'title': article.title,
            'tags': article.tags.split(';')[:-1],
            'content': article.content,
            'publicDate': article.publicDate,
            'editDate': article.editDate,
            'comments': comments,
            'thumbsUp': article.thumbsUpUser.count(),
            'isThumbsUp': isThumbsUp
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def thumbsUpLove(request):
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
def thumbsUpArticle(request):
    _id = request.POST.get('id')
    isThumbsUp = request.POST.get('isThumbsUp')

    uid = request.session.get('uid', None)
    if uid:
        user = User.objects.get(id=uid)
        try:
            article = Article.objects.get(id=_id)
            if (isThumbsUp):
                article.thumbsUpUser.add(user)
            else:
                article.thumbsUpUser.remove(user)
            return HttpResponse(0)
        except:
            return HttpResponse(1)
    else:
        return HttpResponse(1)



@csrf_exempt
def getNumQuestion(request):
    banks = request.POST.getlist('banks[]')

    quantity = 0
    for bank in banks:
        quantity += Bank.objects.filter(bank=bank).count()

    return HttpResponse(quantity)



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



@csrf_exempt
def submitArticleComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        article = Article.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        article.comments.add(comment)
        return HttpResponse(0)
    except:
        return HttpResponse(1)

