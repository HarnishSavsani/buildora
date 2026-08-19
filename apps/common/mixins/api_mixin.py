# coding=utf-8
"""
    @project: MaxKB
    @Author：TigerTiger
    @file： ApiMixin.py
    @date：2025/4/14 18:03
    @desc:
"""


class APIMixin:
    @staticmethod
    def get_request():
        return None

    @staticmethod
    def get_response():
        return None

    @staticmethod
    def get_parameters():
        """
         return OpenApiParameter(
            # ParametersNameYesdone
            name="done",
            # Yes toParametersRemarks
            description="YesNo completion",
            # SpecifyParametersType
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            # Specify must be given to
            required=True,
            # Specify enumeration items
            enum=[True, False],
        )

        """
        return None
