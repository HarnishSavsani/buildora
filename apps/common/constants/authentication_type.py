# coding=utf-8
"""
    @project: maxkb
    @Author：TigerTiger
    @file： authentication_type.py
    @date：2023/11/14 20:03
    @desc:
"""
from enum import Enum


class AuthenticationType(Enum):
    # systemUsers
    SYSTEM_USER = "SYSTEM_USER"
    # Dialog users
    CHAT_USER = "CHAT_USER"
    # ConversationanonymousUsers
    CHAT_ANONYMOUS_USER = "CHAT_ANONYMOUS_USER"
    # APIKEY
    API_KEY = "API_KEY"
