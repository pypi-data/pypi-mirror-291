#!/usr/bin/env python
# -*- coding:utf-8 -*-
from loguru import logger

def info(__message: str) -> None:
    logger.info(__message)

def warning(__message: str) -> None:
    logger.warning(__message)

def error(__message: str) -> None:
    logger.error(__message)

