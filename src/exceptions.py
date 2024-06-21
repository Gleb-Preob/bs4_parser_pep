class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class PepDocStatusException(Exception):
    """Вызывается, когда статус документа PEP не соответствует ожидаемому."""


class EmptyResponseException(Exception):
    """Вызывается, когда запрос к url выполнен успешно, но response is None."""
