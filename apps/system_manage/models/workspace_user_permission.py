# coding=utf-8
"""
    @project: MaxKB
    @Author：TigerTiger
    @file： workspace_permission.py
    @date：2025/4/16 18:25
    @desc:
"""

import uuid_utils.compat as uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.constants.permission_constants import Group, ResourcePermissionGroup, ResourceAuthType, \
    ResourcePermissionRole, ResourcePermission
from users.models import User


class AuthTargetType(models.TextChoices):
    """AuthorizeTarget"""
    KNOWLEDGE = Group.KNOWLEDGE.value, 'knowledge base'
    APPLICATION = Group.APPLICATION.value, 'application'
    TOOL = Group.TOOL.value, 'tool'
    MODEL = Group.MODEL.value, 'Model'


class WorkspaceUserResourcePermission(models.Model):
    """
    WorkspaceUsersresourcePermissionssurface
    Used to managecurrentWorkspaceYes?Permissionsoperate a certain piecesapplicationorknowledge base
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")

    workspace_id = models.CharField(max_length=128, verbose_name="Workspaceid", default="default", db_index=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="WorkspaceunderUsers")

    auth_target_type = models.CharField(verbose_name='AuthorizeTarget', max_length=128, choices=AuthTargetType.choices,
                                        default=AuthTargetType.KNOWLEDGE, db_index=True)
    # Authorizedknowledge baseoror applicationid
    target = models.CharField(max_length=128, verbose_name="knowledge base/applicationid", db_index=True)

    # AuthorizeType likeIf YesRole thenYesRolePermissions  likeIfYesPERMISSION
    auth_type = models.CharField(default=False, verbose_name="AuthorizeType", choices=ResourceAuthType.choices,
                                 db_default=ResourceAuthType.ROLE, db_index=True)
    # resourcePermissionsList
    permission_list = ArrayField(verbose_name="PermissionsList",
                                 default=list,
                                 base_field=models.CharField(max_length=256,
                                                             blank=True,
                                                             choices=ResourcePermission.choices + ResourcePermissionRole.choices,
                                                             default=ResourcePermission.VIEW))

    create_time = models.DateTimeField(verbose_name="Creation time", auto_now_add=True, db_index=True)

    update_time = models.DateTimeField(verbose_name="modification time", auto_now=True, db_index=True)

    class Meta:
        db_table = "workspace_user_resource_permission"
        unique_together = ('workspace_id', 'user', 'auth_target_type', 'target')
