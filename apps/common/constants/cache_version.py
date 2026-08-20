# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： cache_version.py
    @date：2025/4/14 19:09
    @desc:
"""
from enum import Enum


class Cache_Version(Enum):
    # token
    TOKEN = "TOKEN", lambda token: token
    # WorkspaceList
    WORKSPACE_LIST = "WORKSPACE:LIST", lambda user_id: user_id
    # UsersNumberAccording to
    USER = "USER", lambda user_id: user_id
    # currentUsersallofRole
    ROLE_LIST = "ROLE:LIST", lambda user_id: user_id
    # currentUsersallPermissions
    PERMISSION_LIST = "PERMISSION:LIST", lambda user_id: user_id
    # Verification code
    CAPTCHA = "CAPTCHA", lambda captcha: captcha
    # system
    SYSTEM = "SYSTEM", lambda key: key
    # applicationCache for docking third-party applications
    APPLICATION_THIRD_PARTY = "APPLICATION:THIRD_PARTY", lambda key: key
    KNOWLEDGE_WORKFLOW_INTERRUPTED = "KNOWLEDGE_WORKFLOW_INTERRUPTED", lambda action_id: action_id
    # Conversation
    CHAT = "CHAT", lambda key: key

    CHAT_INFO = "CHAT_INFO", lambda key: key

    CHAT_VARIABLE = "CHAT_VARIABLE", lambda key: key

    # applicationAPI KEY
    APPLICATION_API_KEY = "APPLICATION_API_KEY", lambda secret_key, use_get_data: secret_key

    CHAT_USER_TOKEN = "CHAT_USER_TOKEN", lambda token: token

    TOOL_WORKFLOW_EXECUTE = "TOOL_WORKFLOW_EXECUTE", lambda key: key

    def get_version(self):
        return self.value[0]

    def get_key_func(self):
        return self.value[1]

    def get_key(self, **kwargs):
        return self.value[1](**kwargs)
