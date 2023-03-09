from django.shortcuts import render
from django.http import HttpRequest, HttpResponse,JsonResponse

# Create your views here.
def login(request):
    return JsonResponse({
        'code': 200,
        'token': 'token'
    })

def verify_token(request):
    return JsonResponse({
        'code': 200,
    })

def fetch_data(request):
    return JsonResponse({
        'code': 200,
        'data':[
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
