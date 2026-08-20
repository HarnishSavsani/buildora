# coding=utf-8
"""
    @project: qabot
    @Author：Neural Nexus
    @file： app_exception.py
    @date：2023/9/4 14:04
    @desc:
"""
from rest_framework import status


class AppApiException(Exception):
    """
    different within the project
    """
    status_code = status.HTTP_200_OK

    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotFound404(AppApiException):
    """
       Not certified(NotLogin)differentoften
       """
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppAuthenticationFailed(AppApiException):
    """
    Not certified(NotLogin)differentoften
    """
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppUnauthorizedFailed(AppApiException):
    """
    Unauthorized(NoPermissions)differentoften
    """
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppEmbedIdentityFailed(AppApiException):
    """
    After embedding cookie different normal
    """
    status_code = 460

    def __init__(self, code, message):
        self.code = code
        self.message = message


class AppChatNumOutOfBoundsFailed(AppApiException):
    """
      VisitsMore than today's visits
    """
    status_code = 461

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ChatException(AppApiException):
    status_code = 500

    def __init__(self, code, message):
        self.code = code
        self.message = message
