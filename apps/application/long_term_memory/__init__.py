import re
from datetime import timedelta

import uuid_utils.compat as uuid
from django.db.models import Count, QuerySet
from django.utils import timezone
from langchain_core.messages import HumanMessage

from application.models import Chat, ChatRecord, Application, ApplicationLongTermMemory
from common.utils.logger import maxkb_logger
from models_provider.tools import get_model_instance_by_model_workspace_id
from ops import celery_app

long_term_prompt = '''
You Yes A piece of professional Users long-term memory extraction engine. Your only responsibility Yes: accurately identify Users information with lasting value from ConversationMedium, and perform structural fusion with existing memories, outputfor AI Memory of Users portraits used by the assistant for a long time。

## enter
【Existing memory】：
{{existing_memory}}

【BookwheelNewConversation】：
{{new_conversation}}

---

## Extraction threshold (must be met at the same time to extract）

1. **Cross-session reuse value**: This information is still applicable in otherConversationMedium in the future, rather than the current temporary demand
2. **Clearly verifiable**: can be directly supported from the original text of the Conversation, and cannot be inferred, imagined or extended.
3. **Improve answer quality**: After remembering this information，AI The answer will be more accurate or more relevant to the Users

**BelowcontentExtraction prohibited：**
- UsersOne-time temporary Requirements (like "Just use sheet output this time」）
- UsersThe specific content of the question itself (Problem is not Yes memory）
- Inference that cannot be directly proven from the original text of Conversation
- Chat, greetings, thank you, etc. No amount of informationcontent
- AI ofAnswer content（Extract only the Users sideinformation）

---

## Four types of memory classification and fusion rules

### 【Preferences] Interaction preferences
UsersYes to「AI likeThe stable expectation of "how to respond" must be clearly stated or reflected repeatedly in multiple wheelMedium before it can be entered.。

Common dimensions: answer in detail / languageStyle（formal/colloquial）/ Output format（sheet/List/paragraph）/ YesDo you want to give an example? / codeStylePreference / replylanguage

fusion rules：
- New preferences appear in the same dimension → **Overwrite ** old value, end of entryAnnotations `※alreadyrenew`
- new dimension → append directly
- No new certificate for old preferencesAccording tobut not denied → **reserve**

---

### 【Background】UsersBackground
UsersThe objective identity and environment information is highly stable and Users will not be actively changed unless explicitly corrected.。

Common dimensions: occupation/Role / In industry / Technology stackand proficiency / useProductsorsystem / Team size / In region

fusion rules：
- Conflict with old memories → **Based on the new Conversationfor**，Annotations `※alreadyrenew`，Deleteoldvalue
- Newinformation → Append
- informationFuzzy cannot confirm → When appendingAnnotations `※To be confirmed`

---

### 【Agreement】Explicit agreement
UsersClearRequirements AI Fixed compliance with the line for rules must be supported by clear instructional language and cannot be interpreted by yourself。

Common dimensions: forbidden rowsfor / fixed execution action / Specific trigger word response / contentboundary / outputlimit

fusion rules：
- New rules of the same kind → **Overwrite old rules，Annotations `※alreadyrenew`
- Newrule → Append
- UsersClarify the rules for Cancel → **DirectDelete**

---

### 【Target】currentTarget
UsersSpecific Targets that are being promoted in the near future or long term will help AI Proactively provide more relevant Help。

Common dimensions: projects in progress / Learning plan / The core to be solvedProblem / key decisions

fusion rules：
- Clearly completed or abandonedTarget → **Delete**
- newTarget → Append
- Already Target has made progressrenew → **Overwrite ** olddescribe

---

## Output specification

1. **Only the memory content itself** is output, without any opening words, explanations, summaries or separation instructions.
2. Four pieces chapters **all output**, if there is no content, write "None", the chapters cannot be omitted.
3. eachFormat：`- [DimensionsTags] content`，Tags 2~5 Character，Precise and concise
4. Has change mark（`※alreadyrenew` / `※To be confirmed`）The entries are placed at the front of each chapter****
5. Each memory controlIn **60 CharacterWithin **, information density takes priority, if it exceeds, split into two
6. The output language is consistent with the main language of [this wheelNewConversation]

---

## Output format

### 【Preferences] Interaction preferences
- [DimensionsTags] content
（If not available, write: None）

### 【Background】UsersBackground
- [DimensionsTags] content
（If not available, write: None）

### 【Agreement】Explicit agreement
- [DimensionsTags] content
（If not available, write: None）

### 【Target】currentTarget
- [DimensionsTags] content
（If not available, write: None）

'''


def _get_long_term_config(application, chat_user_id):
    """
    Retrieve long-term memoryConfiguration，Return dict or None（None Indicates that no retrieval is required and the memory has been cleared.）
    """
    if application.type == 'WORK_FLOW':
        node_list = application.work_flow.get('nodes', [])
        base_node = next((n for n in node_list if n.get('id') == 'base-node'), None)
        if base_node is None:
            return None
        node_data = base_node.get('properties', {}).get('node_data', {})
        if not node_data.get('long_term_enable', False):
            QuerySet(ApplicationLongTermMemory).filter(
                application_id=application.id, chat_user_id=chat_user_id
            ).delete()
            return None
        return {
            'trigger_type': node_data.get('long_term_trigger_type'),
            'trigger_setting': node_data.get('long_term_trigger_setting') or {'rounds': 10},
            'model_id': node_data.get('long_term_model_id'),
            'model_params': node_data.get('long_term_model_params_setting') or {},
        }
    else:
        if not application.long_term_enable:
            QuerySet(ApplicationLongTermMemory).filter(
                application_id=application.id, chat_user_id=chat_user_id
            ).delete()
            return None
        return {
            'trigger_type': application.long_term_trigger_type,
            'trigger_setting': application.long_term_trigger_setting or {'rounds': 10},
            'model_id': application.long_term_model_id,
            'model_params': application.long_term_model_params_setting or {},
        }


def _get_cron_interval(cron_expression: str):
    """
    By calculation cron The difference between two consecutive trigger times of an expression, estimated execution interval。
    Return timedelta，or None（When it cannot be inferred）。
    """
    from apscheduler.triggers.cron import CronTrigger

    try:
        trigger = CronTrigger.from_crontab(cron_expression.strip())
        now = timezone.now()
        t1 = trigger.get_next_fire_time(None, now)
        if t1 is None:
            return None
        t2 = trigger.get_next_fire_time(t1, t1)
        if t2 is None:
            return None
        return t2 - t1
    except Exception:
        return None


def _get_since_time_from_setting(setting: dict):
    """
    RootAccording toTiming Settings calculate the starting time of the Conversation that should be extracted this time。
    Return datetime（aware），or None indicates that it cannot be inferred (rollbackarrive rounds limit）。
    """
    now = timezone.now()
    schedule_type = setting.get("schedule_type")

    if schedule_type == "daily":
        return now - timedelta(days=1)
    if schedule_type == "weekly":
        return now - timedelta(weeks=1)
    if schedule_type == "monthly":
        return now - timedelta(days=30)
    if schedule_type == "interval":
        unit = (setting.get("interval_unit") or "").strip()
        try:
            value_i = int(setting.get("interval_value"))
            if value_i <= 0:
                return None
        except Exception:
            return None
        delta_map = {
            "seconds": timedelta(seconds=value_i),
            "minutes": timedelta(minutes=value_i),
            "hours": timedelta(hours=value_i),
            "days": timedelta(days=value_i),
        }
        delta = delta_map.get(unit)
        return now - delta if delta else None
    if schedule_type == "cron":
        cron_expression = setting.get("cron_expression") or ""
        delta = _get_cron_interval(cron_expression)
        return now - delta if delta else None
    return None


def _run_extract(workspace_id, application_id, chat_user_id, config, history_limit=None, since_time=None):
    """
    Perform a long-term memory retrieval。
    - since_time Nofor None Time: Extract the data generated after this time pointConversation。
    - Otherwiseaccording to history_limit stripNumberlimit。
    """
    if since_time is None and (history_limit is None or history_limit <= 0):
        return

    qs = (
        QuerySet(ChatRecord)
        .filter(
            chat__application_id=application_id,
            chat__chat_user_id=chat_user_id,
        )
        .order_by('-create_time')
        .only('problem_text', 'answer_text')
    )

    if since_time is not None:
        history_chat_record = list(qs.filter(create_time__gte=since_time))
    else:
        history_chat_record = list(qs[:history_limit])
    if len(history_chat_record) == 0:
        return

    chat_model = get_model_instance_by_model_workspace_id(
        config['model_id'], workspace_id, **config['model_params']
    )
    if not chat_model:
        return

    long_term_memory = QuerySet(ApplicationLongTermMemory).filter(
        application_id=application_id, chat_user_id=chat_user_id
    ).first()

    existing_memory = long_term_memory.memory if long_term_memory else ''

    # Reverse for chronological order (old → new）
    history_chat_record = list(reversed(history_chat_record))

    new_conversation = '\n'.join(
        line
        for record in history_chat_record
        for line in (f"Users：{record.problem_text}", f"AI：{record.answer_text}")
    )

    content = ''
    for chunk in chat_model.stream([
        HumanMessage(
            content=long_term_prompt
                    .replace('{{existing_memory}}', existing_memory)
                    .replace('{{new_conversation}}', new_conversation)
        )
    ]):
        content += chunk.content

    content = re.sub(r'<think>.*?<\/think>', '', content, flags=re.DOTALL).strip()

    if long_term_memory:
        long_term_memory.memory = content
        long_term_memory.save()
    else:
        ApplicationLongTermMemory(
            id=uuid.uuid7(),
            application_id=application_id,
            chat_user_id=chat_user_id,
            memory=content,
        ).save()


def _long_term_job_prefix(application_id) -> str:
    return f"long_term:application:{application_id}:"


def _parse_hhmm(value: str) -> tuple[int, int]:
    hour_str, minute_str = (value or "").split(":")
    hour = int(hour_str)
    minute = int(minute_str)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError("hour/minute out of range")
    return hour, minute


def _weekday_to_cron(d) -> str:
    mapping = {1: "mon", 2: "tue", 3: "wed", 4: "thu",
               5: "fri", 6: "sat", 7: "sun", 0: "sun"}
    di = int(d)
    if di not in mapping:
        raise ValueError("invalid weekday")
    return mapping[di]


def _remove_long_term_jobs(application_id) -> None:
    from common.job import scheduler

    prefix = _long_term_job_prefix(application_id)
    for job in scheduler.get_jobs():
        if getattr(job, "id", "").startswith(prefix):
            try:
                job.remove()
            except Exception as e:
                maxkb_logger.warning(
                    f"remove long_term job failed, job_id={job.id}, err={e}")


def _execute_scheduled_extract(workspace_id, application_id):
    """
    APScheduler Triggered callback: traverse the applicationall chat_user_id，Deliver extraction tasks separately。
    """
    application = Application.objects.filter(id=application_id).first()
    if not application:
        _remove_long_term_jobs(application_id)
        return

    chat_user_ids = list(
        QuerySet(Chat).filter(application_id=application_id)
        .exclude(chat_user_id__isnull=True)
        .values_list('chat_user_id', flat=True)
        .distinct()
    )
    for chat_user_id in chat_user_ids:
        config = _get_long_term_config(application, chat_user_id)
        if config is None:
            continue
        if config['trigger_type'] != 'SCHEDULED':
            continue
        setting = config['trigger_setting'] or {}
        since_time = _get_since_time_from_setting(setting)
        history_limit = None if since_time is not None else setting.get('rounds', 20)
        try:
            _run_extract(workspace_id, application_id, chat_user_id, config,
                         history_limit=history_limit, since_time=since_time)
        except Exception as e:
            maxkb_logger.warning(
                f"scheduled extract long_term_memory failed, "
                f"application_id={application_id}, chat_user_id={chat_user_id}, err={e}"
            )


def _deploy_long_term_daily(workspace_id, application_id, setting):
    from common.job import scheduler

    prefix = _long_term_job_prefix(application_id)
    times = setting.get("time") or []
    for t in times:
        try:
            hour, minute = _parse_hhmm(t)
        except Exception:
            maxkb_logger.warning(
                f"invalid time={t}, application_id={application_id}")
            continue
        job_id = f"{prefix}daily:{hour:02d}{minute:02d}"
        scheduler.add_job(
            _execute_scheduled_extract,
            trigger="cron",
            hour=str(hour),
            minute=str(minute),
            id=job_id,
            kwargs={"workspace_id": workspace_id,
                    "application_id": application_id},
            replace_existing=True,
            misfire_grace_time=60,
            max_instances=1,
        )


def _deploy_long_term_weekly(workspace_id, application_id, setting):
    from common.job import scheduler

    prefix = _long_term_job_prefix(application_id)
    times = setting.get("time") or []
    days = setting.get("days") or []
    if not times or not days:
        maxkb_logger.warning(
            f"empty weekly setting, application_id={application_id}")
        return
    for d in days:
        try:
            dow = _weekday_to_cron(d)
        except Exception:
            maxkb_logger.warning(
                f"invalid weekday={d}, application_id={application_id}")
            continue
        for t in times:
            try:
                hour, minute = _parse_hhmm(t)
            except Exception:
                maxkb_logger.warning(
                    f"invalid time={t}, application_id={application_id}")
                continue
            job_id = f"{prefix}weekly:{dow}:{hour:02d}{minute:02d}"
            scheduler.add_job(
                _execute_scheduled_extract,
                trigger="cron",
                day_of_week=dow,
                hour=str(hour),
                minute=str(minute),
                id=job_id,
                kwargs={"workspace_id": workspace_id,
                        "application_id": application_id},
                replace_existing=True,
                misfire_grace_time=60,
                max_instances=1,
            )


def _deploy_long_term_monthly(workspace_id, application_id, setting):
    from common.job import scheduler

    prefix = _long_term_job_prefix(application_id)
    times = setting.get("time") or []
    days = setting.get("days") or []
    if not times or not days:
        maxkb_logger.warning(
            f"empty monthly setting, application_id={application_id}")
        return
    for d in days:
        try:
            dom = int(d)
            if not (1 <= dom <= 31):
                raise ValueError("invalid day of month")
        except Exception:
            maxkb_logger.warning(
                f"invalid day={d}, application_id={application_id}")
            continue
        for t in times:
            try:
                hour, minute = _parse_hhmm(t)
            except Exception:
                maxkb_logger.warning(
                    f"invalid time={t}, application_id={application_id}")
                continue
            job_id = f"{prefix}monthly:{dom:02d}:{hour:02d}{minute:02d}"
            scheduler.add_job(
                _execute_scheduled_extract,
                trigger="cron",
                day=str(dom),
                hour=str(hour),
                minute=str(minute),
                id=job_id,
                kwargs={"workspace_id": workspace_id,
                        "application_id": application_id},
                replace_existing=True,
                misfire_grace_time=60,
                max_instances=1,
            )


def _deploy_long_term_cron(workspace_id, application_id, setting):
    from apscheduler.triggers.cron import CronTrigger

    from common.job import scheduler

    cron_expression = setting.get('cron_expression')
    if not cron_expression:
        maxkb_logger.warning(
            f"empty cron_expression, application_id={application_id}")
        return
    try:
        cron_trigger = CronTrigger.from_crontab(cron_expression.strip())
    except ValueError:
        maxkb_logger.warning(
            f"invalid cron_expression={cron_expression}, application_id={application_id}")
        return

    job_id = f"{_long_term_job_prefix(application_id)}cron:{cron_expression.strip()}"
    scheduler.add_job(
        _execute_scheduled_extract,
        trigger=cron_trigger,
        id=job_id,
        kwargs={"workspace_id": workspace_id,
                "application_id": application_id},
        replace_existing=True,
        misfire_grace_time=60,
        max_instances=1,
    )


def _deploy_long_term_interval(workspace_id, application_id, setting):
    from common.job import scheduler

    unit = (setting.get("interval_unit") or "").strip()
    value = setting.get("interval_value")
    try:
        value_i = int(value)
        if value_i <= 0:
            raise ValueError("interval_value must be positive")
    except Exception:
        maxkb_logger.warning(
            f"invalid interval_value={value}, application_id={application_id}")
        return
    if unit not in {"seconds", "minutes", "hours", "days"}:
        maxkb_logger.warning(
            f"invalid interval_unit={unit}, application_id={application_id}")
        return

    job_id = f"{_long_term_job_prefix(application_id)}interval:{unit}:{value_i}"
    scheduler.add_job(
        _execute_scheduled_extract,
        trigger="interval",
        id=job_id,
        kwargs={"workspace_id": workspace_id,
                "application_id": application_id},
        replace_existing=True,
        misfire_grace_time=60,
        max_instances=1,
        **{unit: value_i},
    )


@celery_app.task(name="celery:extract_long_term_memory")
def extract_long_term_memory(workspace_id, application_id, chat_user_id):
    application = Application.objects.filter(id=application_id).first()
    if not application:
        return

    config = _get_long_term_config(application, chat_user_id)
    if config is None:
        return

    trigger_type = config['trigger_type']
    trigger_setting = config['trigger_setting']

    if trigger_type != 'ROUND':
        # according toAccording to time, scheduled tasks willProcessing
        return

    rounds = trigger_setting.get('rounds', 10)
    if rounds <= 0:
        return

    current_rounds = QuerySet(ChatRecord).filter(
        chat__application_id=application_id,
        chat__chat_user_id=chat_user_id,
    ).count()
    maxkb_logger.info(f'extract_long_term_memory: current_rounds={current_rounds}, rounds={rounds}')
    if current_rounds % rounds != 0:
        return

    _run_extract(workspace_id, application_id, chat_user_id, config, history_limit=rounds)


@celery_app.task(name="celery:schedule_extract_long_term_memory")
def schedule_extract_long_term_memory(workspace_id, application_id, enabled, trigger_type, trigger_setting):
    # Clean up the old scheduling tasks first
    _remove_long_term_jobs(application_id)

    application = Application.objects.filter(id=application_id).first()
    if not application:
        return

    # applicationTurn off long-term memory
    if not enabled:
        QuerySet(ApplicationLongTermMemory).filter(application_id=application_id).delete()
        return
    # If Yes is no longer triggered regularly, it will only be cleaned and not deployed.
    if trigger_type != 'SCHEDULED':
        return

    setting = trigger_setting or {}
    schedule_type = setting.get("schedule_type")

    deployers = {
        "daily": _deploy_long_term_daily,
        "weekly": _deploy_long_term_weekly,
        "monthly": _deploy_long_term_monthly,
        "interval": _deploy_long_term_interval,
        "cron": _deploy_long_term_cron,
    }
    fn = deployers.get(schedule_type)
    if not fn:
        maxkb_logger.warning(f"unsupported long_term schedule_type={schedule_type}, application_id={application_id}")
        return

    fn(workspace_id, application_id, setting)
