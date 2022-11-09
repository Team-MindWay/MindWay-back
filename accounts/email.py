import jwt
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings

def url_generator(domain, uid, token):
    return f"http://{domain}/accounts/validation/{uid}/{token}"

def send(request, email):
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(email))
    token = jwt.encode({'email' : email}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    url = url_generator(domain, uid, token)
    mail_title = "MindWay 이메일 인증"
    mail_to = email

    html_message = render_to_string('templates/validation.html', context={'url' : url})

    msg = EmailMultiAlternatives(mail_title, url, settings.EMAIL_HOST_USER, [mail_to])
    msg.attach_alternative(html_message, 'text/html')
    msg.send()