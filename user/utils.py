
import base64
import hmac
import json
import time
import hmac

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

