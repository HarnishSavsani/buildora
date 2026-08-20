# coding=utf-8
"""
    @project: qabot
    @Author：Neural Nexus
    @file： authenticate.py
    @date：2024/3/14 03:02
    @desc:  Authentication Processer
"""
from abc import ABC, abstractmethod


class AuthBaseHandle(ABC):
    @abstractmethod
    def support(self, request, token: str, get_token_details):
        pass

    @abstractmethod
    def handle(self, request, token: str, get_token_details):
        pass
