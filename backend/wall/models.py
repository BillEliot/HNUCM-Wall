from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    openid = models.CharField(max_length=50, default=0)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='img/avatar', default='img/avatar/default.png')
    bio = models.CharField(max_length=100)
    gender = models.CharField(max_length=5, default='男')
    _class = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    coin = models.PositiveIntegerField(default=0)
    messages = models.ManyToManyField('Message', blank=True, related_name='messages')
    followings = models.ManyToManyField('User', blank=True, related_name='following')
    errorBook = models.ManyToManyField('Bank', blank=True, related_name='errorBook')
    auth = models.CharField(max_length=50, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



class Love(models.Model):
    isAnony = models.BooleanField(default=False)
    userFrom = models.ForeignKey('User', on_delete=models.CASCADE, related_name='userFrom')
    userTo = models.ManyToManyField('User', related_name='userTo')
    nameTo = models.CharField(max_length=20, default='TA')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumbsUpUser = models.ManyToManyField('User', blank=True)
    isTop = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.userFrom.username



class Lose(models.Model):
    isFound = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()
    loseDate = models.CharField(max_length=20)
    publicDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-publicDate',)
    
    def __str__(self):
        return self.name



class Deal(models.Model):
    isSold = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.FloatField()
    new = models.FloatField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.name



class Help(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title



##############################################################
class Bank_UpdateMessage(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.content



class Bank_UploadHistory(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.comment



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
    isTestPaper = models.BooleanField(default=False)

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



class Bank_Statistics(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=20)
    allQuestions = models.IntegerField()
    correctQuestions = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.user.username



class Bank_Result(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    subject = models.ForeignKey('Bank_Subject', on_delete=models.CASCADE)
    json_serialization = models.TextField()
    allQuestions = models.IntegerField()
    correctQuestions = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.user.username
##############################################################



##############################################################
class File_UploadHistory(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.comment



class File_Subject(models.Model):
    subjectType = (
        ('zy', '中医'),
        ('xy', '西医')
    )

    name = models.CharField(max_length=20)
    subjectType = models.CharField(max_length=10, choices=subjectType)

    def __str__(self):
        return self.name



class File(models.Model):
    fileType = (
        ('word', 'word'),
        ('excel', 'excel'),
        ('ppt', 'ppt'),
        ('pdf', 'pdf')
    )

    name = models.CharField(max_length=200)
    _file = models.FileField(upload_to='file/')
    _type = models.CharField(max_length=20, choices=fileType)
    date = models.DateTimeField(auto_now_add=True)
    viewCount = models.PositiveIntegerField(default=0)
    downloadCount = models.PositiveIntegerField(default=0)
    subject = models.ForeignKey('File_Subject', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name
##############################################################



class CommonFile(models.Model):
    fileType = (
        ('word', 'word'),
        ('excel', 'excel'),
        ('ppt', 'ppt'),
        ('pdf', 'pdf')
    )

    name = models.CharField(max_length=200)
    _file = models.FileField(upload_to='file/')
    _type = models.CharField(max_length=20, choices=fileType)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    tags = models.CharField(max_length=50, default='')
    content = models.TextField()
    neededCoin = models.PositiveIntegerField(default=0)
    publicDate = models.DateTimeField(auto_now_add=True)
    editDate = models.DateTimeField(auto_now=True)
    thumbsUpUser = models.ManyToManyField('User', blank=True, related_name="thumbsUp")
    viewCount = models.PositiveIntegerField(default=0)
    isAdopted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-publicDate',)

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



class Medicine(models.Model):
    medicineType = (
        ('解表药', '解表药'),
        ('清热药', '清热药'),
        ('泻下药', '泻下药'),
        ('祛风湿药', '祛风湿药'),
        ('化湿药', '化湿药'),
        ('利水渗湿药', '利水渗湿药'),
        ('温里药', '温里药'),
        ('理气药', '理气药'),
        ('消食药', '消食药'),
        ('驱虫药', '驱虫药'),
        ('止血药', '止血药'),
        ('活血化瘀药', '活血化瘀药'),
        ('化痰止咳平喘药', '化痰止咳平喘药'),
        ('安神药', '安神药'),
        ('平肝息风药', '平肝息风药'),
        ('开窍药', '开窍药'),
        ('补虚药', '补虚药'),
        ('收涩药', '收涩药'),
        ('涌吐药', '涌吐药'),
        ('涌吐药', '涌吐药'),
        ('攻毒杀虫止痒药', '攻毒杀虫止痒药'),
        ('拨毒化腐生肌药', '拨毒化腐生肌药')
    )
    subMedicineType = (
        ('/', '/'),
        ('发散风寒药', '发散风寒药'),
        ('发散风热药', '发散风热药'),
        ('清热泻火药', '清热泻火药'),
        ('清热燥湿药', '清热燥湿药'),
        ('清热解毒药', '清热解毒药'),
        ('清热凉血药', '清热凉血药'),
        ('清虚热药', '清虚热药'),
        ('攻下药', '攻下药'),
        ('润下药', '润下药'),
        ('峻下逐水药', '峻下逐水药'),
        ('祛风寒湿药', '祛风寒湿药'),
        ('祛风湿热药', '祛风湿热药'),
        ('祛风湿强筋骨药', '祛风湿强筋骨药'),
        ('利水消肿药', '利水消肿药'),
        ('利尿通淋药', '利尿通淋药'),
        ('利湿退黄药', '利湿退黄药'),
        ('凉血止血药', '凉血止血药'),
        ('化瘀止血药', '化瘀止血药'),
        ('收敛止血药', '收敛止血药'),
        ('温经止血药', '温经止血药'),
        ('活血止痛药', '活血止痛药'),
        ('活血调经药', '活血调经药'),
        ('活血疗伤药', '活血疗伤药'),
        ('破血消癓药', '破血消癓药'),
        ('温化寒痰药', '温化寒痰药'),
        ('清化热痰药', '清化热痰药'),
        ('止咳平喘药', '止咳平喘药'),
        ('重镇安神药', '重镇安神药'),
        ('养心安神药', '养心安神药'),
        ('平抑肝阳药', '平抑肝阳药'),
        ('息风止痉药', '息风止痉药'),
        ('补气药', '补气药'),
        ('补血药', '补血药'),
        ('补阴药', '补阴药'),
        ('补阳药', '补阳药'),
        ('固表止汗药', '固表止汗药'),
        ('敛肺涩肠药', '敛肺涩肠药'),
        ('固精缩尿止带药', '固精缩尿止带药')
    )

    name = models.CharField(max_length=20)
    # e.g. 辛;微苦;温
    flavor = models.CharField(max_length=50)
    # e.g. 肺;膀胱
    channel = models.CharField(max_length=50)
    function = models.CharField(max_length=200)
    application = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img/medicine', default='img/medicine/default.png')
    _type = models.CharField(max_length=20, choices=medicineType)
    subType = models.CharField(max_length=20, choices=subMedicineType)

    def __str__(self):
        return self.name



class Prescription(models.Model):
    name = models.CharField(max_length=20)
    composition = models.ManyToManyField('Medicine')
    function = models.CharField(max_length=50)
    application = models.CharField(max_length=100)
    song = models.CharField(max_length=100)
    _type = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Acupoint(models.Model):
    channels = (
        ('手太阴肺经', '手太阴肺经'),
        ('手阳明大肠经', '手阳明大肠经'),
        ('足阳明胃经', '足阳明胃经'),
        ('足太阴脾经', '足太阴脾经'),
        ('手少阴心经', '手少阴心经'),
        ('手太阳小肠经', '手太阳小肠经'),
        ('足太阳膀胱经', '足太阳膀胱经'),
        ('足少阴肾经', '足少阴肾经'),
        ('手厥阴心包经', '手厥阴心包经'),
        ('手少阳三焦经', '手少阳三焦经'),
        ('足少阳胆经', '足少阳胆经'),
        ('足厥阴肝经', '足厥阴肝经'),
        ('任脉', '任脉'),
        ('督脉', '督脉')
    )

    name = models.CharField(max_length=20)
    location = models.CharField(max_length=500)
    function = models.CharField(max_length=500)
    _type = models.CharField(max_length=50)
    channel = models.CharField(max_length=50, choices=channels)

    def __str__(self):
        return self.name



class Hot(models.Model):
    hotType = (
        ('新闻', '新闻'),
        ('通知', '通知'),
        ('招标公告', '招标公告'),
        ('中标公告', '中标公告'),
        ('瓜', '瓜')
    )

    title = models.CharField(max_length=30)
    content = models.TextField()
    _type = models.CharField(max_length=20, default='新闻', choices=hotType)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title



class Lecture(models.Model):
    title = models.CharField(max_length=30)
    lecturer = models.CharField(max_length=20)
    lecturerInfo = models.TextField(null=True)
    address = models.CharField(max_length=30)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    class Meta:
        ordering = ('-startDate',)

    def __str__(self):
        return self.title



class Match(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    requirement = models.TextField(null=True)
    prizeDescription = models.TextField(null=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    totalBonus = models.IntegerField(default=0)

    class Meta:
        ordering = ('-startDate',)

    def __str__(self):
        return self.title



class Image(models.Model):
    image = models.ImageField(upload_to='img/wall')
    love = models.ForeignKey('Love', on_delete=models.CASCADE, null=True)
    lose = models.ForeignKey('Lose', on_delete=models.CASCADE, null=True)
    deal = models.ForeignKey('Deal', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image



class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    love = models.ForeignKey('Love', on_delete=models.CASCADE, null=True)
    lose = models.ForeignKey('lose', on_delete=models.CASCADE, null=True)
    deal = models.ForeignKey('deal', on_delete=models.CASCADE, null=True)
    _help = models.ForeignKey('help', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey('article', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-id',)



class Message(models.Model):
    messageType = (
        ('thumbsUp', 'thumbsUp'),
        ('comment', 'comment')
    )
    messageFrom = (
        ('love', 'love'),
        ('lose', 'lose'),
        ('deal', 'deal'),
        ('help', 'help'),
        ('article', 'article')
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # thumbsUp or comment
    _type = models.CharField(max_length=10, choices=messageType)
    # love, lose, deal, help, article
    _from = models.CharField(max_length=10, choices=messageFrom)
    messageID = models.IntegerField()
    commentContent = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)



# Pending
class Activity_JinGui(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField(default=u'元气满满的一天～')
    cover = models.ImageField(upload_to='img/JinGui', default='img/JinGui/default.png')
    audio = models.FileField(upload_to='audio/JinGui', default='audio/JinGui/default.mp3')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)



# Pending
class Statistics_VirtualDiagnosis(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    patient_name = models.CharField(max_length=100)
    patient_gender = models.CharField(max_length=100)
    patient_age = models.CharField(max_length=100)
    patient_chiefcomplaint = models.CharField(max_length=200)
    patient_coldhot = models.CharField(max_length=100)
    patient_sweat = models.CharField(max_length=100)
    patient_pain = models.CharField(max_length=100)
    patient_body = models.CharField(max_length=100)
    patient_eareye = models.CharField(max_length=100)
    patient_sleep = models.CharField(max_length=100)
    patient_flavor = models.CharField(max_length=100)
    patient_excretion = models.CharField(max_length=100)
    patient_face = models.CharField(max_length=100)
    patient_tongue = models.CharField(max_length=100)
    patient_vein = models.CharField(max_length=100)

    player_diagnosis = models.CharField(max_length=100)
    player_syndrome = models.TextField()
    player_method = models.CharField(max_length=100)
    player_prescription = models.TextField()
    player_acupoints = models.CharField(max_length=200)

    ref_diagnosis = models.CharField(max_length=100)
    ref_syndrome = models.TextField()
    ref_method = models.CharField(max_length=100)
    ref_prescription = models.TextField()
    ref_acupoints = models.CharField(max_length=200)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.user.username