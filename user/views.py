from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .utils import *
from . import models
# Create your views here.

@oauth
def login(request, email=None):
    assert email != None
    users = models.User.objects.filter(email=email)
    user = None
    if users.__len__() == 0:
        # create new user
        user = models.User(email=email)
        user.save()
    user = users.first()
    tokens = models.Token.objects.filter(user=user)
    if tokens.__len__() != 0:
        tokens.first().delete()
    
    token = gen_token(email)
    token_model = models.Token(token=token, user=user)
    token_model.save()
    return JsonResponse({
        'status_code': 200,
        'token': token,
    })


def verify_token(request):
    return JsonResponse({
        'status_code': 200,
    })


@verification
def fetch_data(request, user=None):
    assert user != None

    data = []
    for msg in models.Message.objects.filter(user=user).order_by('-time'):
        data.append({
            'role': 'user' if msg.from_user else 'assistant',
            'content': msg.content,
        })
        return JsonResponse({
            'status_code': 200,
            'data': data
        })
    return JsonResponse({
        'status_code': 200,
        'data': [
            {
                'role': 'user',
                'content': 'Q1',
            },
            {
                'role': 'assistant',
                'content': 'A1',
            },
            {
                'role': 'user',
                'content': 'Q2'
            },
            {
                'role': 'assistant',
                'content': 'A2'
            }
        ]
    })
