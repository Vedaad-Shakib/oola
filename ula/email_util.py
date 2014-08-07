from django.core.mail       import *
from django.template.loader import get_template
from django.template        import Context
from django.http            import HttpResponseRedirect

import datetime

from myproject.settings     import *
from models                 import *
from util                   import *


def sendEmail(request, user, type):
    
    if type == "resetPassword":
        plaintext = get_template('email.txt')
        htmly     = get_template('email.html')
        d = Context({'username': user.name})
        
        randomPassword = RandomPassword()
        randomPassword.userId = user
        while True:
            randomString = randomStr(16)
            try:
                temp = RandomPassword.objects.get(passwordKey=randomString)
            except:
                randomPassword.passwordKey = randomString
                break
        
        randomPassword.expiration = datetime.datetime.now() + datetime.timedelta(0, 14400)
        randomPassword.save()
        

    subject, from_email, to = 'hello', 'vedaad799@gmail.com', user.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")

    # retrieve emailbackend from settings.py
    connection = get_connection()
    connection.username = settings.EMAIL_HOST_USER
    connection.password = settings.EMAIL_HOST_PASSWORD
    connection.host = EMAIL_HOST
    connection.send_messages([msg,])
    connection.close()

def sendEmailBasic(request):
    msg = EmailMessage('Request Callback',
                       'Here is the message.', to=['andrew.tierno@gmail.com'])
    msg.send()
    return HttpResponseRedirect('/')
