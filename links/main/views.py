import json
from datetime import datetime

import redis

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from links.settings import REDIS_PORT
from main.utils import clean_links

r = redis.Redis(host='redis', port=REDIS_PORT, db=0)


@csrf_exempt
@require_http_methods(['POST'])
def add_visited_links(request):
    try:
        content = json.loads(request.body)
        cleaned_links = clean_links(content['links'])
        unique_links = set(cleaned_links)
        for x in unique_links:
            if x:
                curr_time = datetime.now().timestamp()
                r.zadd('linkHistory:domains', {x: curr_time})

        return JsonResponse(data={'status': 'ok'}, status=201)

    except KeyError:
        error_content = 'wrong params'

    except Exception as e:
        error_content = e

    return HttpResponseBadRequest(content=error_content)


@csrf_exempt
@require_http_methods(['GET'])
def get_domains(request):
    try:
        start_time = int(request.GET.get('from'))
        end_time = int(request.GET.get('to')) + 1
        domains = set()
        answer = dict(domains=[], status='')
        if end_time - start_time < 0:
            answer['status'] = 'Некорректный интервал времени'
            return JsonResponse(answer)

        data = r.zrangebyscore('linkHistory:domains', start_time, end_time, withscores=True)

    except redis.exceptions.ConnectionError:
        return JsonResponse(dict(status='Проблема с БД'))
    except Exception as e:
        return HttpResponseBadRequest('wrong input {0}'.format(str(e)))

    x: bytes
    for x, score in data:
        if x in domains:
            continue
        else:
            domains.add(x.decode('utf-8'))

    answer["domains"] = list(domains)
    answer["status"] = 'ok'

    return JsonResponse(answer)
