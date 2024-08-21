#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@time   : 2021/1/8 16:23
@file   : logger.py
@author : nbyue
@desc   : 
@exec   : /bin/python3 logger.py
@wiki
"""
import logging
from logging.handlers import RotatingFileHandler


def logger(log_file, console_log=True, file_log=True):
    """
    :param log_file:
    :return:
    """
    log = logging.getLogger(__name__)
    log.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if file_log:
        file_handler = RotatingFileHandler(filename=log_file,
                                           maxBytes=100 * 1024 * 1024,
                                           backupCount=1,
                                           encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    if console_log:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        log.addHandler(console_handler)

    return log
