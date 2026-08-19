# apps/trigger/tasks.py
# coding=utf-8
from __future__ import annotations

# Operationfor Celery autodiscover Entry, ensure that the task module is imported to complete the registration
from trigger.handler.impl.trigger.scheduled_trigger import deploy_scheduled_trigger  # noqa: F401
