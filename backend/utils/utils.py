# -*- coding: utf-8 -*-

from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random, time


# mail
sender = 'billeliot@126.com'
mail_host = 'smtp.126.com'
mail_user="billeliot@126.com"
mail_pass="hnucmwall"

def generateCaptcha():
    return ''.join(random.choice('0123456789') for _ in range(6))



def sendCaptcha(receiver, captcha):
    context = "【HNUCM】- 墙墙 -> 您的验证码为：" + captcha
    message = MIMEText(context, 'plain', 'utf-8')
    message['From'] = Header(sender)
    message['To'] =  Header(receiver)
    message['Subject'] = Header('【HNUCM】- 墙墙')

    try:
        # When compiling python3 from source code, you need to support SSL
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        return True
    except smtplib.SMTPException:
        return False



def formatName(name):
    return name + '_' + str(int(time.time())) + '.jpg'



def generateUploadPath(path, name):
    return settings.MEDIA_ROOT + path + name


