import redis
from django.http import HttpResponse


class RequestAllowed(object):
    def __init__(self, response):
        self.get_response = response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kargs):
        conn = redis.Redis(host="127.0.0.1", port=6379)
        ip = request.META['REMOTE_ADDR']
        times = conn.get(ip)
        if times:
            if int(times) < 5:
                conn.incr(ip)
            else:
                conn.sadd("blockip", ip)
        else:
            conn.set(ip, 0)
            conn.expire(ip, 60)
        if bytes(ip, 'utf-8') in conn.smembers("blockip"):
            return HttpResponse(status=400)
