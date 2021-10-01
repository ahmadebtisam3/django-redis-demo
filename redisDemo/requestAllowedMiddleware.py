import redis
from django.http import HttpResponse


class RequestAllowed(object):
    PERMISSIONS = {"golden": 10, "silver": 8, "platinium": 6, "user": 4}
    BLOCKLIST = "blockip"
    BLOCKTIME = 100
    conn = redis.Redis(host="127.0.0.1", port=6379)

    def __init__(self, response):
        self.get_response = response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kargs):
        try:
            if request.user.is_authenticated:
                for key, time in self.PERMISSIONS.items():
                    if request.user.groups.filter(name=key):
                        return self.request_allowed(self.conn, request, time)
            return self.request_allowed(self.conn, request,
                                        self.PERMISSIONS['user'])
        except Exception as e:
            print(" *********** error occured  ", e)

    def request_allowed(self, conn, request, tim):
        ip = request.META['REMOTE_ADDR']
        times = conn.get(ip)
        if times:
            if int(times) < tim:
                conn.incr(ip)
            else:
                self.block_ip(ip, conn)
        else:
            conn.set(ip, 0)
            conn.expire(ip, 60)
        if bytes(ip, 'utf-8') in conn.smembers("blockip"):
            return HttpResponse(status=400)
        return None

    def block_ip(self, ip, conn):
        if conn.smembers("blockip"):
            conn.sadd(self.BLOCKLIST, ip)
        else:
            conn.sadd(self.BLOCKLIST, ip)
            conn.expire(self.BLOCKLIST, self.BLOCKTIME)
