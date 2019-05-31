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
    comments = models.ManyToManyField('Comment', blank=True, related_name='user_comments')



class Love(models.Model):
    isAnony = models.BooleanField(default=False)
    userFrom = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_from')
    userTo = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='user_to')
    nameTo = models.CharField(max_length=20, default='TA')
    content = models.TextField()
    images = models.ManyToManyField('Image', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    thumbsUpUser = models.ManyToManyField('User', blank=True)



class Lose(models.Model):
    isFound = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    description = models.TextField()
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
    images = models.ManyToManyField('Image', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return self.name



class Image(models.Model):
    name = models.CharField(max_length=100, default='default')



class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ('-id',)


