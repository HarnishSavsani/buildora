import uuid_utils.compat as uuid
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.encoder.encoder import SystemEncoder
from common.mixins.app_model_mixin import AppModelMixin
from knowledge.models.knowledge_action import State
from users.models import User


class ToolFolder(MPTTModel, AppModelMixin):
    id = models.CharField(primary_key=True, max_length=64, editable=False, verbose_name="Primary keyid")
    name = models.CharField(max_length=64, verbose_name="folder name", db_index=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="describe")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children')

    class Meta:
        db_table = "tool_folder"

    class MPTTMeta:
        order_insertion_by = ['name']


class ToolScope(models.TextChoices):
    SHARED = "SHARED", 'commonEnjoy'
    WORKSPACE = "WORKSPACE", "WorkspaceAvailable"
    INTERNAL = "INTERNAL", 'built-in'


class ToolType(models.TextChoices):
    INTERNAL = "INTERNAL", 'built-in'
    CUSTOM = "CUSTOM", "Customize"
    SKILL = "SKILL", "Skill"
    MCP = "MCP", "MCPtool"
    DATA_SOURCE = "DATA_SOURCE", "NumberAccording tosource"
    WORKFLOW = "WORKFLOW", "Workflow"


class ToolTaskTypeChoices(models.TextChoices):
    APPLICATION = 'APPLICATION'
    KNOWLEDGE = 'KNOWLEDGE'
    TOOL = 'TOOL'
    TRIGGER = 'TRIGGER'


class Tool(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    name = models.CharField(max_length=64, verbose_name="Tool name", db_index=True)
    desc = models.CharField(max_length=128, verbose_name="describe")
    code = models.CharField(max_length=102400, verbose_name="pythoncode")
    input_field_list = models.JSONField(verbose_name="Input field list", default=list)
    init_field_list = models.JSONField(verbose_name="start upFieldsList", default=list)
    icon = models.CharField(max_length=256, verbose_name="Tool libraryicon", default="")
    is_active = models.BooleanField(default=True, db_index=True)
    scope = models.CharField(max_length=20, verbose_name='AvailableRange', choices=ToolScope.choices,
                             default=ToolScope.WORKSPACE, db_index=True)
    tool_type = models.CharField(max_length=20, verbose_name='toolType', choices=ToolType.choices,
                                 default=ToolType.CUSTOM, db_index=True)
    template_id = models.CharField(max_length=128, verbose_name="Templateid", null=True, default=None, db_index=True)
    folder = models.ForeignKey(ToolFolder, on_delete=models.DO_NOTHING, verbose_name="Folderid", default='default')
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    init_params = models.CharField(max_length=102400, verbose_name="Initializationparameter", null=True)
    label = models.CharField(max_length=128, verbose_name="Tags", null=True, db_index=True)
    version = models.CharField(max_length=64, verbose_name="VersionNumber", null=True, default=None)

    class Meta:
        db_table = "tool"


class ToolRecord(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    source_type = models.CharField(verbose_name="trigger taskType", choices=ToolTaskTypeChoices.choices,
                                   default=ToolTaskTypeChoices.APPLICATION, max_length=256)
    source_id = models.UUIDField(verbose_name="resourceid")
    meta = models.JSONField(default=dict, encoder=SystemEncoder)
    state = models.CharField(verbose_name='state', max_length=20, choices=State.choices, default=State.STARTED)
    run_time = models.FloatField(verbose_name="runDuration", default=0)

    class Meta:
        db_table = "tool_record"
