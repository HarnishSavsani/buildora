# coding=utf-8
from typing import Dict

from django.utils.translation import gettext_lazy as _, gettext

from common import forms
from common.exception.app_exception import AppApiException
from common.forms import BaseForm, TooltipLabel
from models_provider.base_model_provider import BaseModelCredential, ValidCode


class XInferenceTTSModelGeneralParams(BaseForm):
    # ['indian female', 'indian male', 'Japanese male', 'Cantonese female', 'English female', 'English male', 'Korean female']
    voice = forms.SingleSelect(
        TooltipLabel(_('timbre'), ''),
        required=True, default_value='indian female',
        text_field='value',
        value_field='value',
        option_list=[
            {'text': _('indian female'), 'value': 'indian female'},
            {'text': _('indian male'), 'value': 'indian male'},
            {'text': _('Japanese male'), 'value': 'Japanese male'},
            {'text': _('Cantonese female'), 'value': 'Cantonese female'},
            {'text': _('English female'), 'value': 'English female'},
            {'text': _('English male'), 'value': 'English male'},
            {'text': _('Korean female'), 'value': 'Korean female'},
        ])


class XInferenceTTSModelCredential(BaseForm, BaseModelCredential):
    api_base = forms.TextInputField('API URL', required=True)
    api_key = forms.PasswordInputField('API Key', required=True)

    def is_valid(self, model_type: str, model_name, model_credential: Dict[str, object], model_params, provider,
                 raise_exception=False):
        model_type_list = provider.get_model_type_list()
        if not any(list(filter(lambda mt: mt.get('value') == model_type, model_type_list))):
            raise AppApiException(ValidCode.valid_error.value,
                                  gettext('{model_type} Model type is not supported').format(model_type=model_type))

        for key in ['api_base', 'api_key']:
            if key not in model_credential:
                if raise_exception:
                    raise AppApiException(ValidCode.valid_error.value, gettext('{key}  is required').format(key=key))
                else:
                    return False
        try:
            model = provider.get_model(model_type, model_name, model_credential, **model_params)
            model.check_auth()
        except Exception as e:
            if isinstance(e, AppApiException):
                raise e
            if raise_exception:
                raise AppApiException(ValidCode.valid_error.value,
                                      gettext(
                                          'Verification failed, please check whether the parameters are correct: {error}').format(
                                          error=str(e)))
            else:
                return False
        return True

    def encryption_dict(self, model: Dict[str, object]):
        return {**model, 'api_key': super().encryption(model.get('api_key', ''))}

    def get_model_params_setting_form(self, model_name):
        return XInferenceTTSModelGeneralParams()
