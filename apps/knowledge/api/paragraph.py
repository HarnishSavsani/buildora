from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

from common.mixins.api_mixin import APIMixin
from common.result import DefaultResultSerializer, ResultSerializer
from knowledge.serializers.common import BatchSerializer
from knowledge.serializers.paragraph import ParagraphSerializer, ParagraphBatchGenerateRelatedSerializer
from knowledge.serializers.problem import ProblemSerializer


class ParagraphReadResponse(ResultSerializer):
    @staticmethod
    def get_data():
        return ParagraphSerializer(many=True)


class ParagraphReadAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="title",
                description="Title",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
            OpenApiParameter(
                name="content",
                description="content",
                type=OpenApiTypes.STR,
                location='query',
                required=False,
            ),
        ]

    @staticmethod
    def get_response():
        return ParagraphReadResponse


class ParagraphCreateAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
        ]

    @staticmethod
    def get_request():
        return ParagraphSerializer

    @staticmethod
    def get_response():
        return ParagraphReadResponse


class ParagraphBatchDeleteAPI(ParagraphCreateAPI):
    @staticmethod
    def get_request():
        return BatchSerializer

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class ParagraphBatchGenerateRelatedAPI(ParagraphCreateAPI):
    @staticmethod
    def get_request():
        return ParagraphBatchGenerateRelatedSerializer

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class ParagraphGetAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="paragraph_id",
                description="paragraphid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
        ]


class ParagraphEditAPI(ParagraphGetAPI):

    @staticmethod
    def get_request():
        return ParagraphSerializer

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class ProblemCreateAPI(ParagraphGetAPI):
    @staticmethod
    def get_request():
        return ProblemSerializer

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class UnAssociationAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="paragraph_id",
                description="paragraphid",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            ),
            OpenApiParameter(
                name="problem_id",
                description="Problemid",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            )
        ]


class AssociationAPI(UnAssociationAPI):
    pass


class ParagraphPageAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="current_page",
                description="Current page",
                type=OpenApiTypes.INT,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="page_size",
                description="Per page size",
                type=OpenApiTypes.INT,
                location='path',
                required=True,
            ),
        ]


class ParagraphMigrateAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="target_knowledge_id",
                description="Targetknowledge baseid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="target_document_id",
                description="Target documentid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
        ]

    @staticmethod
    def get_request():
        return BatchSerializer


class ParagraphAdjustOrderAPI(APIMixin):
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
                name="document_id",
                description="Documentationid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
            OpenApiParameter(
                name="paragraph_id",
                description="paragraphid",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            ),
            OpenApiParameter(
                name="new_position",
                description="new order",
                type=OpenApiTypes.INT,
                location='query',
                required=True,
            ),
        ]

    @staticmethod
    def get_response():
        return DefaultResultSerializer
