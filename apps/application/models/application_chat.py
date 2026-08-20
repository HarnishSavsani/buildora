# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： application_chat_log.py
    @date：2025/5/29 17:12
    @desc:
"""
import uuid_utils.compat as uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _
from langchain_core.messages import HumanMessage, AIMessage

from application.models import Application
from common.encoder.encoder import SystemEncoder
from common.mixins.app_model_mixin import AppModelMixin
from users.models import User


class ChatUserType(models.TextChoices):
    ANONYMOUS_USER = "ANONYMOUS_USER", 'anonymousUsers'
    CHAT_USER = "CHAT_USER", "Dialog users"
    SYSTEM_API_KEY = "SYSTEM_API_KEY", "systemAPI_KEY"
    APPLICATION_API_KEY = "APPLICATION_API_KEY", "applicationAPI_KEY"
    PLATFORM_USER = "PLATFORM_USER", "platformUsers"


def default_asker():
    return {'username': 'tourists'}


class Chat(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    abstract = models.CharField(max_length=1024, verbose_name="summary")
    chat_user_id = models.CharField(verbose_name="Dialog usersid", default=None, null=True)
    chat_user_type = models.CharField(max_length=64, verbose_name="Client type", choices=ChatUserType.choices,
                                      default=ChatUserType.ANONYMOUS_USER)
    is_deleted = models.BooleanField(verbose_name="logicDelete", default=False)
    asker = models.JSONField(verbose_name="Visitor", default=default_asker, encoder=SystemEncoder)
    meta = models.JSONField(verbose_name="Metadata", default=dict)
    star_num = models.IntegerField(verbose_name="Number of likes", default=0)
    trample_num = models.IntegerField(verbose_name="Number of clicks and dislikes", default=0)
    chat_record_count = models.IntegerField(verbose_name="ConversationSecond-rateNumber", default=0)
    mark_sum = models.IntegerField(verbose_name="markQuantity", default=0)
    source = models.JSONField(verbose_name="source", default=dict)
    ip_address = models.CharField(max_length=128, verbose_name="ipaddress", default='')

    class Meta:
        db_table = "application_chat"


class VoteChoices(models.TextChoices):
    """OrderSingleType"""
    UN_VOTE = "-1", 'Not voted'
    STAR = "0", 'Agree'
    TRAMPLE = "1", 'be opposed to'


class VoteReasonChoices(models.TextChoices):
    ACCURATE = 'accurate', 'Accurate content'
    COMPLETE = 'complete', 'Improved content'
    INACCURATE = 'inaccurate', 'Inaccurate content'
    INCOMPLETE = 'incomplete', 'Incomplete content'
    OTHER = 'other', 'other'

class ShareLinkType(models.TextChoices):
    PUBLIC = "PUBLIC", 'public'
    PRIVATE = "PRIVATE", 'private'

class ChatSourceChoices(models.TextChoices):
    ONLINE = "ONLINE", "Use online"
    API_CALL = "API_CALL", "APICall"
    ENTERPRISE_WECHAT = "ENTERPRISE_WECHAT", "Business WeChat"
    WECHAT_PUBLIC_ACCOUNT = "WECHAT_PUBLIC_ACCOUNT", "WeChat public account"
    LARK = "LARK", "Feishu"
    DINGTALK = "DINGTALK", "DingTalk"
    ENTERPRISE_WECHAT_ROBOT = "ENTERPRISE_WECHAT_ROBOT", "Enterprise WeChat robot"
    TRIGGER = "TRIGGER", "trigger"
    SLACK = "SLACK", "Slack"


class ChatRecord(AppModelMixin):
    """
    Conversation log Details
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    vote_status = models.CharField(verbose_name='vote', max_length=10, choices=VoteChoices.choices,
                                   default=VoteChoices.UN_VOTE)
    vote_reason = models.CharField(verbose_name='Reason for voting', max_length=50, choices=VoteReasonChoices.choices, null=True,
                                   blank=True)
    vote_other_content = models.CharField(verbose_name='otherreason', max_length=1024, default='')
    problem_text = models.CharField(max_length=10240, verbose_name="Problem")
    answer_text = models.CharField(max_length=40960, verbose_name="Answer")
    answer_text_list = ArrayField(verbose_name="ImprovementAnnotationsList",
                                  base_field=models.JSONField()
                                  , default=list)
    message_tokens = models.IntegerField(verbose_name="asktokenQuantity", default=0)
    answer_tokens = models.IntegerField(verbose_name="ResponsetokenQuantity", default=0)
    const = models.IntegerField(verbose_name="total cost", default=0)
    details = models.JSONField(verbose_name="ConversationDetails", default=dict, encoder=SystemEncoder)
    improve_paragraph_id_list = ArrayField(verbose_name="ImprovementAnnotationsList",
                                           base_field=models.UUIDField(max_length=128, blank=True)
                                           , default=list)
    run_time = models.FloatField(verbose_name="runDuration", default=0)
    index = models.IntegerField(verbose_name="Conversationsubscript")
    source = models.JSONField(verbose_name="source", default=dict)
    ip_address = models.CharField(max_length=128, verbose_name="ipaddress", default='')

    def get_human_message(self):
        if 'problem_padding' in self.details:
            return HumanMessage(content=self.details.get('problem_padding').get('padding_problem_text'))
        return HumanMessage(content=self.problem_text)

    def get_ai_message(self):
        answer_text = self.answer_text
        if answer_text is None or len(str(answer_text).strip()) == 0:
            answer_text = _(
                'Sorry, no relevant content was found. Please re-describe your problem or provide more information. ')
        return AIMessage(content=answer_text)

    def get_node_details_runtime_node_id(self, runtime_node_id):
        return self.details.get(runtime_node_id, None)

    class Meta:
        db_table = "application_chat_record"


class ApplicationChatUserStats(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    chat_user_id = models.UUIDField(max_length=128, default=uuid.uuid7, verbose_name="Dialog usersid")
    chat_user_type = models.CharField(max_length=64, verbose_name="Dialogue user type", choices=ChatUserType.choices,
                                      default=ChatUserType.ANONYMOUS_USER)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name="applicationid")
    access_num = models.IntegerField(default=0, verbose_name="Total visitsNumber timesNumber")
    intraday_access_num = models.IntegerField(default=0, verbose_name="whendayVisits")

    class Meta:
        db_table = "application_chat_user_stats"
        indexes = [
            models.Index(fields=['application_id', 'chat_user_id']),
        ]

class ChatShareLink(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    share_type = models.CharField(max_length=20, choices=ShareLinkType.choices, default=ShareLinkType.PUBLIC)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    chat_record_ids = ArrayField(base_field=models.UUIDField(max_length=128))

    class Meta:
        db_table = "application_chat_share_link"



class ApplicationLongTermMemory(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    application = models.ForeignKey(Application, on_delete=models.CASCADE, db_constraint=False, verbose_name="Belongs toapplication")
    chat_user_id = models.CharField( max_length=128, verbose_name="Dialog usersid", db_index=True)
    memory = models.TextField(verbose_name="long term memorycontent", default="")

    class Meta:
        db_table = "application_long_term_memory"
        unique_together = [('application', 'chat_user_id')]
        indexes = [
            models.Index(fields=['application_id', 'chat_user_id']),
        ]
