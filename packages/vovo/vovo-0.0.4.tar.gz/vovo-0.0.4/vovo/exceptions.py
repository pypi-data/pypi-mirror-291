from typing import Any


class VovoException(Exception):
    ...


class ParserException(ValueError, VovoException):
    """解析器应引发异常以表示解析错误"""

    def __init__(self, error: Any):
        super(ParserException, self).__init__(error)
