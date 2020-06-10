import redis
from django.conf import settings
from rest_framework.test import APITestCase


class BaseApiTests(APITestCase):
    """Базовый класс тестирования апи"""
    REDIS_ZSET = 'links'
    VISITED_LINKS_PATH = '/visited_links/'
    HEADERS = {'test': 'true'}
    JSON_FORMAT = 'json'

    def tearDown(self):
        redis_instance = self._get_redis_instance()
        redis_instance.delete(self.REDIS_ZSET)

    def _post_client_response(self, path, data):
        """Post запрос тестового клиента с нужными загаловками"""
        return self.client.post(
            path,
            data,
            format=self.JSON_FORMAT,
            headers=self.HEADERS
        )

    def _get_redis_instance(self):
        """Получить инстанс к бд редис"""
        return redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            charset="utf-8",
            decode_responses=True,
            db=1,
        )
