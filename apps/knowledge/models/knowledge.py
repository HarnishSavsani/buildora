import io
import zipfile
from enum import Enum

import uuid_utils.compat as uuid
from common.db.sql_execute import select_one
from common.mixins.app_model_mixin import AppModelMixin
from common.utils.common import get_sha256_hash
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from models_provider.models import Model
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from users.models import User


class KnowledgeType(models.IntegerChoices):
    BASE = 0, "UniversalType"
    WEB = 1, "websiteType"
    LARK = 2, "FeishuType"
    YUQUE = 3, "YuqueType"
    WORKFLOW = 4, "WorkflowType"


class TaskType(Enum):
    # vector
    EMBEDDING = 1
    # generate questions
    GENERATE_PROBLEM = 2
    # synchronous
    SYNC = 3
    # index
    TOKENIZE = 4


class State(Enum):
    # etc.To be
    PENDING = "0"
    # implementMedium
    STARTED = "1"
    # success
    SUCCESS = "2"
    # Failed
    FAILURE = "3"
    # Cancel task
    REVOKE = "4"
    # Cancelsuccess
    REVOKED = "5"
    # neglect
    IGNORED = "n"


class KnowledgeScope(models.TextChoices):
    SHARED = "SHARED", "commonEnjoy"
    WORKSPACE = "WORKSPACE", "WorkspaceAvailable"


class HitHandlingMethod(models.TextChoices):
    optimization = "optimization", "Modeloptimization"
    directly_return = "directly_return", "DirectReturn"


class Status:
    type_cls = TaskType
    state_cls = State

    def __init__(self, status: str = None):
        self.task_status = {}
        status_list = list(status[::-1] if status is not None else "")
        for _type in self.type_cls:
            index = _type.value - 1
            _state = self.state_cls(status_list[index] if len(status_list) > index else "n")
            self.task_status[_type] = _state

    @staticmethod
    def of(status: str):
        return Status(status)

    def __str__(self):
        result = []
        for _type in sorted(self.type_cls, key=lambda item: item.value, reverse=True):
            result.insert(len(self.type_cls) - _type.value, self.task_status[_type].value)
        return "".join(result)

    def __setitem__(self, key, value):
        self.task_status[key] = value

    def __getitem__(self, item):
        return self.task_status[item]

    def update_status(self, task_type: TaskType, state: State):
        self.task_status[task_type] = state


def default_status_meta():
    return {"state_time": {}}


class KnowledgeFolder(MPTTModel, AppModelMixin):
    id = models.CharField(primary_key=True, max_length=64, editable=False, verbose_name="Primary keyid")
    name = models.CharField(max_length=64, verbose_name="folder name", db_index=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="describe")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    parent = TreeForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="children")

    class Meta:
        db_table = "knowledge_folder"

    class MPTTMeta:
        order_insertion_by = ["name"]


class Knowledge(AppModelMixin):
    """
    knowledge basesurface
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    name = models.CharField(max_length=150, verbose_name="Knowledge base name", db_index=True)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    desc = models.CharField(max_length=256, verbose_name="describe")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    type = models.IntegerField(
        verbose_name="Type", choices=KnowledgeType.choices, default=KnowledgeType.BASE, db_index=True
    )
    scope = models.CharField(
        max_length=20,
        verbose_name="AvailableRange",
        choices=KnowledgeScope.choices,
        default=KnowledgeScope.WORKSPACE,
        db_index=True,
    )
    folder = models.ForeignKey(KnowledgeFolder, on_delete=models.DO_NOTHING, verbose_name="Folderid", default="default")
    embedding_model = models.ForeignKey(Model, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    file_size_limit = models.IntegerField(verbose_name="File size limit", default=100)
    file_count_limit = models.IntegerField(verbose_name="File quantity limit", default=50)
    meta = models.JSONField(verbose_name="Metadata", default=dict)

    class Meta:
        db_table = "knowledge"


class KnowledgeWorkflow(AppModelMixin):
    """
    knowledge baseWorkflowsurface
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.OneToOneField(
        Knowledge, on_delete=models.CASCADE, verbose_name="knowledge base", db_constraint=False, related_name="workflow"
    )
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    work_flow = models.JSONField(verbose_name="WorkflowNumberAccording to", default=dict)
    is_publish = models.BooleanField(verbose_name="Whether to publish", default=False, db_index=True)
    publish_time = models.DateTimeField(verbose_name="PublishTime", null=True, blank=True)

    class Meta:
        db_table = "knowledge_workflow"


class KnowledgeWorkflowVersion(AppModelMixin):
    """
    knowledge baseWorkflow versionsurface - Record Workflow historyVersion
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE, verbose_name="knowledge base", db_constraint=False)
    workspace_id = models.CharField(max_length=64, verbose_name="Workspaceid", default="default", db_index=True)
    name = models.CharField(verbose_name="Version name", max_length=128, default="")
    work_flow = models.JSONField(verbose_name="WorkflowNumberAccording to", default=dict)
    publish_user_id = models.UUIDField(verbose_name="Publishwhoid", max_length=128, default=None, null=True)
    publish_user_name = models.CharField(verbose_name="PublishAuthor's name", max_length=128, default="")

    class Meta:
        db_table = "knowledge_workflow_version"


def get_default_status():
    return Status("").__str__()


class Document(AppModelMixin):
    """
    Documentationsurface
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING, verbose_name="knowledge baseid")
    name = models.CharField(max_length=150, verbose_name="Document name", db_index=True)
    char_length = models.IntegerField(verbose_name="DocumentationcharacterNumber RedundantFields")
    status = models.CharField(verbose_name="state", max_length=20, default=get_default_status, db_index=True)
    status_meta = models.JSONField(verbose_name="statestatisticsNumberAccording to", default=default_status_meta)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    type = models.IntegerField(
        verbose_name="Type", choices=KnowledgeType.choices, default=KnowledgeType.BASE, db_index=True
    )
    hit_handling_method = models.CharField(
        verbose_name="Hit handling",
        max_length=20,
        choices=HitHandlingMethod.choices,
        default=HitHandlingMethod.optimization,
    )
    directly_return_similarity = models.FloatField(verbose_name="direct answerSimilarity", default=0.9)

    meta = models.JSONField(verbose_name="Metadata", default=dict)

    class Meta:
        db_table = "document"


class Tag(AppModelMixin):
    """
    Tagssurface - Store the key-value definition of Tags
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING, verbose_name="knowledge base", db_constraint=False)
    key = models.CharField(max_length=64, verbose_name="TagsKey", db_index=True)
    value = models.CharField(max_length=128, verbose_name="Tag value", db_index=True)

    class Meta:
        db_table = "tag"
        unique_together = [["knowledge", "key", "value"]]  # Insameknowledge baseThe key-value combination is unique within
        indexes = [
            models.Index(fields=["knowledge", "key"]),
        ]


class DocumentTag(AppModelMixin):
    """
    DocumentationTagsassociation table
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, verbose_name="Documentation", db_constraint=False)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, verbose_name="Tags", db_constraint=False)

    class Meta:
        db_table = "document_tag"
        unique_together = [["document", "tag"]]  # DocumentationandTagsThe only combination


class Paragraph(AppModelMixin):
    """
    paragraphsurface
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, db_constraint=False)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=102400, verbose_name="Paragraph content")
    title = models.CharField(max_length=256, verbose_name="Title", default="", db_index=True)
    status = models.CharField(verbose_name="state", max_length=20, default=get_default_status, db_index=True)
    status_meta = models.JSONField(verbose_name="stateNumberAccording to", default=default_status_meta)
    hit_num = models.IntegerField(verbose_name="Medium timesNumber", default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    position = models.IntegerField(verbose_name="paragraphSequence", default=0, db_index=True)
    chunks = ArrayField(verbose_name="piece", base_field=models.CharField(), default=list)

    class Meta:
        db_table = "paragraph"


class Problem(AppModelMixin):
    """
    Problemsurface
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING, db_constraint=False)
    content = models.CharField(max_length=256, verbose_name="Problemcontent", db_index=True)
    hit_num = models.IntegerField(verbose_name="Medium timesNumber", default=0)

    class Meta:
        db_table = "problem"


class ProblemParagraphMapping(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING, db_constraint=False)
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, db_constraint=False)
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING, db_constraint=False)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.DO_NOTHING, db_constraint=False)

    class Meta:
        db_table = "problem_paragraph_mapping"


class Termbase(AppModelMixin):
    """
    Glossary
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING, db_constraint=False)
    content = models.CharField(max_length=256, verbose_name="Terminologycontent", db_index=True)

    class Meta:
        db_table = "termbase"


class SourceType(models.IntegerChoices):
    """OrderSingleType"""

    PROBLEM = 0, "Problem"
    PARAGRAPH = 1, "paragraph"
    TITLE = 2, "Title"


class SearchMode(models.TextChoices):
    embedding = "embedding"
    keywords = "keywords"
    blend = "blend"


class FileSourceType(models.TextChoices):
    # knowledge base  followknowledge baseDelete byDelete source_id forknowledge baseid
    KNOWLEDGE = "KNOWLEDGE"
    # application  Following the application being deleted, it isDelete source_id forapplicationid
    APPLICATION = "APPLICATION"
    # tool  Following tool is Delete and isDelete source_id forapplicationid
    TOOL = "TOOL"
    # Documentation
    DOCUMENT = "DOCUMENT"
    # Conversation
    CHAT = "CHAT"
    SYSTEM = "SYSTEM"
    # Temporary 30 minutes NumberAccording to30Cleaned up after minutes source_id forTEMPORARY_30_MINUTE
    TEMPORARY_30_MINUTE = "TEMPORARY_30_MINUTE"
    # Temporary 120 minutes NumberAccording to120Cleaned up after minutes source_idforTEMPORARY_100_MINUTE
    TEMPORARY_120_MINUTE = "TEMPORARY_120_MINUTE"
    # Temporary1sky NumberAccording to1skylater cleared source_idforTEMPORARY_1_DAY
    TEMPORARY_1_DAY = "TEMPORARY_1_DAY"


class VectorField(models.Field):
    def db_type(self, connection):
        return "vector"


class Embedding(models.Model):
    id = models.CharField(max_length=128, primary_key=True, verbose_name="Primary keyid")
    source_id = models.CharField(max_length=128, verbose_name="resourceid", db_index=True)
    source_type = models.CharField(
        verbose_name="Resource type", max_length=5, choices=SourceType.choices, default=SourceType.PROBLEM, db_index=True
    )
    is_active = models.BooleanField(verbose_name="YesnoAvailable", max_length=1, default=True)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.DO_NOTHING, verbose_name="Documentationassociation", db_constraint=False)
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, verbose_name="Documentationassociation", db_constraint=False)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.DO_NOTHING, verbose_name="paragraphassociation", db_constraint=False)
    embedding = VectorField(verbose_name="vector")
    search_vector = SearchVectorField(verbose_name="participle", default="")
    meta = models.JSONField(verbose_name="Metadata", default=dict)

    class Meta:
        db_table = "embedding"


class File(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="Primary keyid")
    file_name = models.CharField(max_length=256, verbose_name="documentName", default="")
    file_size = models.IntegerField(verbose_name="documentsize", default=0)
    sha256_hash = models.CharField(verbose_name="documentsha256_hashlogo", default="")
    source_type = models.CharField(
        verbose_name="Resource type",
        choices=FileSourceType,
        default=FileSourceType.TEMPORARY_120_MINUTE.value,
        db_index=True,
    )
    source_id = models.CharField(
        verbose_name="resourceid", default=FileSourceType.TEMPORARY_120_MINUTE.value, db_index=True
    )
    loid = models.IntegerField(verbose_name="loid")
    meta = models.JSONField(verbose_name="documentassociationNumberAccording to", default=dict)

    class Meta:
        db_table = "file"

    def save(self, bytea=None, force_insert=False, force_update=False, using=None, update_fields=None):
        if bytea is None:
            raise ValueError("byteaparametercannot be empty")

        sha256_hash = get_sha256_hash(bytea)
        self.sha256_hash = sha256_hash
        existing_file = QuerySet(File).filter(sha256_hash=sha256_hash).first()
        if existing_file:
            self.loid = existing_file.loid
            self.file_size = existing_file.file_size
            return super().save()

        compressed_data = self._compress_data(bytea)
        self.file_size = len(compressed_data)

        self.loid = self._create_large_object()

        self._write_compressed_data(compressed_data)
        # CallParent class save
        return super().save()

    def _compress_data(self, data, compression_level=9):
        """compressionNumberAccording toarriveMemory"""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zipinfo = zipfile.ZipInfo(self.file_name)
            zipinfo.compress_type = zipfile.ZIP_DEFLATED
            zip_file.writestr(zipinfo, data, compresslevel=compression_level)

        return buffer.getvalue()

    def _create_large_object(self):
        result = select_one("SELECT lo_creat(-1)::int8 as lo_id;", [])
        return result["lo_id"]

    def _write_compressed_data(self, data, block_size=64 * 1024):
        buffer = io.BytesIO(data)
        offset = 0

        while True:
            chunk = buffer.read(block_size)
            if not chunk:
                break

            offset += len(chunk)
            select_one(
                "SELECT lo_put(%s::oid, %s::bigint, %s::bytea)::VARCHAR;", [self.loid, offset - len(chunk), chunk]
            )

    def get_bytes(self):
        buffer = io.BytesIO()
        for chunk in self.get_bytes_stream():
            buffer.write(chunk)
        data = buffer.getvalue()
        try:
            # UnzipNumberAccording to
            with zipfile.ZipFile(buffer) as zip_file:
                names = [name for name in zip_file.namelist() if not name.endswith("/")]
                if len(names) != 1:
                    return data
                # use zip The actual entry name stored in thematch
                name = names[0]
                return zip_file.read(name)
        except zipfile.BadZipFile:
            # likeIfNumberAccording toNot YeszipFormat, directly Return the originalNumberAccording to
            return data

    def get_bytes_stream(self, start=0, end=None, chunk_size=64 * 1024):
        def _read_with_offset():
            offset = start
            while True:
                result = select_one(
                    "SELECT lo_get(%s::oid, %s, %s) as chunk",
                    [self.loid, offset, end - offset if end and (end - offset) < chunk_size else chunk_size],
                )
                chunk = result["chunk"] if result else None
                if not chunk:
                    break
                yield chunk
                offset += len(chunk)
                if len(chunk) < chunk_size:
                    break
                if end and offset > end:
                    break

        return _read_with_offset()


@receiver(pre_delete, sender=File)
def on_delete_file(sender, instance, **kwargs):
    exist = QuerySet(File).filter(loid=instance.loid).exclude(id=instance.id).exists()
    if not exist:
        select_one(f"SELECT lo_unlink({instance.loid})", [])


class PublicFileAccess(AppModelMixin):
    """
    Public commondocument access control list
    Record which documents are allowed to be publicly accessed
    """
    id = models.UUIDField(
        primary_key=True,
        max_length=128,
        default=uuid.uuid7,
        editable=False,
        verbose_name="Primary keyid"
    )

    source_type = models.CharField(
        max_length=20,
        choices=[
            ('FILE', 'document'),
            ('APPLICATION', 'application'),
            ('KNOWLEDGE', 'knowledge base'),
        ],
        db_index=True,
        verbose_name="Resource type"
    )
    source_id = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name="resourceID"
    )

    class Meta:
        db_table = 'public_file_access'
        indexes = [
            models.Index(fields=['source_type', 'source_id']),
        ]
