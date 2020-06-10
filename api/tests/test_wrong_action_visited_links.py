from rest_framework import status
from .test_base import BaseApiTests


class WrongActionVisitedLinks(BaseApiTests):
    """
    Класс тестирования неудачных сценариев
    страницы сохранения посещенных ссылок
    """
    def test_wrong_status_code_request(self):
        """тест проверки кода ответа с некорректными данными запроса"""
        list_wrong_parameters = ('', {}, {'links': []}, '{"links": ["https://ya.ru", "funbox.ru", ]}')

        for wrong_parameter in list_wrong_parameters:
            response = self.client.generic('POST', self.VISITED_LINKS_PATH, params=wrong_parameter)
            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_wrong_request_without_body(self):
        """тест проверки ответа с некорректными данными запросов"""
        list_wrong_parameters = ({}, {'links': []})
        error_message = 'Check the request arguments. ' \
                        'The request must have values "links" ' \
                        'with values'

        for wrong_parameter in list_wrong_parameters:
            response = self._post_client_response(self.VISITED_LINKS_PATH, wrong_parameter)
            self.assertEqual(response.data['status'], error_message)

    def test_wrong_request_with_not_correct_json(self):
        """тест проверки ответа при запросе с некорректным или пустым json"""
        list_wrong_parameters = ('', '{"links": ["https://ya.ru", "funbox.ru", ]}')
        error_message = "Not valid json"

        for wrong_parameter in list_wrong_parameters:
            response = self.client.generic('POST', self.VISITED_LINKS_PATH, params=wrong_parameter)
            self.assertEqual(response.data['status'], error_message)
