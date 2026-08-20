# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Tiger
    @file： system_management.py
    @date：2024/3/19 13:47
    @desc: Mailmanage
"""

from django.db import models

from common.mixins.app_model_mixin import AppModelMixin


class SettingType(models.IntegerChoices):
    """System settingsType"""
    EMAIL = 0, 'Mail'

    RSA = 1, "Private key"

    LOG = 2, "dayLog cleanup time"


class SystemSetting(AppModelMixin):
    """
     System settings
    """
    type = models.IntegerField(primary_key=True, verbose_name='SettingsType', choices=SettingType.choices,
                               default=SettingType.EMAIL)

    meta = models.JSONField(verbose_name="ConfigurationNumberAccording to", default=dict)

    class Meta:
        db_table = "system_setting"
