# coding=utf-8

import json
import logging
from typing import Dict

from django.utils.translation import gettext as _
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

from common.utils.logger import maxkb_logger
from models_provider.base_model_provider import MaxKBBaseModel
from models_provider.impl.base_tti import BaseTextToImage
from models_provider.impl.tencent_model_provider.model.hunyuan import ChatHunyuan


class TencentTextToImageModel(MaxKBBaseModel, BaseTextToImage):
    hunyuan_secret_id: str
    hunyuan_secret_key: str
    model: str
    params: dict

    @staticmethod
    def is_cache_model():
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hunyuan_secret_id = kwargs.get('hunyuan_secret_id')
        self.hunyuan_secret_key = kwargs.get('hunyuan_secret_key')
        self.model = kwargs.get('model_name')
        self.params = kwargs.get('params')

    @staticmethod
    def new_instance(model_type: str, model_name: str, model_credential: Dict[str, object],
                     **model_kwargs) -> 'TencentTextToImageModel':
        optional_params = {'params': {'Style': '201', 'Resolution': '768:768'}}
        for key, value in model_kwargs.items():
            if key not in ['model_id', 'use_local', 'streaming']:
                optional_params['params'][key] = value
        return TencentTextToImageModel(
            model=model_name,
            hunyuan_secret_id=model_credential.get('hunyuan_secret_id'),
            hunyuan_secret_key=model_credential.get('hunyuan_secret_key'),
            **optional_params
        )

    def check_auth(self):
        chat = ChatHunyuan(hunyuan_app_id='111111',
                           hunyuan_secret_id=self.hunyuan_secret_id,
                           hunyuan_secret_key=self.hunyuan_secret_key,
                           model="hunyuan-standard")
        res = chat.invoke(_('Hello'))
        # print(res)

    def generate_image(self, prompt: str, negative_prompt: str = None):
        try:
            # ExampleConvert a pieces authentication object, the input parameters need to be passed inTencent CloudAccount SecretId and SecretKey，NoticeKeys also need to be kept confidential here.
            # codeLeakage may cause SecretId and SecretKey Leakage and threaten the security of all resources under the account. Belowcode example is for reference only, it is recommended to use Keys in a safer way, please see：https://cloud.tencent.com/document/product/1278/85305
            # KeysYou can go to the official website console https://console.cloud.tencent.com/cam/capi conductget
            cred = credential.Credential(self.hunyuan_secret_id, self.hunyuan_secret_key)
            # ExampleChange the pieceshttp option, which is optional and can be skipped if there are no special requirements.
            httpProfile = HttpProfile()
            httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

            # ExampleConvert to piecesclient option, optional, skip without special requirements
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # ExampleConfigure the client object to request Products,clientProfileYesOptional
            client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou", clientProfile)

            # ExampleCreate a pieces request object,Each pieces interface corresponds to a piecesrequest object
            req = models.TextToImageLiteRequest()
            params = {
                "Prompt": prompt,
                "NegativePrompt": negative_prompt,
                "RspImgType": "url",
                **self.params
            }
            req.from_json_string(json.dumps(params))

            # ReturnrespYes an Example of piecesTextToImageLiteResponse, corresponding to the request object
            resp = client.TextToImageLite(req)
            file_urls = []

            file_urls.append(resp.ResultImage)
            return file_urls
        except TencentCloudSDKException as err:
            maxkb_logger.error(f"Tencent Text to Image API call failed: {err}")
            raise RuntimeError(f"Tencent Text to Image API call failed: {err}") from err
