
import time
from typing import Dict

import requests

from common.utils.logger import maxkb_logger
from models_provider.base_model_provider import MaxKBBaseModel
from models_provider.base_ttv import BaseGenerationVideo


class GenerationVideoModel(MaxKBBaseModel, BaseGenerationVideo):
    api_key: str
    api_base: str
    model_name: str
    params: dict
    max_retries: int = 3
    retry_delay: int = 10  # seconds

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get('api_key')
        self.api_base = kwargs.get('api_base', 'https://api.minimaxi.com/v1')
        self.model_name = kwargs.get('model_name')
        self.params = kwargs.get('params', {})
        self.max_retries = kwargs.get('max_retries', 3)
        self.retry_delay = 10

    @staticmethod
    def is_cache_model():
        return False

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = {'params': {}}
        for key, value in model_kwargs.items():
            if key not in ['model_id', 'use_local', 'streaming']:
                optional_params['params'][key] = value

        api_base = model_credential.get('api_base','https://api.minimaxi.com/v1')

        return GenerationVideoModel(
            model_name=model_name,
            api_key=model_credential.get('api_key'),
            api_base=api_base,
            **optional_params,
        )

    def check_auth(self):
        return True

    def _safe_call(self, method, url, **kwargs):
        """Request encapsulation with retry"""
        headers = {"Authorization": f"Bearer {self.api_key}"}

        for attempt in range(self.max_retries):
            try:
                if method.upper() == 'POST':
                    response = requests.post(url, headers=headers, **kwargs)
                elif method.upper() == 'GET':
                    response = requests.get(url, headers=headers, **kwargs)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                response.raise_for_status()
                return response.json()
            except (requests.exceptions.ProxyError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as e:
                maxkb_logger.error(f"⚠️ networkError: {e}，Retrying {attempt + 1}/{self.max_retries}...")
                time.sleep(self.retry_delay)
            except requests.exceptions.HTTPError as e:
                maxkb_logger.error(f"HTTP Error: {e}")
                raise RuntimeError(f"HTTP Request failed: {e.response.text if hasattr(e, 'response') else str(e)}")

        raise RuntimeError("Still failed after multiple retriesconnectarrive MiniMax API，Please check the proxy or networkConfiguration")

    def generate_video(self, prompt, negative_prompt=None, first_frame_url=None, last_frame_url=None, **kwargs):
        """
        generatevideo
        prompt: textdescribe
        negative_prompt: reversetextdescribe（MiniMax Not supported yet, retain parameters for compatible interfaces）
        first_frame_url: Starting KeyframePicture URL (Tusheng videoorFirst and last frame mode)
        last_frame_url: FinishKey framePicture URL (First and last frame mode)

        Return: videodownload URL
        """
        base_url = f"{self.api_base}/video_generation"

        # Build the foundationparameter
        payload = {
            "prompt": prompt,
            "model": self.model_name,
        }

        # RootAccording toProvide the parameter for to judge the generate mode
        if first_frame_url and last_frame_url:
            # Mode 3: First and last frame generate video
            payload["first_frame_image"] = first_frame_url
            payload["last_frame_image"] = last_frame_url
            maxkb_logger.info("useFirst and last frame mode generate video")
        elif first_frame_url:
            # Mode 2：Tusheng video
            payload["first_frame_image"] = first_frame_url
            maxkb_logger.info("useTusheng videoMode")
        else:
            # Mode one：Vincent Video
            maxkb_logger.info("useVincent VideoMode")

        # Merge extraparameter（duration, resolution etc.）
        payload.update(self.params)

        # --- Steps 1: submitTask ---
        maxkb_logger.info(f"submitVideo generate task，Model: {self.model_name}")
        response_data = self._safe_call('POST', base_url, json=payload)

        task_id = response_data.get("task_id")
        if not task_id:
            raise RuntimeError(f"submitTask Failed, notgetarrive task_id: {response_data}")

        maxkb_logger.info(f"Task hassubmit，task_id: {task_id}")

        # --- Steps 2: wheelQuery taskstate ---
        query_url = f"{self.api_base}/query/video_generation"
        file_id = self._poll_task_status(query_url, task_id)

        # --- Steps 3: getVideo download link ---
        video_url = self._get_video_download_url(file_id)

        maxkb_logger.info(f"The video generate is completed! Video URL: {video_url}")
        return video_url

    def _poll_task_status(self, query_url: str, task_id: str) -> str:
        """wheelQuery the task state untilsuccessorFailed"""
        params = {"task_id": task_id}
        max_attempts = 60  # mostwheelQuery 60 times (approx. 10 minute）

        for attempt in range(max_attempts):
            response_data = self._safe_call('GET', query_url, params=params)
            status = response_data.get("status")

            maxkb_logger.info(f"currentTaskstate (Try {attempt + 1}/{max_attempts}): {status}")

            if status == "Success":
                file_id = response_data.get("file_id")
                if not file_id:
                    raise RuntimeError(f"Task succeeded but notgetarrive file_id: {response_data}")
                maxkb_logger.info(f"TaskProcessingsuccess，file_id: {file_id}")
                return file_id
            elif status == "Fail":
                error_msg = response_data.get("error_message", "unknown error")
                maxkb_logger.error(f"videogenerateFailed: {error_msg}")
                raise RuntimeError(f"videogenerateFailed: {error_msg}")
            else:
                # The task is still InProcessingMedium, etc. Continue to query later
                time.sleep(self.retry_delay)

        raise RuntimeError(f"Task timeout: elapsed {max_attempts} Not completed after several rounds of queries")

    def _get_video_download_url(self, file_id: str) -> str:
        """RootAccording to file_id getVideo download link"""
        retrieve_url = f"{self.api_base}/files/retrieve"
        params = {"file_id": file_id}

        response_data = self._safe_call('GET', retrieve_url, params=params)

        file_info = response_data.get("file", {})
        download_url = file_info.get("download_url")

        if not download_url:
            raise RuntimeError(f"getdownloadLinkFailed: {response_data}")

        return download_url
