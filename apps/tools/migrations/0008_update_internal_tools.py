import json
import re
from django.db import migrations


# English init_field_list for Google Search
GOOGLE_SEARCH_INIT_FIELDS = [
    {"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": True, "show-word-limit": True}, "field": "apikey", "label": "API Key", "required": True, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "API Key is required", "required": True}, {"max": 200, "min": 1, "message": "API Key length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "cx", "label": "cx", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "cx is required", "required": True}, {"max": 200, "min": 1, "message": "cx length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
]

# English init_field_list for LangSearch
LANGSEARCH_INIT_FIELDS = [
    {"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": True, "show-word-limit": True}, "field": "apikey", "label": "API Key", "required": True, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "API Key is required", "required": True}, {"max": 200, "min": 1, "message": "API Key length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
]

# English init_field_list for MySQL Query
MYSQL_INIT_FIELDS = [
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "host", "label": "host", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "host is required", "required": True}, {"max": 200, "min": 1, "message": "host length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
    {"attrs": {"maxlength": 20, "minlength": 1, "show-word-limit": True}, "field": "port", "label": "port", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "port is required", "required": True}, {"max": 20, "min": 1, "message": "port length must be between 1 and 20 characters", "trigger": "blur"}]}, "default_value": "3306", "show_default_value": False},
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "user", "label": "user", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "user is required", "required": True}, {"max": 200, "min": 1, "message": "user length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "root", "show_default_value": False},
    {"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": True, "show-word-limit": True}, "field": "password", "label": "password", "required": True, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "password is required", "required": True}, {"max": 200, "min": 1, "message": "password length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "database", "label": "database", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "database is required", "required": True}, {"max": 200, "min": 1, "message": "database length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
]

# English init_field_list for PostgreSQL Query
PGSQL_INIT_FIELDS = [
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "host", "label": "host", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "host is required", "required": True}, {"max": 200, "min": 1, "message": "host length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
    {"attrs": {"maxlength": 20, "minlength": 1, "show-word-limit": True}, "field": "port", "label": "port", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "port is required", "required": True}, {"max": 20, "min": 1, "message": "port length must be between 1 and 20 characters", "trigger": "blur"}]}, "default_value": "5432", "show_default_value": False},
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "user", "label": "user", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "user is required", "required": True}, {"max": 200, "min": 1, "message": "user length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "root", "show_default_value": False},
    {"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": True, "show-word-limit": True}, "field": "password", "label": "password", "required": True, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "password is required", "required": True}, {"max": 200, "min": 1, "message": "password length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
    {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": True}, "field": "database", "label": "database", "required": True, "input_type": "TextInput", "props_info": {"rules": [{"message": "database is required", "required": True}, {"max": 200, "min": 1, "message": "database length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": False},
]


def update_internal_tools(apps, schema_editor):
    Tool = apps.get_model('tools', 'Tool')

    # Delete Bocha Search (Chinese-only service)
    Tool.objects.filter(id='c75cb48e-fd77-11ef-84d2-5618c4394482').delete()

    # Update Google Search
    Tool.objects.filter(id='e89ad2ae-f3f2-11ef-ad09-0242ac110002').update(
        name='Google Search',
        desc='Google Web Search',
        init_field_list=GOOGLE_SEARCH_INIT_FIELDS,
    )

    # Update LangSearch
    Tool.objects.filter(id='5e912f00-f34c-11ef-8a9c-5618c4394482').update(
        name='LangSearch',
        desc='A Web Search tool supporting natural language search',
        init_field_list=LANGSEARCH_INIT_FIELDS,
    )

    # Update MySQL Query
    Tool.objects.filter(id='22c21b76-0308-11f0-9694-5618c4394482').update(
        name='MySQL Query',
        desc='A tool to connect to MySQL database to execute SQL queries',
        init_field_list=MYSQL_INIT_FIELDS,
    )

    # Update PostgreSQL Query
    Tool.objects.filter(id='bd1e8b88-0302-11f0-87bb-5618c4394482').update(
        name='PostgreSQL Query',
        desc='A tool to connect to PostgreSQL database to execute SQL queries',
        init_field_list=PGSQL_INIT_FIELDS,
    )

    # Fix any remaining tools that may have Chinese validation messages
    # (e.g., tools imported from the store by the user)
    all_tools = Tool.objects.exclude(init_field_list=[]).exclude(init_field_list__isnull=True)
    for tool in all_tools:
        original = json.dumps(tool.init_field_list, ensure_ascii=False)
        modified = original
        modified = re.sub(r'([\w\s]+?)\s*为必填属性', r'\1 is required', modified)
        modified = re.sub(r'([\w\s]+?)长度在\s*(\d+)\s*到\s*(\d+)\s*个字符',
                          r'\1 length must be between \2 and \3 characters', modified)
        if modified != original:
            tool.init_field_list = json.loads(modified)
            tool.save(update_fields=['init_field_list'])


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0007_alter_tool_tool_type_toolworkflow_and_more'),
    ]

    operations = [
        migrations.RunPython(update_internal_tools),
    ]
