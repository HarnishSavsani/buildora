# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： Trigger.py
    @date：2026/1/14 18:45
    @desc:
"""

from abc import ABC, abstractmethod


class BaseTrigger(ABC):
    """
    triggerabstract
    """

    @abstractmethod
    def support(self, trigger, **kwargs):
        pass

    @abstractmethod
    def deploy(self, trigger, **kwargs):
        pass

    @abstractmethod
    def undeploy(self, trigger, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def execute(trigger, **kwargs):
        pass
