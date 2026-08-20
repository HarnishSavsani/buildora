# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： log_management.py
    @date：2025/6/4 14:15
    @desc:
"""
import uuid_utils.compat as uuid

from django.db import models

from common.encoder.encoder import SystemEncoder
from common.mixins.app_model_mixin import AppModelMixin


class Log(AppModelMixin):
    """
    Audit diary
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")

    menu = models.CharField(max_length=128, verbose_name="operateMenu")

    operate = models.CharField(max_length=128, verbose_name="operate", db_index=True)

    operation_object = models.JSONField(verbose_name="operateobject", default=dict, encoder=SystemEncoder)

    user = models.JSONField(verbose_name="Usersinformation", default=dict)

    status = models.IntegerField(verbose_name="state", db_index=True)

    ip_address = models.CharField(max_length=128, verbose_name="ipaddress")

    details = models.JSONField(verbose_name="Details", default=dict, encoder=SystemEncoder)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)

    class Meta:
        db_table = "log"
