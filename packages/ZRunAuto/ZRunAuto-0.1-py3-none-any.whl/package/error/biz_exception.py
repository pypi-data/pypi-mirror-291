#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""自定义异常"""


class BIZException(Exception):

    def __init__(self, message):
        super().__init__(message)

