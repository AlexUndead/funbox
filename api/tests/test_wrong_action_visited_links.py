from django.test import TestCase
from rest_framework import status
from .test_base import BaseApiTests



class WrongActionVisitedLinks(BaseApiTests):
    """
    Класс тестирования неудачных сценариев
    страницы сохранения посещенных ссылок
    """

    def test_wrong_request_without_body(self):
        """тест проверки ответа при запросе с пустым телом"""
        response = self._post_client_response(self.VISITED_LINKS_PATH, {})
        error_message = 'Check the request arguments. ' \
                        'The request must have values "links" ' \
                        'with values'

        self.assertEqual(response.data['status'], error_message)

    def test_wrong_request_with_not_correct_json(self):
        """тест проверки ответа при запросе с некорректным json"""
        not_correct_json = '{"links": ["https://ya.ru", "https://ya.ru?q=123", "funbox.ru", ]}'
        response = TestCase().client(self.VISITED_LINKS_PATH, not_correct_json)
        #response = self._post_client_response(self.VISITED_LINKS_PATH, [not_correct_json])
        print(response.data)
