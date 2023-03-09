from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .utils import *
# Create your views here.

@oauth
def login(request):
    return JsonResponse({
        'status_code': 200,
        'token': 'token'
    })


def verify_token(request):
    return JsonResponse({
        'status_code': 200,
    })


@verification
def fetch_data(request, user=None):
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
