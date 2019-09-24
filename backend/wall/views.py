from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import *
from utils.utils import *
from datetime import timedelta
import os, random, datetime, pytz, math
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

    if uid:
        try:
            user = User.objects.get(id=uid)
            return JsonResponse({
                'uid': uid,
                'nickname': user.nickname,
                'avatar': user.avatar.url,
                'unreadCount': user.messages.filter(isRead=False).count(),
                'isAdmin': user.isAdmin
            })
        except:
            return HttpResponse(1)
    else:
        return JsonResponse({
                'uid': -1,
                'nickname': '赶快登陆吧～',
                'avatar': '/media/img/avatar/anony.jpg',
                'isAdmin': False
            })



@csrf_exempt
def updateUser(request):
    uid = request.POST.get('uid')
    nickname = request.POST.get('nickname')
    bio = request.POST.get('bio')
    _class = request.POST.get('class[0]') + '/' + request.POST.get('class[1]')
    phone = request.POST.get('phone')
    qq = request.POST.get('qq')
    wechat = request.POST.get('wechat')

    try:
        user = User.objects.get(id=uid)
        user.nickname = nickname
        user.bio = bio
        user._class = _class
        user.phone = phone
        user.qq = qq
        user.wechat = wechat

        user.save()
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def changePassword(request):
    uid = request.POST.get('uid')
    originPassword = request.POST.get('originPassword')
    password = request.POST.get('password')

    try:
        user = User.objects.get(id=uid)
        if user.password == originPassword:
            user.password = password
            user.save()
            return HttpResponse(0)
        else:
            return HttpResponse(1)
    except:
        return HttpResponse(2)



@csrf_exempt
def getMessage(request):
    uid = request.session.get('uid', None)
    messageList = []
    try:
        for message in User.objects.get(id=uid).messages.all():
            messageList.append({
                'user': { 'uid': message.user.id, 'nickname': message.user.nickname, 'bio': message.user.bio, 'avatar': message.user.avatar.url },
                'messageType': message.messageType,
                'messageFrom': message.messageFrom,
                'messageID': message.messageID,
                'commentContent': message.commentContent,
                'date': message.date
            })
            if not message.isRead:
                message.isRead = True
                message.save()
        return JsonResponse({ 'info': messageList })
    except:
        return HttpResponse(1)



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
def searchArticle(request):
    name = request.POST.get('name')

    listArticle = []
    try:
        for article in Article.objects.filter(title__contains=name):
            listArticle.append({
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
            'list': listArticle,
            'total': len(listArticle)
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def searchArticleByUser(request):
    name = request.POST.get('name')

    listArticle = []
    try:
        for article in Article.objects.filter(user__nickname__contains=name):
            listArticle.append({
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
            'list': listArticle,
            'total': len(listArticle)
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def searchArticleByTag(request):
    tags = request.POST.getlist('tags[]')

    allArticles = Article.objects.all()
    for tag in tags:
        allArticles = allArticles.filter(tags__contains=tag)
    
    listArticle = []
    for article in allArticles:
        listArticle.append({
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
        'list': listArticle,
        'total': len(listArticle)
    })



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
        # helps
        helps = []
        for _help in Help.objects.filter(user=user):
            helps.append({
                'id': _help.id,
                'title': _help.title,
                'content': _help.content
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
            'auth': user.auth.split(';') if user.auth else None,
            'comments': comments,
            'loves': loves,
            'loses': loses,
            'deals': deals,
            'helps': helps
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
    numQuestion = int(request.POST.get('numQuestion'))
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
        if _type == 'total':
            for bank in banks:
                allQuestions = Bank.objects.filter(bank=bank)
                singleA = allQuestions.filter(questionType='singleA')
                singleB = allQuestions.filter(questionType='singleB')
                multiple = allQuestions.filter(questionType='multiple')
                blank = allQuestions.filter(questionType='blank')
                judge = allQuestions.filter(questionType='judge')
                qa = allQuestions.filter(questionType='qa')

                questions_singleA.extend(list(singleA.values()[0:int(singleA.count()*freSingleA)]))
                questions_singleB.extend(list(singleB.values()[0:int(singleB.count()*freSingleB)]))
                questions_multiple.extend(list(multiple.values()[0:int(multiple.count()*freMultiple)]))
                questions_blank.extend(list(blank.values()[0:int(blank.count()*freMultiple)]))
                questions_judge.extend(list(judge.values()[0:int(judge.count()*freJudge)]))
                questions_qa.extend(list(qa.values()[0:int(qa.count()*freQA)]))
        elif _type == 'random':
            for index, bank in enumerate(banks):
                allQuestions = Bank.objects.filter(bank=bank)
                if index == 0:
                    singleA = allQuestions.filter(questionType='singleA')
                    singleB = allQuestions.filter(questionType='singleB')
                    multiple = allQuestions.filter(questionType='multiple')
                    blank = allQuestions.filter(questionType='blank')
                    judge = allQuestions.filter(questionType='judge')
                    qa = allQuestions.filter(questionType='qa')
                else:
                    singleA = singleA | allQuestions.filter(questionType='singleA')
                    singleB = singleB | allQuestions.filter(questionType='singleB')
                    multiple = multiple | allQuestions.filter(questionType='multiple')
                    blank = blank | allQuestions.filter(questionType='blank')
                    judge = judge | allQuestions.filter(questionType='judge')
                    qa = qa | allQuestions.filter(questionType='qa')
            # random all questions
            random.shuffle(singleA)
            random.shuffle(singleB)
            random.shuffle(multiple)
            random.shuffle(blank)
            random.shuffle(judge)
            random.shuffle(qa)

            questions_singleA.extend(list(singleA.values()[0:math.ceil(numQuestion*freSingleA)]))
            questions_singleB.extend(list(singleB.values()[0:math.ceil(numQuestion*freSingleB)]))
            questions_multiple.extend(list(multiple.values()[0:math.ceil(numQuestion*freMultiple)]))
            questions_blank.extend(list(blank.values()[0:math.ceil(numQuestion*freBlank)]))
            questions_judge.extend(list(judge.values()[0:math.ceil(numQuestion*freJudge)]))
            questions_qa.extend(list(qa.values()[0:math.ceil(numQuestion*freQA)]))

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
    qa = questions['qa']

    try:
        for question in singleA:
            answer = Bank.objects.get(id=question['id']).answer
            if answer == question['answer']:
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in singleB:
            pass
        for question in multiple:
            answer = Bank.objects.get(id=question['id']).answer
            question['answer'].sort()
            if answer == ''.join(question['answer']):
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in judge:
            answer = Bank.objects.get(id=question['id']).answer
            if answer == question['answer']:
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        for question in blank:
            answer = Bank.objects.get(id=question['id']).answer
            if answer == question['answer']:
                question['isCorrect'] = True
            else:
                question['isCorrect'] = False
                question['correctAnswer'] = answer
        
        return JsonResponse({ 
            'singleA': singleA,
            'singleB': singleB,
            'multiple': multiple,
            'judge': judge,
            'blank': blank,
            'qa': qa
         })
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
def submitHelp(request):
    uid = request.POST.get('uid')
    title = request.POST.get('title')
    content = request.POST.get('content')

    try:
        Help.objects.create(
            user = User.objects.get(id=uid),
            title = title,
            content = content
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
    filterType = request.POST.get('filterType')
    order = request.POST.get('order')
    index = int(request.POST.get('index'))


    listArticle = []
    articles = []
    if filterType == 'date':
        if order == 'positive':
            articles = Article.objects.order_by('publicDate')[index:index+9]
        elif order == 'reverse':
            articles = Article.objects.order_by('-publicDate')[index:index+9]
    elif filterType == 'thumbsUp':
        if order == 'positive':
            articles = Article.objects.annotate(numThumbsUp = Count('thumbsUpUser')).order_by('numThumbsUp')[index:index+9]
        elif order == 'reverse':
            articles = Article.objects.annotate(numThumbsUp = Count('thumbsUpUser')).order_by('-numThumbsUp')[index:index+9]
    elif filterType == 'coin':
        if order == 'positive':
            articles = Article.objects.order_by('neededCoin')[index:index+9]
        elif order == 'reverse':
            articles = Article.objects.order_by('-neededCoin')[index:index+9]
    else:
        articles = Article.objects.all()[index:index+9]

    try:
        for article in articles:
            listArticle.append({
                'id': article.id,
                'user': { 'uid': article.user.id, 'avatar': article.user.avatar.url, 'nickname': article.user.nickname, 'bio': article.user.bio, 'auth': article.user.auth.split(';') },
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
            'list': listArticle,
            'total': Article.objects.count()
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getHelpList(request):
    filterType = request.POST.get('filterType')
    order = request.POST.get('order')
    index = int(request.POST.get('index'))

    listHelp = []
    helps = []
    if filterType == 'date':
        if order == 'positive':
            helps = Help.objects.order_by('date')[index:index+9]
        elif order == 'reverse':
            helps = Help.objects.order_by('-date')[index:index+9]
    else:
        helps = Help.objects.all()[index:index+9]

    try:
        for _help in helps:
            listHelp.append({
                'id': _help.id,
                'user': { 'uid': _help.user.id, 'avatar': _help.user.avatar.url, 'nickname': _help.user.nickname, 'bio': _help.user.bio },
                'title': _help.title,
                'content': _help.content,
                'date': _help.date,
                'comments': _help.comments.count()
            })

        return JsonResponse({
            'list': listHelp,
            'total': Help.objects.count()
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
                'content': comment.content,
                'date': comment.date
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
                'content': comment.content,
                'date': comment.date
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
                'content': comment.content,
                'date': comment.date
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
                'content': comment.content,
                'date': comment.date
            })

        return JsonResponse({
            'id': article.id,
            'user': { 'uid': article.user.id, 'nickname': article.user.nickname, 'bio': article.user.bio, 'avatar': article.user.avatar.url, 'auth': article.user.auth.split(';') if article.user.auth else None },
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
        try:
            user = User.objects.get(id=uid)
            love = Love.objects.get(id=_id)
            if (isThumbsUp):
                love.thumbsUpUser.add(user)
                # message
                message = Message.objects.create(
                    user=user,
                    messageType='thumbsUp',
                    messageFrom='love',
                    messageID=_id
                )
                love.userFrom.messages.add(message)
                for userTo in love.userTo.all():
                    userTo.messages.add(message)
            else:
                love.thumbsUpUser.remove(user)
                love.userFrom.messages.remove(Message.objects.get(messageID=_id))
                for userTo in love.userTo.all():
                    userTo.messages.remove(Message.objects.get(messageID=_id))
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
        try:
            user = User.objects.get(id=uid)
            article = Article.objects.get(id=_id)
            if (isThumbsUp):
                article.thumbsUpUser.add(user)
                # message
                message = Message.objects.create(
                    user=user,
                    messageType='thumbsUp',
                    messageFrom='love',
                    messageID=_id
                )
                article.user.messages.add(message)
            else:
                article.thumbsUpUser.remove(user)
                article.user.messages.remove(Message.objects.get(messageID=_id))
            return HttpResponse(0)
        except:
            return HttpResponse(1)
    else:
        return HttpResponse(1)



@csrf_exempt
def getHelpDetail(request):
    _id = request.POST.get('id')

    try:
        _help = Help.objects.get(id=_id)
        # comments
        comments = []
        for comment in _help.comments.all():
            comments.append({
                'uid': comment.user.id,
                'avatar': comment.user.avatar.url,
                'nickname': comment.user.nickname,
                'content': comment.content,
                'date': comment.date
            })

        return JsonResponse({
            'id': _help.id,
            'user': { 'uid': _help.user.id, 'avatar': _help.user.avatar.url, 'nickname': _help.user.nickname, 'bio': _help.user.bio, 'auth': _help.user.auth.split(';') if _help.user.auth else None },
            'title': _help.title,
            'content': _help.content,
            'date': _help.date,
            'comments': comments
        })
    except:
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
        # comment
        love = Love.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        love.comments.add(comment)
        # message
        message = Message.objects.create(
            user=user,
            messageType='comment',
            messageFrom='love',
            messageID=_id,
            commentContent=content,
        )
        love.userFrom.messages.add(message)
        for userTo in love.userTo.all():
            userTo.messages.add(message)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitLoseComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        # comment
        lose = Lose.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        lose.comments.add(comment)
        # message
        message = Message.objects.create(
            user=user,
            messageType='comment',
            messageFrom='lose',
            messageID=_id,
            commentContent=content,
        )
        lose.user.messages.add(message)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitDealComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        # comment
        deal = Deal.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        deal.comments.add(comment)
        # message
        message = Message.objects.create(
            user=user,
            messageType='comment',
            messageFrom='deal',
            messageID=_id,
            commentContent=content,
        )
        deal.user.messages.add(message)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitArticleComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        # comment
        article = Article.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        article.comments.add(comment)
        # message
        message = Message.objects.create(
            user=user,
            messageType='comment',
            messageFrom='article',
            messageID=_id,
            commentContent=content,
        )
        article.user.messages.add(message)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def submitHelpComment(request):
    _id = request.POST.get('id')
    uid = request.POST.get('uid')
    content = request.POST.get('content')

    try:
        # comment
        _help = Help.objects.get(id=_id)
        user = User.objects.get(id=uid)
        comment = Comment.objects.create(user=user, content=content)
        _help.comments.add(comment)
        # message
        message = Message.objects.create(
            user=user,
            messageType='comment',
            messageFrom='help',
            messageID=_id,
            commentContent=content,
        )
        _help.user.messages.add(message)
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def getClubDetail(request):
    name = request.POST.get('name')

    try:
        club = Club.objects.get(name=name)
        return JsonResponse({
            'name': club.name,
            'description': club.description,
            'president_uid': club.president.id,
            'president_name': club.president.nickname,
            'president_avatar': club.president.avatar,
            'vicePresident_uid': club.vicePresident.id,
            'vicePresident_name': club.vicePresident.nickname,
            'vicePresident_avatar': club.vicePresident.avatar,
            'presidentAssistant_uid': club.presidentAssistant.id,
            'presidentAssistant_name': club.presidentAssistant.nickname,
            'presidentAssistant_avatar': club.presidentAssistant.avatar,
            'planDirector_uid': club.planDirector.id,
            'planDirector_name': club.planDirector.nickname,
            'planDirector_avatar': club.planDirector.avatar,
            'financeDirector_uid': club.financeDirector.id,
            'financeDirector_name': club.financeDirector.nickname,
            'financeDirector_avatar': club.financeDirector.avatar,
            'feedbackDirector_uid': club.feedbackDirector.id,
            'feedbackDirector_name': club.feedbackDirector.nickname,
            'feedbackDirector_avatar': club.feedbackDirector.avatar,
            'ITDirector_uid': club.ITDirector.id,
            'ITDirector_name': club.ITDirector.nickname,
            'ITDirector_avatar': club.ITDirector.avatar,
            'propagandaDirector_uid': club.propagandaDirector.id,
            'propagandaDirector_name': club.propagandaDirector.nickname,
            'propagandaDirector_avatar': club.propagandaDirector.avatar,
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getHotList(request):
    listHot = []
    try:
        for hot in Hot.objects.all():
            listHot.append({
                'key': hot.id,
                'title': hot.title,
                'publisher': { 'uid': hot.publisher.id, 'nickname': hot.publisher.nickname, 'avatar': hot.publisher.avatar.url },
                'date': hot.date
            })
        return JsonResponse({ 'info': listHot })
    except:
        return HttpResponse(1)



@csrf_exempt
def getHotDetail(request):
    _id = request.POST.get('id')
    try:
        hot = Hot.objects.get(id=_id)
        return JsonResponse({
            'title': hot.title,
            'content': hot.content,
            'publisher': { 'uid': hot.publisher.id, 'nickname': hot.publisher.nickname, 'avatar': hot.publisher.avatar.url },
            'date': hot.date
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def deleteHot(request):
    _id = request.POST.get('id')
    try:
        hot = Hot.objects.get(id=_id)
        hot.delete()
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def addHot(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    publisherUID = request.POST.get('publisherUID')

    try:
        if Hot.objects.filter(title=title).exists():
            hot = Hot.objects.get(title=title)
            hot.title = title
            hot.content = content
            hot.publisher = User.objects.get(id=publisherUID)
            hot.save()
        else:
            Hot.objects.create(
                title = title,
                content = content,
                publisher = User.objects.get(id=publisherUID)
            )
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def getUserList(request):
    listUser = []
    try:
        for user in User.objects.all():
            listUser.append({
                'key': user.id,
                'email': user.email,
                'nickname': user.nickname,
                'bio': user.bio,
                'class': user._class,
                'phone': user.phone,
                'qq': user.qq,
                'wechat': user.wechat,
                'coin': user.coin,
                'isAdmin': user.isAdmin,
                'auth': user.auth
            })
        return JsonResponse({ 'info': listUser })
    except:
        return HttpResponse(1)



@csrf_exempt
def getUserDetail(request):
    _id = request.POST.get('uid')
    try:
        user = User.objects.get(id=_id)
        return JsonResponse({
            'email': user.email,
            'nickname': user.nickname,
            'bio': user.bio,
            'class': user._class.split('/'),
            'phone': user.phone,
            'qq': user.qq,
            'wechat': user.wechat,
            'coin': user.coin,
            'isAdmin': user.isAdmin,
            'auth': user.auth
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def updateUserAdmin(request):
    uid = request.POST.get('uid')
    email = request.POST.get('email')
    nickname = request.POST.get('nickname')
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
            user.nickname = nickname
            user.bio = bio
            user._class = _class
            user.phone = phone
            user.qq = qq
            user.wechat = wechat
            user.coin = coin
            user.isAdmin = isAdmin
            user.auth = auth

            user.save()
            return HttpResponse(0)
    except:
        return HttpResponse(1)


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
def getLectureList(request):
    listLecture = []
    try:
        for lecture in Lecture.objects.all():
            lectureDate = lecture.date
            currentDate = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))

            if currentDate < lectureDate:
                state = 'wait'
            elif currentDate > lectureDate:
                state = 'done'
            elif currentDate == lectureDate:
                state = 'running'

            listLecture.append({
                'key': lecture.id,
                'title': lecture.title,
                'lecturer': lecture.lecturer,
                'address': lecture.address,
                'date': lecture.date,
                'state': state
            })
            return JsonResponse({ 'info': listLecture })
    except:
        return HttpResponse(1)



@csrf_exempt
def getLectureDetail(request):
    _id = request.POST.get('id')
    try:
        lecture = Lecture.objects.get(id=_id)
        return JsonResponse({
            'title': lecture.title,
            'lecturer': lecture.lecturer,
            'address': lecture.address,
            'date': lecture.date
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def addLecture(request):
    title = request.POST.get('title')
    lecturer = request.POST.get('lecturer')
    address = request.POST.get('address')
    date = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d %H:%M:%S')

    try:
        if Lecture.objects.filter(title=title).exists():
            lecture = Lecture.objects.get(title=title)
            lecture.title = title
            lecture.lecturer = lecturer
            lecture.address = address
            lecture.date = date
            lecture.save()
        else:
            Lecture.objects.create(
                title = title,
                lecturer = lecturer,
                address = address,
                date = date
            )
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def deleteLecture(request):
    _id = request.POST.get('id')
    try:
        lecture = Lecture.objects.get(id=_id)
        lecture.delete()
        return HttpResponse(0)
    except:
        return HttpResponse(1)
