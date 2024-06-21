import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import EmptyResponseException, ParserFindTagException


def get_response(session, url, encode='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encode
        return response
    except RequestException:
        errmsg = f'Возникла ошибка при загрузке страницы {url}'
        raise RequestException(errmsg)


def make_soup(session, url, features='lxml'):
    response = get_response(session, url)
    if response is None:
        errmsg = 'При загрузке страницы получен пустой ответ'
        raise EmptyResponseException(errmsg)
    return BeautifulSoup(response.text, features=features)


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
