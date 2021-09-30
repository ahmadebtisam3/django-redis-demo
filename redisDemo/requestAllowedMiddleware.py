import redis
from django.http import HttpResponse


class RequestAllowed(object):
    def __init__(self, response):
        self.get_response = response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kargs):
        allowed = True
        try:
            if not request.user.is_authenticated:
                allowed = self._unauthorized_user_permitions(request, 5)
            elif request.user.groups.filter(name="golden"):
                allowed = self._unauthorized_user_permitions(request, 10)
            elif request.user.groups.filter(name="silver"):
                allowed = self._unauthorized_user_permitions(request, 8)
            elif request.user.groups.filter(name="platinium"):
                allowed = self._unauthorized_user_permitions(request, 6)
        except Exception as e:
            print(" *********** error occured  ", e)
        if not allowed:
            return HttpResponse(status=400)

    def _unauthorized_user_permitions(self, request, tim):
        conn = redis.Redis(host="127.0.0.1", port=6379)
        ip = request.META['REMOTE_ADDR']
        times = conn.get(ip)
        if times:
            if int(times) < tim:
                conn.incr(ip)
            else:
                conn.sadd("blockip", ip)
        else:
            conn.set(ip, 0)
            conn.expire(ip, 60)
        if bytes(ip, 'utf-8') in conn.smembers("blockip"):
            return False
        return True