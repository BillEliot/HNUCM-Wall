# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import send_mail
import random, time, smtplib


def generateCaptcha():
    return ''.join(random.choice('0123456789') for _ in range(6))



def sendCaptcha(receiver, captcha):
    try:
        # When compiling python3 from source code, you need to support SSL
        send_mail(
            '【HNUCM】- 湖南中医药大学校园墙',
            "【HNUCM】- 湖南中医药大学校园墙 -> 您的验证码为：" + captcha,
            'no-reply@mail.hnucmwall.top',
            [receiver],
            False
        )
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False



def formatName(name, suffix):
    return name + '_' + str(int(time.time())) + '.' + suffix



def generateUploadPath(directory, name):
    return settings.MEDIA_ROOT + directory + '/' + name



def sizeFormat(size, precision=2):
    '''
    size format for human.
        byte      ---- (B)
        kilobyte  ---- (KB)
        megabyte  ---- (MB)
        gigabyte  ---- (GB)
        terabyte  ---- (TB)
        petabyte  ---- (PB)
        exabyte   ---- (EB)
        zettabyte ---- (ZB)
        yottabyte ---- (YB)
    '''
    formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1024.0
    if not(isinstance(size, float) or isinstance(size, int)):
        raise TypeError('a float number or an integer number is required!')
    if size < 0:
        raise ValueError('number must be non-negative')
    for i in formats:
        size /= unit
        if size < unit:
            return f'{round(size, precision)}{i}'
    return f'{round(size, precision)}{i}'
