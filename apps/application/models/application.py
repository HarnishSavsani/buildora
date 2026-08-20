# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： application.py
    @date：2025/5/7 15:29
    @desc:
"""
import uuid_utils.compat as uuid
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.mixins.app_model_mixin import AppModelMixin
from knowledge.models import Knowledge
from models_provider.models import Model
from users.models import User


class ApplicationFolder(MPTTModel, AppModelMixin):
    id = models.CharField(primary_key=True, max_length=64, editable=False, verbose_name="Primary keyid")
    name = models.CharField(max_length=64, verbose_name="folder name", db_index=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="describe")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children')

    class Meta:
        db_table = "application_folder"

    class MPTTMeta:
        order_insertion_by = ['name']


class ApplicationTypeChoices(models.TextChoices):
    """OrderSingleType"""
    SIMPLE = 'SIMPLE', 'simple'
    WORK_FLOW = 'WORK_FLOW', 'Workflow'


def get_dataset_setting_dict():
    return {'top_n': 3, 'similarity': 0.6, 'max_paragraph_char_number': 5000, 'search_mode': 'embedding',
            'no_references_setting': {
                'status': 'ai_questioning',
                'value': '{question}'
            }}


def get_model_setting_dict():
    return {
        'prompt': Application.get_default_model_prompt(),
        'no_references_prompt': '{question}',
        'reasoning_content_start': '<think>',
        'reasoning_content_end': '</think>',
        'reasoning_content_enable': False,
    }


class Application(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    folder = models.ForeignKey(ApplicationFolder, on_delete=models.DO_NOTHING, verbose_name="Folderid",
                               default='default')
    is_publish = models.BooleanField(verbose_name="Whether to publish", default=False)
    name = models.CharField(max_length=128, verbose_name="Application name", db_index=True)
    desc = models.CharField(max_length=512, verbose_name="Quotedescribe", default="")
    prologue = models.CharField(max_length=40960, verbose_name="Opening", default="")
    dialogue_number = models.IntegerField(default=0, verbose_name="SessionQuantity")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    knowledge_setting = models.JSONField(verbose_name="NumberAccording tosetparameterSettings", default=get_dataset_setting_dict)
    model_setting = models.JSONField(verbose_name="Model parametersRelatedSettings", default=get_model_setting_dict)
    model_params_setting = models.JSONField(verbose_name="Model parametersRelatedSettings", default=dict)
    tts_model_params_setting = models.JSONField(verbose_name="Model parametersRelatedSettings", default=dict)
    stt_model_params_setting = models.JSONField(verbose_name="STTModel parametersRelatedSettings", default=dict)
    problem_optimization = models.BooleanField(verbose_name="Problemoptimization", default=False)
    icon = models.CharField(max_length=256, verbose_name="applicationicon", default="./favicon.ico")
    work_flow = models.JSONField(verbose_name="WorkflowNumberAccording to", default=dict)
    type = models.CharField(verbose_name="applicationType", choices=ApplicationTypeChoices.choices,
                            default=ApplicationTypeChoices.SIMPLE, max_length=256)
    problem_optimization_prompt = models.CharField(verbose_name="ProblemoptimizationPrompt words", max_length=102400, blank=True,
                                                   null=True,
                                                   default="()There are user questions,Answer guessing user questions based on context({question}) Requirements: Output a completion question,and put<data></data>in tags")
    tts_model = models.ForeignKey(Model, related_name='tts_model_id', on_delete=models.SET_NULL, db_constraint=False,
                                  blank=True, null=True)
    stt_model = models.ForeignKey(Model, related_name='stt_model_id', on_delete=models.SET_NULL, db_constraint=False,
                                  blank=True, null=True)
    tts_model_enable = models.BooleanField(verbose_name="speech synthesisModelEnable or not", default=False)
    stt_model_enable = models.BooleanField(verbose_name="speech recognition modelEnable or not", default=False)
    tts_type = models.CharField(verbose_name="Voice playback type", max_length=20, default="BROWSER")
    tts_autoplay = models.BooleanField(verbose_name="Auto play", default=False)
    stt_autosend = models.BooleanField(verbose_name="Send automatically", default=False)
    clean_time = models.IntegerField(verbose_name="cleanup time", default=180)
    publish_time = models.DateTimeField(verbose_name="PublishTime", default=None, null=True, blank=True)
    file_upload_enable = models.BooleanField(verbose_name="documentUploadEnable or not", default=False)
    file_upload_setting = models.JSONField(verbose_name="documentUpload relatedSettings", default=dict)
    mcp_enable = models.BooleanField(verbose_name="MCPnoenable", default=False)
    mcp_tool_ids = models.JSONField(verbose_name="MCPtoolIDList", default=list)
    mcp_servers = models.JSONField(verbose_name="MCPServeList", default=dict)
    mcp_source = models.CharField(verbose_name="MCP Source", max_length=20, default="referencing")
    tool_enable = models.BooleanField(verbose_name="toolEnable or not", default=False)
    tool_ids = models.JSONField(verbose_name="toolIDList", default=list)
    application_enable = models.BooleanField(verbose_name="applicationEnable or not", default=False)
    application_ids = models.JSONField(verbose_name="applicationIDList", default=list)
    skill_tool_ids = models.JSONField(verbose_name="SkillIDList", default=list)
    mcp_output_enable = models.BooleanField(verbose_name="MCPoutputEnable or not", default=True)
    file_clean_time = models.IntegerField(verbose_name="documentcleanup time", default=180)
    long_term_enable = models.BooleanField(verbose_name='long term memoryWhether to open', default=False)
    long_term_model = models.ForeignKey(Model, related_name='long_term_model_id', on_delete=models.SET_NULL,
                                        db_constraint=False, blank=True, null=True)
    long_term_model_params_setting = models.JSONField(verbose_name="long term memoryModel parametersRelatedSettings", default=dict)
    long_term_trigger_type = models.CharField(verbose_name='long term memoryTrigger type', default='ROUND')
    long_term_trigger_setting = models.JSONField(verbose_name='Long-term memory triggerConfiguration', default=dict)

    @staticmethod
    def get_default_model_prompt():
        return ("known information："
                "\n{data}"
                "\nAnswer the request："
                "\n- likeIf you don't know the answer or don't have the answer, please answer \"NoInknowledge baseMediumSearcharriveRelated information，It is recommended to consult relevant technical support or refer to the official Documentation.operate”。"
                "\n- Avoid mentioning your Yes from<data></data>Mediumacquired knowledge。"
                "\n- Please keep the answer with<data></data>MediumdescribeConsistency。"
                "\n- pleaseusemarkdown Grammarly optimized answersFormat。"
                "\n- <data></data>MediumofPictureLink、LinkaddressandscriptlanguagepleasewholeReturn。"
                "\n- Please use the same language as Problemanswer。"
                "\nProblem："
                "\n{question}")

    class Meta:
        db_table = "application"


class ApplicationKnowledgeMapping(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    application = models.ForeignKey(Application, on_delete=models.DO_NOTHING)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "application_knowledge_mapping"


class ApplicationVersion(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Version name", max_length=128, default="")
    publish_user_id = models.UUIDField(verbose_name="Publishwhoid", max_length=128, default=None, null=True)
    publish_user_name = models.CharField(verbose_name="PublishAuthor's name", max_length=128, default="")
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    application_name = models.CharField(max_length=128, verbose_name="Application name")
    desc = models.CharField(max_length=512, verbose_name="Quotedescribe", default="")
    prologue = models.CharField(max_length=40960, verbose_name="Opening", default="")
    dialogue_number = models.IntegerField(default=0, verbose_name="SessionQuantity")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    model_id = models.UUIDField(verbose_name="large language model", blank=True, null=True)
    knowledge_setting = models.JSONField(verbose_name="NumberAccording tosetparameterSettings", default=get_dataset_setting_dict)
    model_setting = models.JSONField(verbose_name="Model parametersRelatedSettings", default=get_model_setting_dict)
    model_params_setting = models.JSONField(verbose_name="Model parametersRelatedSettings", default=dict)
    tts_model_params_setting = models.JSONField(verbose_name="Model parametersRelatedSettings", default=dict)
    stt_model_params_setting = models.JSONField(verbose_name="STTModel parametersRelatedSettings", default=dict)
    problem_optimization = models.BooleanField(verbose_name="Problemoptimization", default=False)
    icon = models.CharField(max_length=256, verbose_name="applicationicon", default="./favicon.ico")
    work_flow = models.JSONField(verbose_name="WorkflowNumberAccording to", default=dict)
    type = models.CharField(verbose_name="applicationType", choices=ApplicationTypeChoices.choices,
                            default=ApplicationTypeChoices.SIMPLE, max_length=256)
    problem_optimization_prompt = models.CharField(verbose_name="ProblemoptimizationPrompt words", max_length=102400, blank=True,
                                                   null=True,
                                                   default="()There are user questions,Answer guessing user questions based on context({question}) Requirements: Output a completion question,and put<data></data>in tags")
    tts_model_id = models.UUIDField(verbose_name="textConvert to voiceModelid",
                                    blank=True, null=True)
    stt_model_id = models.UUIDField(verbose_name="voice to speechtextModelid",
                                    blank=True, null=True)
    tts_model_enable = models.BooleanField(verbose_name="speech synthesisModelEnable or not", default=False)
    stt_model_enable = models.BooleanField(verbose_name="speech recognition modelEnable or not", default=False)
    tts_type = models.CharField(verbose_name="Voice playback type", max_length=20, default="BROWSER")
    tts_autoplay = models.BooleanField(verbose_name="Auto play", default=False)
    stt_autosend = models.BooleanField(verbose_name="Send automatically", default=False)
    clean_time = models.IntegerField(verbose_name="cleanup time", default=180)
    file_upload_enable = models.BooleanField(verbose_name="documentUploadEnable or not", default=False)
    file_upload_setting = models.JSONField(verbose_name="documentUpload relatedSettings", default=dict)
    mcp_enable = models.BooleanField(verbose_name="MCPnoenable", default=False)
    mcp_tool_ids = models.JSONField(verbose_name="MCPtoolIDList", default=list)
    mcp_servers = models.JSONField(verbose_name="MCPServeList", default=dict)
    mcp_source = models.CharField(verbose_name="MCP Source", max_length=20, default="referencing")
    tool_enable = models.BooleanField(verbose_name="toolEnable or not", default=False)
    tool_ids = models.JSONField(verbose_name="toolIDList", default=list)
    application_enable = models.BooleanField(verbose_name="applicationEnable or not", default=False)
    application_ids = models.JSONField(verbose_name="applicationIDList", default=list)
    skill_tool_ids = models.JSONField(verbose_name="SkillIDList", default=list)
    mcp_output_enable = models.BooleanField(verbose_name="MCPoutputEnable or not", default=True)
    long_term_enable = models.BooleanField(verbose_name='long term memoryWhether to open', default=False)
    long_term_model_id = models.UUIDField(verbose_name="long term memoryModelid", blank=True, null=True)
    long_term_model_params_setting = models.JSONField(verbose_name="long term memoryModel parametersRelatedSettings", default=dict)
    long_term_trigger_type = models.CharField(verbose_name='long term memoryTrigger type', default='ROUND')
    long_term_trigger_setting = models.JSONField(verbose_name='Long-term memory triggerConfiguration', default=dict)
    knowledge_ids = models.JSONField(verbose_name="NumberAccording tosetidList", default=list)

    class Meta:
        db_table = "application_version"
