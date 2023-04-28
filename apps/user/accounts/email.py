import jwt
from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings

def url_generator(domain, uid, token):
    return f"http://{domain}/accounts/validation/{uid}/{token}"

def send(request, email, type):
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(email))
    token = jwt.encode({'email' : email, 'type' : type}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    url = url_generator(domain, uid, token)
    mail_title = "MindWay 이메일 인증"
    mail_to = email

    cache.set(email, token, 30)

    if type == 'signup':
        html_message = render_to_string('templates/signup.html', context={'url' : url})
    elif type == 'password':
        html_message = render_to_string('templates/change_password.html', context={'url' : url})

    msg = EmailMultiAlternatives(mail_title, url, settings.EMAIL_HOST_USER, [mail_to])
    msg.attach_alternative(html_message, 'text/html')
    msg.send()