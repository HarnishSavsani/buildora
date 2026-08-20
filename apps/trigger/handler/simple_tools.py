# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Neural Nexus
    @file： simple_task.py
    @date：2026/1/14 19:18
    @desc:
"""
from threading import Thread

from trigger.handler.impl.task.application_task import ApplicationTask
from trigger.handler.impl.task.tool_task import ToolTask
from trigger.handler.impl.trigger.event_trigger import EventTrigger
from trigger.handler.impl.trigger.scheduled_trigger import ScheduledTrigger

simple_task_handlers = [ApplicationTask(), ToolTask()]

simple_trigger_handlers = [ScheduledTrigger(), EventTrigger()]


def execute(trigger_task, **kwargs):
    """
    implementtrigger task
    @param trigger_task:  trigger taskNumberAccording to
    @param kwargs:        AdditionalNumberAccording to
    @return:
    """
    for simple_task_handler in simple_task_handlers:
        if simple_task_handler.support(trigger_task, **kwargs):
            Thread(target=simple_task_handler.execute, args=(trigger_task,), kwargs=kwargs).start()
            return
    raise Exception("Unsupported ProcessorType")


def deploy(trigger, **kwargs):
    """
    Deploymenttrigger
    @param trigger: triggerCharacterclassicNumberAccording to
    @param kwargs:  AdditionalNumberAccording to
    @return:
    """
    for simple_trigger_handler in simple_trigger_handlers:
        if simple_trigger_handler.support(trigger, **kwargs):
            return simple_trigger_handler.deploy(trigger, **kwargs)
    raise Exception("Not supportedtriggerType")


def undeploy(trigger, **kwargs):
    """
    CancelDeploymenttrigger
    @param trigger: triggerCharacterclassicNumberAccording to
    @param kwargs:  AdditionalNumberAccording to
    @return:
    """
    for simple_trigger_handler in simple_trigger_handlers:
        return simple_trigger_handler.undeploy(trigger, **kwargs)
    raise Exception("Not supportedtriggerType")
