import time
from rest_framework import status
from .test_base import BaseApiTests
from api.utils import get_domains


def set_testing_fixtures(func):
    """декоратор установки тестовых фикстур"""
    lists_links = [
        ["https://ya.ru/search/?text=test&lr=2/", "funbox.ru", "twitch.com"],
        ["https://ya.ru", "google.com", "funbox.ru",
         "https://stackoverflow.com/questions/11828270"]
    ]

    def wrapper(self):
        start_time = round(time.time())
        all_links = []
        for list_links in lists_links:
            self._post_client_response(self.VISITED_LINKS_PATH, {'links': list_links})
            all_links.extend(list_links)

        end_time = round(time.time())

        self.start_time = start_time
        self.end_time = end_time
        self.all_links = all_links
        func(self)

    return wrapper


class SuccessActionVisitedDomains(BaseApiTests):
    """
    Класс тестирования успешных сценариев
    страницы получения посещенных доменов
    """

    @set_testing_fixtures
    def test_success_request_status_code(self):
        """тест кода статуса успешного ответа"""
        request_data = {"from": self.start_time, "to": self.end_time}
        response = self._get_client_response(self.VISITED_DOMAINS_PATH, request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @set_testing_fixtures
    def test_success_request_correct_domains(self):
        """тест успешного ответа страницы посещенных доменов"""
        request_data = {"from": self.start_time, "to": self.end_time}
        response = self._get_client_response(self.VISITED_DOMAINS_PATH, request_data)

        self.assertEqual(response.data['domains'], get_domains(self.all_links))
