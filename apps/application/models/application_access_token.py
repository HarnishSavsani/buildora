# coding=utf-8
"""
    @project: MaxKB
    @Author：TigerTiger
    @file： application_access_token.py
    @date：2025/5/27 9:55
    @desc:
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models

from application.models.application import Application
from common.mixins.app_model_mixin import AppModelMixin


class ApplicationAccessToken(AppModelMixin):
    """
    applicationCertificationtoken
    """
    application = models.OneToOneField(Application, primary_key=True, on_delete=models.CASCADE, verbose_name="applicationid")
    access_token = models.CharField(max_length=128, verbose_name="UsersPublic access Certificationtoken", unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Whether to openPublic access")
    access_num = models.IntegerField(default=100, verbose_name="Visits")
    white_active = models.BooleanField(default=False, verbose_name="Whether to openWhitelist")
    white_list = ArrayField(verbose_name="WhitelistList",
                            base_field=models.CharField(max_length=128, blank=True)
                            , default=list)
    show_source = models.BooleanField(default=False, verbose_name="YesWhether to display knowledgesource")
    show_exec = models.BooleanField(default=False, verbose_name="Whether to display execution details")
    authentication = models.BooleanField(default=False, verbose_name="YesWhether authentication is required")
    authentication_value = models.JSONField(verbose_name="Certificationvalue", default=dict)

    language = models.CharField(max_length=10, verbose_name="language", default=None, null=True)

    class Meta:
        db_table = "application_access_token"
