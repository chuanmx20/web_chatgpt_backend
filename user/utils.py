
import base64
import hmac
import json
import time
import hmac
import requests
from django.http import JsonResponse
from . import models
import yaml

def gen_token(email):
    header = {"typ": 'JWT', 'alg': "HS256"}
    # 将header字典 转为  json字符串
    header_str = json.dumps(header)
    # print("header_str:", header_str, type(header_str))
    header_encode = base64.urlsafe_b64encode(header_str.encode())
    # print("编码的结果:", header_encode)
    # 替换=   为 空字符
    header_p1 = header_encode.replace(b"=", b"")
    payload = {"email": 'email', 'exp': time.time() + 300}
    # 对payload进行base64编码
    payload_p2 = base64.urlsafe_b64encode(
        json.dumps(payload).encode()).replace(b"=", b"")
    # 获取第三部分
    # 先拼接前两部分
    temp = header_p1 + b"." + payload_p2
    # hash 加密
    temp_hash = hmac.new(b"123", temp, digestmod="SHA256")
    # print("加密的二进制结果：", temp_hash.digest())
    # print("加密的十六进制结果:", temp_hash.hexdigest())
    # base64 编码
    signature = base64.urlsafe_b64encode(temp_hash.digest()).replace(b"=", b"")
    # 最后三者拼接
    jwt_token = (header_p1 + b"." + payload_p2 + b"." + signature).decode()
    # print("jwt token:", jwt_token)
    return jwt_token


def verification(fun):
    def wrapped_func(*args, **kwargs):
        token = args[0].headers.get('Authorization')
        if 'Authorization' not in args[0].headers.keys() or token == '':
            return JsonResponse({'status_code': 500, 'message': '请检查请求头Authorization'})
        query = models.Token.objects.filter(token=token)
        if query.__len__() == 0:
            return JsonResponse({'status_code': 403, 'data': 'Authorization failed!'})
        if query.first().exp < time.time():
            query.first().delete()
            return JsonResponse({'status_code': 401, 'data': 'Token expired'})

        return fun(**args, **kwargs, user=query.first().user)
    return wrapped_func

def decode_bytes(data):
    pairs = data.split('&')
    ret = {}
    for pair in pairs:
        key, value = pair.split('=')
        ret[key] = value
    return ret

def oauth(fun):
    def wrapped_func(*args, **kwargs):
        # get code in request.body
        code = json.loads(args[0].body).get('code', '')
        if code == '':
            return JsonResponse({'status_code': 400, 'message': 'Invalid oauth code'})
        
        # get client_id and secret in config.yml
        conf = open('config.yml', 'r', encoding='utf-8').read()
        conf = yaml.load(conf)
        client_id = conf['client_id']
        client_secret = conf['client_secret']

        # oauth token
        url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}"
        response = requests.get(url, {'content_type':'application/json'})
        response = decode_bytes(response.text)
        if 'access_token' not in response:
            return JsonResponse({'status_code':500, 'data':'code error'})

        token = response['access_token']
        url = "https://api.github.com/user"
        response = requests.get(url, headers={
            'Authorization': f'Bearer {token}',
            'content_type': 'application/json',
        })
        data = response.json()
        # check email in whitelist
        if "email" not in data:
            return JsonResponse({'status_code':400, 'data':'Email not found in GitHub profile!'})
        email = data['email']
        print(conf['email_whitelist'][0])
        if email not in conf['email_whitelist']:
            print(email)
            return JsonResponse({'status_code':400, 'data':'You are not qualified to login!'})
        return fun(*args, **kwargs, email=email)

    return wrapped_func
