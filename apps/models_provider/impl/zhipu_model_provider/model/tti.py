from typing import Dict

from common.config.tokenizer_manage_config import TokenizerManage
from django.utils.translation import gettext
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from zai import ZhipuAiClient

from models_provider.base_model_provider import MaxKBBaseModel
from models_provider.impl.base_tti import BaseTextToImage


def custom_get_token_ids(text: str):
    tokenizer = TokenizerManage.get_tokenizer()
    return tokenizer.encode(text)


class ZhiPuTextToImage(MaxKBBaseModel, BaseTextToImage):
    api_key: str
    base_url: str
    model: str
    params: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get("api_key")
        self.base_url = kwargs.get("base_url")
        self.model = kwargs.get("model")
        self.params = kwargs.get("params")

    @staticmethod
    def is_cache_model():
        return False

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = {"params": {"size": "1024x1024"}}
        for key, value in model_kwargs.items():
            if key not in ["model_id", "use_local", "streaming"]:
                optional_params["params"][key] = value
        return ZhiPuTextToImage(
            model=model_name,
            api_key=model_credential.get("api_key"),
            base_url=model_credential.get("base_url", "https://open.bigmodel.cn/api/paas/v4"),
            **optional_params,
        )

    def check_auth(self):
        chat = ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model,
        )
        chat.invoke([HumanMessage([{"type": "text", "text": gettext("Hello")}])])

        # self.generate_image('generatepieces of kittenPicture')

    def generate_image(self, prompt: str, negative_prompt: str = None):
        chat = ZhipuAiClient(api_key=self.api_key, base_url=self.base_url)
        response = chat.images.generations(
            model=self.model,  # Fill in the Model code that requires Call
            prompt=prompt,  # Fill in the required generatePicturetext
            **self.params,  # Fill in additionalparameter
        )
        file_urls = []
        try:
            for content in response.data:
                url = content.url
                file_urls.append(url)

            return file_urls
        except Exception as e:
            raise e
