from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

from common.mixins.api_mixin import APIMixin
from common.result import ResultSerializer, DefaultResultSerializer
from knowledge.serializers.common import BatchSerializer, BatchMoveSerializer
from knowledge.serializers.common import GenerateRelatedSerializer
from knowledge.serializers.knowledge import KnowledgeBaseCreateRequest, KnowledgeModelSerializer, KnowledgeEditRequest, \
    KnowledgeWebCreateRequest, HitTestSerializer, KnowledgeImportRequest


class KnowledgeCreateResponse(ResultSerializer):
    def get_data(self):
        return KnowledgeModelSerializer()


class KnowledgeReadAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="knowledge_id",
                description="knowledge baseid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            )
        ]

    @staticmethod
    def get_response():
        return KnowledgeCreateResponse


class KnowledgeBaseCreateAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            )
        ]

    @staticmethod
    def get_request():
        return KnowledgeBaseCreateRequest

    @staticmethod
    def get_response():
        return KnowledgeCreateResponse


class KnowledgeWebCreateAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            )
        ]

    @staticmethod
    def get_request():
        return KnowledgeWebCreateRequest

    @staticmethod
    def get_response():
        return KnowledgeCreateResponse


class KnowledgeEditAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="knowledge_id",
                description="knowledge baseid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            )
        ]

    @staticmethod
    def get_request():
        return KnowledgeEditRequest

    @staticmethod
    def get_response():
        return KnowledgeCreateResponse


class KnowledgeTreeReadAPI(KnowledgeReadAPI):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="folder_id",
                description="Folderid",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            ),
            OpenApiParameter(
                name="user_id",
                description="Usersid",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
            OpenApiParameter(
                name="name",
                description="Name",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
            OpenApiParameter(
                name="desc",
                description="describe",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
        ]


class KnowledgePageAPI(KnowledgeReadAPI):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="current_page",
                description="Current pagecode",
                type=OpenApiTypes.INT,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="page_size",
                description="strips per pageNumber",
                type=OpenApiTypes.INT,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="folder_id",
                description="Folderid",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            ),
            OpenApiParameter(
                name="name",
                description="Name",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
            OpenApiParameter(
                name="desc",
                description="describe",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
        ]


class SyncWebAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="knowledge_id",
                description="knowledge baseid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="sync_type",
                description="Sync type (replace: Replacementsynchronous, complete: full sync)",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            ),
        ]

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class GenerateRelatedAPI(SyncWebAPI):
    @staticmethod
    def get_request():
        return GenerateRelatedSerializer


class HitTestAPI(SyncWebAPI):
    @staticmethod
    def get_request():
        return HitTestSerializer


class EmbeddingAPI(SyncWebAPI):
    pass


class GetModelAPI(SyncWebAPI):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
        ]

    @staticmethod
    def get_response():
        return DefaultResultSerializer

class KnowledgeExportAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="knowledge_id",
                description="knowledge baseid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="with_source_file",
                description="YesNoExportoriginaldocument",
                type=OpenApiTypes.BOOL,
                location='query',
                required=False,
            ),
        ]

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class KnowledgeBatchOperateAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            )
        ]

    @staticmethod
    def get_request():
        return BatchSerializer

    @staticmethod
    def get_move_request():
        return BatchMoveSerializer


class KnowledgeImportAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="workspace_id",
                description="Workspaceid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
        ]

    @staticmethod
    def get_request():
        return KnowledgeImportRequest

    @staticmethod
    def get_response():
        return DefaultResultSerializer
