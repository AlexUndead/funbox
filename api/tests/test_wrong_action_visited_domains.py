from rest_framework import status
from .test_base import BaseApiTests


class WrongActionVisitedDomains(BaseApiTests):
    """
    Класс тестирования неудачных сценариев
    страницы просмотра посещенных доменов
    """
    def test_wrong_status_code_request(self):
        """тест проверки кода ответа с некорректными данными запроса"""
        list_wrong_parameters = (
            {'from': '1591709370'},
            {'from': '1591709370', 'to': 'to'},
            {'from': '1591709370', 'to': '1591709373'},
        )

        for wrong_parameter in list_wrong_parameters:
            response = self._get_client_response(self.VISITED_DOMAINS_PATH, wrong_parameter)
            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_wrong_request_with_string_arguments(self):
        """тест проверки ответа запроса со строковым параметром"""
        error_message = 'min or max is not a float'
        string_parameter = {'from': '1591709370', 'to': 'test'}
        response = self._get_client_response(self.VISITED_DOMAINS_PATH, string_parameter)

        self.assertEqual(response.data['status'], error_message)

    def test_wrong_request_without_arguments(self):
        """тест проверки ответа запроса без параметров"""
        error_message = 'Check the request arguments. ' \
                             'The request must have values "from" and "to"'
        response = self._get_client_response(self.VISITED_DOMAINS_PATH, {})

        self.assertEqual(response.data['status'], error_message)

    def test_wrong_out_of_time_range(self):
        """
        тест проверки ответа запроса во временном промежутке
        в котором нет данных
        """
        error_message = 'There is no data in this time period'
        response = self._get_client_response(
            self.VISITED_DOMAINS_PATH,
            {'from': '1591709370', 'to': '1591709373'}
        )

        self.assertEqual(response.data['status'], error_message)
