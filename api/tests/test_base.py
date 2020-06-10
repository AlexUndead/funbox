import redis
from django.conf import settings
from rest_framework.test import APITestCase


class BaseApiTests(APITestCase):
    """Базовый класс тестирования апи"""
    REDIS_ZSET = settings.REDIS_ZSET_NAME
    VISITED_LINKS_PATH = '/visited_links/'
    VISITED_DOMAINS_PATH = '/visited_domains/'
    HEADERS = {'test': 'true'}
    JSON_FORMAT = 'json'

    def tearDown(self):
        """удаление всех данных сохраненных в результате выполнения тестов"""
        redis_instance = self._get_redis_instance()
        for sets in redis_instance.zrange(self.REDIS_ZSET, 0, -1):
            redis_instance.delete(sets)

        redis_instance.delete(self.REDIS_ZSET)

    def _get_client_response(self, path, data):
        """Get запрос тестового клиента с нужными загаловками"""
        return self.client.get(
            path,
            data,
            headers=self.HEADERS
        )

    def _post_client_response(self, path, data):
        """Post запрос тестового клиента с нужными загаловками"""
        return self.client.post(
            path,
            data,
            format=self.JSON_FORMAT,
            headers=self.HEADERS
        )

    def _get_redis_instance(self):
        """получить инстанс к бд редис"""
        return redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            charset="utf-8",
            decode_responses=True,
            db=1,
        )
