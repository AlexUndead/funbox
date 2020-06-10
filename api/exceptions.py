"""Основные исключения, создаваемые api"""


class RequestEmptyDataLinksError(Exception):
    """
    Исключение возникающее если в теле запроса
    не будет массива ссылками
    """
    pass


class RequestEmptyTimeArgumentsDomainsError(Exception):
    """
    Исключение возникающее если в теле запроса
    нет параметров промежутка времени в котором
    требуются посещенные домены
    """
    pass


class OutOfTimeRangeError(Exception):
    """
    Исключение возникающее запрашивается временной промежуток
    в котором нет данных
    """
    pass
