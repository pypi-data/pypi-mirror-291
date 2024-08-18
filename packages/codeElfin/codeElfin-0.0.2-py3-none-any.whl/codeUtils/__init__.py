#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/08/18 13:18:17
@Author  :   firstelfin 
@Version :   1.0
@Desc    :   None
'''

from . import decorator
from .tools import is_async_function



__all__ = [
    "decorator.log_time", 
    "decorator.inject_time", 
    "decorator.inject_attr",
    "is_async_function"
]
