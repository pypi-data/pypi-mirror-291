import gzip
import json
from io import BytesIO
from request_logger.models import userLog
from django.utils import timezone
import locale
from threading import Thread

def get_client_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip = ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def compress_json(data):
    buf = BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(data.encode('utf-8'))
    return buf.getvalue()

def build_json(data_dict):
    serializable_dict = {k: v for k, v in data_dict.items() if isinstance(v, str)}
    return json.dumps(serializable_dict)

def userLogCheck(get_response):
    def middleware_log(request):
        response = get_response(request)

        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        
        now = timezone.now()
        path = f"{request.path}"

        log_data = {
            'user': request.user if request.user.is_authenticated else None,
            'url': path,
            'ip': get_client_ip(request),
            'status_code': response.status_code,
            'time':now,
            'type':request.method
        }

        if request.method == "GET":
            meta_data = build_json(request.META)
            log_data['metaData'] = compress_json(meta_data)
        
        elif request.method == "POST":
            post_data = build_json({key: value for key, value in request.POST.items() if key != 'password'})
            meta_data = build_json(request.META)
            log_data['postData'] = compress_json(post_data)
            log_data['metaData'] = compress_json(meta_data)

        def log_to_db(data):
            userLog.objects.create(
                user=data['user'],
                url=data['url'],
                metaData=data['metaData'],
                postData=data.get('postData'),
                ip=data['ip'],
                status_code=data['status_code'],
                time=data['time'],
                status_type=data['type']
            )
        
        Thread(target=log_to_db, args=(log_data,)).start()

        return response
    
    return middleware_log