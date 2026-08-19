from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

from common.mixins.api_mixin import APIMixin
from common.result import DefaultResultSerializer


class FileUploadAPI(APIMixin):

    @staticmethod
    def get_request():
        return {
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'to be uploadeddocument'

                    },
                    "source_id": {
                        'type': 'string',
                        'description': 'resourceid likeIfsource_typefor[TEMPORARY_30_MINUTE,TEMPORARY_120_MINUTE,TEMPORARY_1_DAY,SYSTEM] otherThe reasoning ofid'
                    },
                    "source_type": {
                        'type': 'string',
                        'description': 'Resource type[KNOWLEDGE,APPLICATION,TOOL,DOCUMENT,CHAT,SYSTEM,TEMPORARY_30_MINUTE,TEMPORARY_120_MINUTE,TEMPORARY_1_DAY]'
                    }
                }
            }
        }

    @staticmethod
    def get_response():
        return DefaultResultSerializer


class FileGetAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="file_id",
                description="documentid",
                type=OpenApiTypes.STR,
                location='path',
                required=True,
            ),
        ]

    @staticmethod
    def get_response():
        return DefaultResultSerializer

class GetUrlContentAPI(APIMixin):
    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="url",
                description="documenturl",
                type=OpenApiTypes.STR,
                location='query',
                required=True,
            ),
        ]

    @staticmethod
    def get_response():
        return DefaultResultSerializer