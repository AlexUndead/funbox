import time
from rest_framework import status
from .test_base import BaseApiTests


class SuccessActionVisitedLinks(BaseApiTests):
    """
    Класс тестирования успешных сценариев
    страницы сохранения посещенных ссылок
    """

    def test_success_request_status_code(self):
        """тест кода статуса успешного ответа"""
        response_data = {"links": ["https://ya.ru", "funbox.ru"]}
        response = self._post_client_response(self.VISITED_LINKS_PATH, response_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_success_request_answer(self):
        """тест ответа успешного запроса"""
        response_data = {"links": ["https://ya.ru", "funbox.ru"]}
        response = self._post_client_response(self.VISITED_LINKS_PATH, response_data)

        self.assertEqual(response.data['status'], 'ok')

    def test_success_saving_zset_links_items(self):
        """тест сохранения нескольких множеств элементов списка ссылок"""
        redis_instance = self._get_redis_instance()
        response_data = {"links": ["https://ya.ru", "funbox.ru"]}
        count = 2

        for request in range(count):
            time.sleep(1)
            self._post_client_response(self.VISITED_LINKS_PATH, response_data)

        links_count = redis_instance.zcard(self.REDIS_ZSET)

        self.assertEqual(links_count, count)

    def test_success_saving_correct_count_items(self):
        """тест сохранения корректного числа и содержания ссылок в множестве"""
        redis_instance = self._get_redis_instance()
        response_data = {"links": ["https://ya.ru", "funbox.ru", "google.com"]}

        self._post_client_response(self.VISITED_LINKS_PATH, response_data)

        link_id = redis_instance.zrange(self.REDIS_ZSET, 0, 1)
        links_items = redis_instance.smembers(link_id.pop())

        self.assertEqual(links_items, set(response_data['links']))
