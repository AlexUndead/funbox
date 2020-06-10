import redis
import json
import time
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .utils import get_domains
from .exceptions import *

REDIS_ZSET = 'links'


def get_redis_instance(func):
    """
    Декоратор определяющий инстанс редис в зависимости от
    передачи тестового параметра
    """
    def wrapper(request, *args, **kwargs):
        db = 1 if request.META.get('HTTP_TEST', '') or \
                  request.META.get('headers', '') and \
                  request.META.get('headers', '').get('test', '') else 0
        kwargs['redis_instance'] = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            charset="utf-8",
            decode_responses=True,
            db=db,
        )
        return func(request, *args, **kwargs)

    return wrapper


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@get_redis_instance
def visited_links(request, *args, **kwargs):
    """Брекпоинт сохранения ссылок"""
    try:
        code = 201
        response = {'status': 'ok'}
        redis_instance = kwargs['redis_instance']
        timestamp = str(round(time.time()))
        links = json.loads(request.body).get("links", '')
        if not links:
            raise RequestEmptyDataLinksError
        link_id = 'link:' + timestamp

        redis_instance.zadd(REDIS_ZSET, {link_id: timestamp})
        for link in links:
            redis_instance.sadd(link_id, link)

    except RequestEmptyDataLinksError:
        code = 409
        response['status'] = 'Check the request arguments. ' \
                             'The request must have values "links" ' \
                             'with values'
    except json.JSONDecodeError:
        code = 409
        response['status'] = 'Not valid json'

    return Response(response, code)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
@get_redis_instance
def visited_domains(request, *args, **kwargs):
    """Брекпоинт получения доменов"""
    try:
        code = 201
        response = {'status': 'ok'}
        redis_instance = kwargs['redis_instance']
        request_from = request.GET['from']
        request_to = request.GET['to']

        link_ids_between_dates = redis_instance.zrangebyscore(REDIS_ZSET, request_from, request_to)
        links = redis_instance.sunion(link_ids_between_dates)
        domains = get_domains(links)
        response['domains'] = domains

    except redis.exceptions.ResponseError as redis_response_error:
        code = 409
        response['status'] = redis_response_error.args[0]
    except MultiValueDictKeyError:
        code = 409
        response['status'] = 'Check the request arguments. The request must have values "from" and "to"'

    return Response(response, code)
