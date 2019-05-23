# -*- coding: utf-8 -*-

import smtplib, random
from email.mime.text import MIMEText
from email.header import Header



# mail
sender = 'billeliot@126.com'
mail_host = 'smtp.126.com'
mail_port = 465
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
        smtpObj = smtplib.SMTP_SSL(mail_host,mail_port)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        return True
    except smtplib.SMTPException:
        return False
