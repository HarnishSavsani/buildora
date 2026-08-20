# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Tiger
    @file： base_field.py
    @date：2023/10/31 18:07
    @desc:
"""
from enum import Enum
from typing import List, Dict

from common.exception.app_exception import AppApiException
from common.forms.label.base_label import BaseLabel
from django.utils.translation import gettext_lazy as _


class TriggerType(Enum):
    # execution letterNumberget OptionListNumberAccording to
    OPTION_LIST = 'OPTION_LIST'
    # Execution function Numberget sub-tableSingle
    CHILD_FORMS = 'CHILD_FORMS'


class BaseField:
    def __init__(self,
                 input_type: str,
                 label: str or BaseLabel,
                 required: bool = False,
                 default_value: object = None,
                 relation_show_field_dict: Dict = None,
                 relation_trigger_field_dict: Dict = None,
                 trigger_type: TriggerType = TriggerType.OPTION_LIST,
                 attrs: Dict[str, object] = None,
                 props_info: Dict[str, object] = None):
        """

        :param input_type: Fields
        :param label: hint
        :param default_value: default value
        :param relation_show_field_dict:        {field:field_value_list} expressIn fieldhavevalue ,and valueInfield_value_listMedium will only display
        :param relation_trigger_field_dict:     {field:field_value_list} expressIn fieldhavevalue ,And valueInfield_value_listMedium is execution letterNumberget NumberAccording to
        :param trigger_type:                    ExecutorType  OPTION_LISTaskOption_listNumberAccording to CHILD_FORMSRequest subtableSingle
        :param attrs:                           Front endattrNumberAccording to
        :param props_info:                      otherAdditionalinformation
        """
        if props_info is None:
            props_info = {}
        if attrs is None:
            attrs = {}
        self.label = label
        self.attrs = attrs
        self.props_info = props_info
        self.default_value = default_value
        self.input_type = input_type
        self.relation_show_field_dict = {} if relation_show_field_dict is None else relation_show_field_dict
        self.relation_trigger_field_dict = [] if relation_trigger_field_dict is None else relation_trigger_field_dict
        self.required = required
        self.trigger_type = trigger_type

    def is_valid(self, value):
        field_label = self.label.label if hasattr(self.label, 'to_dict') else self.label
        if self.required and value is None:
            raise AppApiException(500,
                                  _('The field {field_label} is required').format(field_label=field_label))

    def to_dict(self, **kwargs):
        return {
            'input_type': self.input_type,
            'label': self.label.to_dict(**kwargs) if hasattr(self.label, 'to_dict') else self.label,
            'required': self.required,
            'default_value': self.default_value,
            'relation_show_field_dict': self.relation_show_field_dict,
            'relation_trigger_field_dict': self.relation_trigger_field_dict,
            'trigger_type': self.trigger_type.value,
            'attrs': self.attrs,
            'props_info': self.props_info,
            **kwargs
        }


class BaseDefaultOptionField(BaseField):
    def __init__(self, input_type: str,
                 label: str,
                 text_field: str,
                 value_field: str,
                 option_list: List[dict],
                 required: bool = False,
                 default_value: object = None,
                 relation_show_field_dict: Dict[str, object] = None,
                 attrs: Dict[str, object] = None,
                 props_info: Dict[str, object] = None):
        """

        :param input_type:           Fields
        :param label:           label
        :param text_field:      text field
        :param value_field:     valueFields
        :param option_list:     OptionalList
        :param required:        Is it required?
        :param default_value:   default value
        :param relation_show_field_dict:        {field:field_value_list} expressIn fieldhavevalue ,and valueInfield_value_listMedium will only display
        :param attrs:                           Front endattrNumberAccording to
        :param props_info:                      otherAdditionalinformation
        """
        super().__init__(input_type, label, required, default_value, relation_show_field_dict,
                         {}, TriggerType.OPTION_LIST, attrs, props_info)
        self.text_field = text_field
        self.value_field = value_field
        self.option_list = option_list

    def to_dict(self, **kwargs):
        return {**super().to_dict(**kwargs), 'text_field': self.text_field, 'value_field': self.value_field,
                'option_list': self.option_list}


class BaseExecField(BaseField):
    def __init__(self,
                 input_type: str,
                 label: str,
                 text_field: str,
                 value_field: str,
                 provider: str,
                 method: str,
                 required: bool = False,
                 default_value: object = None,
                 relation_show_field_dict: Dict = None,
                 relation_trigger_field_dict: Dict = None,
                 trigger_type: TriggerType = TriggerType.OPTION_LIST,
                 attrs: Dict[str, object] = None,
                 props_info: Dict[str, object] = None):
        """

        :param input_type:  Fields
        :param label:  hint
        :param text_field:  text field
        :param value_field: valueFields
        :param provider:    Specifysupplier
        :param method:      Execute supplier letterNumber method
        :param required:    Is it required?
        :param default_value: default value
        :param relation_show_field_dict:        {field:field_value_list} expressIn fieldhavevalue ,and valueInfield_value_listMedium will only display
        :param relation_trigger_field_dict:     {field:field_value_list} expressIn fieldhavevalue ,And valueInfield_value_listMedium is execution letterNumberget NumberAccording to
        :param trigger_type:                    ExecutorType  OPTION_LISTaskOption_listNumberAccording to CHILD_FORMSRequest subtableSingle
        :param attrs:                           Front endattrNumberAccording to
        :param props_info:                      otherAdditionalinformation
        """
        super().__init__(input_type, label, required, default_value, relation_show_field_dict,
                         relation_trigger_field_dict,
                         trigger_type, attrs, props_info)
        self.text_field = text_field
        self.value_field = value_field
        self.provider = provider
        self.method = method

    def to_dict(self, **kwargs):
        return {**super().to_dict(**kwargs), 'text_field': self.text_field, 'value_field': self.value_field,
                'provider': self.provider, 'method': self.method}
