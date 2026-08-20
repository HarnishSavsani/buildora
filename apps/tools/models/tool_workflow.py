# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： tool_workflow.py
    @date：2026/3/3 13:59
    @desc:
"""
from django.db import models

from common.mixins.app_model_mixin import AppModelMixin
import uuid_utils.compat as uuid

from tools.models import Tool


class ToolWorkflow(AppModelMixin):
    """
    knowledge baseWorkflowsurface
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    tool = models.OneToOneField(Tool, on_delete=models.CASCADE, verbose_name="tool",
                                db_constraint=False, related_name='workflow')
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    work_flow = models.JSONField(verbose_name="WorkflowNumberAccording to", default=dict)
    is_publish = models.BooleanField(verbose_name="Whether to publish", default=False, db_index=True)
    publish_time = models.DateTimeField(verbose_name="PublishTime", null=True, blank=True)

    class Meta:
        db_table = "tool_workflow"


class ToolWorkflowVersion(AppModelMixin):
    """
    knowledge baseWorkflow versionsurface - Record Workflow historyVersion
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, verbose_name="tool", db_constraint=False)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    name = models.CharField(verbose_name="Version name", max_length=128, default="")
    work_flow = models.JSONField(verbose_name="WorkflowNumberAccording to", default=dict)
    publish_user_id = models.UUIDField(verbose_name="Publishwhoid", max_length=128, default=None, null=True)
    publish_user_name = models.CharField(verbose_name="PublishAuthor's name", max_length=128, default="")

    class Meta:
        db_table = "tool_workflow_version"
