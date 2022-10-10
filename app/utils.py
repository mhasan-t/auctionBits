from .models import RequestAndIP
from django.utils import timezone

def check_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        req = RequestAndIP.objects.filter(ip=ip)


        now = timezone.now()
        now_minus_ten = now - timezone.timedelta(minutes=5)
        if len(req)==0:
            r =  RequestAndIP.objects.create(ip=ip, req_counter=20)
        elif req[0].last_request_time > now_minus_ten:
            req[0].req_counter=req[0].req_counter-1
            req[0].save()
        else:
            req[0].last_request_time = now
            req[0].req_counter=10
            req[0].save()
        

        if req[0].req_counter == 0:
            req[0].last_request_time = now
            req[0].save()
            return True

        return False