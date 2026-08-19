# coding=utf-8
"""
    @project: MaxKB
    @Author：TigerTiger
    @file： user.py
    @date：2025/4/14 10:20
    @desc:
"""
import uuid_utils.compat as uuid
from django.db import models

from common.constants.permission_constants import Group


class ChatUser(models.Model):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    email = models.EmailField(null=True, blank=True, verbose_name="Mail", db_index=True)
    phone = models.CharField(max_length=20, verbose_name="Telephone", default="")
    nick_name = models.CharField(max_length=150, verbose_name="Nick name", unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, verbose_name="username", db_index=True)
    password = models.CharField(max_length=150, verbose_name="Password")
    source = models.CharField(max_length=10, verbose_name="source", default="LOCAL", db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(verbose_name="Creation time", auto_now_add=True, null=True, db_index=True)
    update_time = models.DateTimeField(verbose_name="modification time", auto_now=True, null=True, db_index=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "chat_user"


class UserGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    name = models.CharField(max_length=150, verbose_name="Name", unique=True, db_index=True)

    class Meta:
        db_table = "user_group"


class UserGroupRelation(models.Model):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, verbose_name="Users")
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name="User group")

    class Meta:
        db_table = "user_group_relation"


class ResourceType(models.TextChoices):
    """Resource type"""
    KNOWLEDGE = Group.KNOWLEDGE.value, 'knowledge base'
    APPLICATION = Group.APPLICATION.value, 'application'


class ResourceChatUserAuthorize(models.Model):
    """
    resourceDialog usersAuthorization table
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True,
                                    null=True)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name="User group")
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, verbose_name="Users")
    resource_id = models.UUIDField(max_length=128, verbose_name="resourceid", db_index=True)
    resource_type = models.CharField(verbose_name="Resource type", choices=ResourceType.choices, db_index=True)
    is_auth = models.BooleanField(verbose_name="whether authorized")

    class Meta:
        db_table = "resource_chat_user_authorize"
        unique_together = ('user_group_id', 'resource_type', 'resource_id', 'user_id')


class ResourceChatUserGroupAuthorize(models.Model):
    """
    resourceDialog usersGroup authorization table
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True,
                                    null=True)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name="User group")
    resource_id = models.UUIDField(max_length=128, verbose_name="resourceid", db_index=True)
    resource_type = models.CharField(verbose_name="Resource type", choices=ResourceType.choices, db_index=True)
    is_auth = models.BooleanField(verbose_name="whether authorized")

    class Meta:
        db_table = "resource_chat_user_group_authorize"
        unique_together = ('user_group_id', 'resource_type', 'resource_id')
