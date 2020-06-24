from django.db import models


class User(models.Model):
    openid = models.CharField(max_length=50, default=0)
    avatar = models.ImageField(upload_to='img/avatar', default='img/avatar/default.png')
    email = models.EmailField()
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    bio = models.CharField(max_length=100)
    gender = models.CharField(max_length=5, default='男')
    _class = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    coin = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments')
    messages = models.ManyToManyField('Message', blank=True, related_name='messages')
    errorBook = models.ManyToManyField('Bank', blank=True, related_name='errorBook')
    followings = models.ManyToManyField('User', blank=True, related_name='following')
    isAdmin = models.BooleanField(default=False)
    auth = models.CharField(max_length=50, blank=True, null=True)



class Love(models.Model):
    isAnony = models.BooleanField(default=False)
    userFrom = models.ForeignKey('User', on_delete=models.CASCADE, related_name='userFrom')
    userTo = models.ManyToManyField('User', blank=True, related_name='userTo')
    nameTo = models.CharField(max_length=20, default='TA')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField('Image', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    thumbsUpUser = models.ManyToManyField('User', blank=True)

    class Meta:
        ordering = ('-date',)



class Lose(models.Model):
    isFound = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()
    loseDate = models.CharField(max_length=20)
    publicDate = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField('Image', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)

    class Meta:
        ordering = ('-publicDate',)
    
    def __str__(self):
        return self.name



class Deal(models.Model):
    isSold = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.FloatField()
    new = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField('Image', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.name



class Bank_UpdateMessage(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.content



class Bank_Subject(models.Model):
    subjectType = (
        ('zy', '中医'),
        ('xy', '西医')
    )

    name = models.CharField(max_length=20)
    subjectType = models.CharField(max_length=10, choices=subjectType)

    def __str__(self):
        return self.name



class Bank_Chapter(models.Model):
    name = models.CharField(max_length=20)
    subject = models.ForeignKey('Bank_Subject', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Bank(models.Model):
    questionType = (
        ('singleA', '单选-题型A'),
        ('singleB', '单选-题型B'),
        ('multiple', '多选'),
        ('blank', '填空'),
        ('judge', '判断'),
        ('term', '名词解释'),
        ('qa', '问答'),
        ('case', '病案分析')
    )

    title = models.CharField(max_length=1000)
    A = models.CharField(max_length=50, blank=True)
    B = models.CharField(max_length=50, blank=True)
    C = models.CharField(max_length=50, blank=True)
    D = models.CharField(max_length=50, blank=True)
    E = models.CharField(max_length=50, blank=True)
    questionType = models.CharField(max_length=10, choices=questionType, default='singleA')
    isBlankSeq = models.BooleanField(default=True)
    # After sorting, 'A', 'AB' or 'blank'
    answer = models.TextField()
    chapter = models.ForeignKey('Bank_Chapter', on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class BankStatistics(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=20)
    allQuestions = models.IntegerField()
    correctQuestions = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.user.nickname



class Article(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    tags = models.CharField(max_length=50, default='')
    content = models.TextField()
    neededCoin = models.PositiveIntegerField(default=0)
    publicDate = models.DateTimeField(auto_now_add=True)
    editDate = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField('Comment', blank=True)
    thumbsUpUser = models.ManyToManyField('User', blank=True, related_name="thumbsUp")
    isAdopted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-publicDate',)

    def __str__(self):
        return self.title



class Help(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Comment', blank=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title



class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    president = models.ForeignKey('User', on_delete=models.CASCADE, related_name='president')
    vicePresident = models.ForeignKey('User', on_delete=models.CASCADE, related_name='vicePresident')
    presidentAssistant = models.ForeignKey('User', on_delete=models.CASCADE, related_name='presidentAssistant')
    planDirector = models.ManyToManyField('User', blank=True, related_name='planDirector')
    financeDirector = models.ManyToManyField('User', blank=True, related_name='financeDirector')
    feedbackDirector = models.ManyToManyField('User', blank=True, related_name='feedbackDirector')
    ITDirector = models.ManyToManyField('User', blank=True, related_name='ITDirector')
    propagandaDirector = models.ManyToManyField('User', blank=True, related_name='propagandaDirector')
    learningDirector = models.ManyToManyField('User', blank=True, related_name='learningDirector')

    def __str__(self):
        return self.name



class Hot(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    publisher = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title



class Lecture(models.Model):
    title = models.CharField(max_length=30)
    lecturer = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    date = models.DateTimeField()
    state = models.CharField(max_length=10)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title



class Image(models.Model):
    name = models.CharField(max_length=100, default='default')

    def __str__(self):
        return self.name



class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)



class Message(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # thumbsUp or comment
    messageType = models.CharField(max_length=10)
    # love, lose, deal, help, article
    messageFrom = models.CharField(max_length=10)
    messageID = models.IntegerField()
    commentContent = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)
