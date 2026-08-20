# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Tiger
    @file： app_model_mixin.py
    @date：2023/9/21 9:41
    @desc:
"""
from django.db import models


class AppModelMixin(models.Model):
    objects = models.Manager()

    create_time = models.DateTimeField(verbose_name="Creation time", auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(verbose_name="modification time", auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['create_time']
