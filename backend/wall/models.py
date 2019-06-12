from django.db import models


class User(models.Model):
    avatar = models.ImageField(upload_to='img/avatar', default='img/avatar/default.png')
    email = models.EmailField()
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    bio = models.CharField(max_length=100)
    _class = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    coin = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField('Comment', blank=True, related_name='user_comments')



class Love(models.Model):
    isAnony = models.BooleanField(default=False)
    userFrom = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_from')
    userTo = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='user_to')
    nameTo = models.CharField(max_length=20, default='TA')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField('Image', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    thumbsUpUser = models.ManyToManyField('User', blank=True)



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
        ordering = ('-id',)
    
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
        ordering = ('-id',)
    
    def __str__(self):
        return self.name



class Bank(models.Model):
    questionType = (
        ('singleA', '单选-题型A'),
        ('singleB', '单选-题型B'),
        ('multiple', '多选'),
        ('blank', '填空'),
        ('judge', '判断'),
        ('qa', '问答'),
    )

    title = models.CharField(max_length=50)
    A = models.CharField(max_length=50, blank=True)
    B = models.CharField(max_length=50, blank=True)
    C = models.CharField(max_length=50, blank=True)
    D = models.CharField(max_length=50, blank=True)
    E = models.CharField(max_length=50, blank=True)
    questionType = models.CharField(max_length=10, choices=questionType, default='singleA')
    # After sorting, 'A', 'AB' or 'blank'
    answer = models.CharField(max_length=10)
    bank = models.CharField(max_length=20)

    def __str__(self):
        return self.title



class Article(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    neededCoin = models.PositiveIntegerField(default=0)
    publicDate = models.DateTimeField(auto_now_add=True)
    editDate = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField('Comment', blank=True)

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

    class Meta:
        ordering = ('-id',)


