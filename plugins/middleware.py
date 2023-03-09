class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 允许来自你自己的前端的跨域请求
        response['Access-Control-Allow-Origin'] = 'https://chat.chuanmx.cc'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Accept, Authorization, Origin'

        return response
