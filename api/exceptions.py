"""Core exceptions raised by the api for link tracking"""


class RequestEmptyDataLinksError(Exception):
    """
    Исключение возникающее если в теле запроса
    не будет массива ссылками
    """
    pass