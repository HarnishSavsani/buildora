INSERT INTO tool (create_time, update_time, id, name, label, "desc", code, input_field_list, init_field_list, icon, is_active, scope, tool_type, template_id, workspace_id, init_params, user_id, folder_id) VALUES ('2025-02-26 03:36:48.187286 +00:00', '2025-03-11 07:23:46.123972 +00:00', 'e89ad2ae-f3f2-11ef-ad09-0242ac110002', 'Google Search','web_search', 'Google Web Search', e'def google_search(query, apikey, cx):
    import requests
    import json
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": apikey,
        "cx": cx,
        "num": 10,  # Return up to 10 items at a time
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.status_code}, Error message: {response.text}")
        return (response.text)', '[{"name": "query", "type": "string", "source": "reference", "is_required": true}]', '[{"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": true, "show-word-limit": true}, "field": "apikey", "label": "API Key", "required": true, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "API Key is required", "required": true}, {"max": 200, "min": 1, "message": "API Key length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}, {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "cx", "label": "cx", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "cx is required", "required": true}, {"max": 200, "min": 1, "message": "cx length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}]', './tool/google_search/icon.png', true, 'INTERNAL', 'INTERNAL', null, 'None', '', 'f0dd8f71-e4ee-11ee-8c84-a8a1595801ab', 'default');
INSERT INTO tool (create_time, update_time, id, name, label, "desc", code, input_field_list, init_field_list, icon, is_active, scope, tool_type, template_id, workspace_id, init_params, user_id, folder_id) VALUES ('2025-02-25 07:44:40.141515 +00:00', '2025-03-11 06:33:53.248495 +00:00', '5e912f00-f34c-11ef-8a9c-5618c4394482', 'LangSearch','web_search', e'A Web Search tool supporting natural language search
', e'
def langsearch(query, apikey):
    import json
    import requests

    url = "https://api.langsearch.com/v1/web-search"
    payload = json.dumps({
        "query": query,
        "summary": True,
        "freshness": "noLimit",
        "livecrawl": True,
        "count": 20
    })
    headers = {
        "Authorization": apikey,
        "Content-Type": "application/json"
    }
    # Get key from official website https://langsearch.com/
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.status_code}, Error message: {response.text}")
        return (response.text)', '[{"name": "query", "type": "string", "source": "reference", "is_required": true}]', '[{"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": true, "show-word-limit": true}, "field": "apikey", "label": "API Key", "required": true, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "API Key is required", "required": true}, {"max": 200, "min": 1, "message": "API Key length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}]', './tool/langsearch/icon.png', true, 'INTERNAL', 'INTERNAL', null, 'None', '', 'f0dd8f71-e4ee-11ee-8c84-a8a1595801ab', 'default');
INSERT INTO tool (create_time, update_time, id, name, label, "desc", code, input_field_list, init_field_list, icon, is_active, scope, tool_type, template_id, workspace_id, init_params, user_id, folder_id) VALUES ('2025-03-17 08:16:32.626245 +00:00', '2025-03-17 08:16:32.626308 +00:00', '22c21b76-0308-11f0-9694-5618c4394482', 'MySQL Query','database_search', 'A tool to connect to MySQL database to execute SQL queries', e'
def query_mysql(host,port, user, password, database, sql):
    import pymysql
    import json
    from pymysql.cursors import DictCursor
    from datetime import datetime, date

    def default_serializer(obj):
        from decimal import Decimal
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()  # Convert datetime/date to ISO format string
        elif isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        raise TypeError(f"Type {type(obj)} not serializable")

    try:
        # Create connection
        db = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor  # Use dictionary cursor
        )

        # Create a cursor object
        cursor = db.cursor()

        # Execute SQL query
        cursor.execute(sql)

        # Get all data using fetchall()
        data = cursor.fetchall()

        # Process bytes type data
        for row in data:
            for key, value in row.items():
                if isinstance(value, bytes):
                    row[key] = value.decode("utf-8")  # Convert to string

        # Serialize data to JSON
        json_data = json.dumps(data, default=default_serializer, ensure_ascii=False)
        return json_data

        # Close database connection
        db.close()

    except Exception as e:
        print(f"Error while connecting to MySQL: {e}")
        raise e', '[{"name": "sql", "type": "string", "source": "reference", "is_required": true}]', '[{"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "host", "label": "host", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "host is required", "required": true}, {"max": 200, "min": 1, "message": "host length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}, {"attrs": {"maxlength": 20, "minlength": 1, "show-word-limit": true}, "field": "port", "label": "port", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "port is required", "required": true}, {"max": 20, "min": 1, "message": "port length must be between 1 and 20 characters", "trigger": "blur"}]}, "default_value": "3306", "show_default_value": false}, {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "user", "label": "user", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "user is required", "required": true}, {"max": 200, "min": 1, "message": "user length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "root", "show_default_value": false}, {"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": true, "show-word-limit": true}, "field": "password", "label": "password", "required": true, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "password is required", "required": true}, {"max": 200, "min": 1, "message": "password length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}, {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "database", "label": "database", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "database is required", "required": true}, {"max": 200, "min": 1, "message": "database length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}]', './tool/mysql/icon.png', true, 'INTERNAL', 'INTERNAL', null, 'None', null, 'f0dd8f71-e4ee-11ee-8c84-a8a1595801ab', 'default');
INSERT INTO tool (create_time, update_time, id, name, label, "desc", code, input_field_list, init_field_list, icon, is_active, scope, tool_type, template_id, workspace_id, init_params, user_id, folder_id) VALUES ('2025-03-17 07:37:54.620836 +00:00', '2025-03-17 07:37:54.620887 +00:00', 'bd1e8b88-0302-11f0-87bb-5618c4394482', 'PostgreSQL Query','database_search', 'A tool to connect to PostgreSQL database to execute SQL queries', e'
def queryPgSQL(database, user, password, host, port, query):
    import psycopg2
    import json
    from datetime import datetime

    # Custom JSON serialization function
    def default_serializer(obj):
        from decimal import Decimal
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        elif isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        raise TypeError(f"Type {type(obj)} not serializable")

    # Database connection information
    conn_params = {
        "dbname": database,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }
    try:
        # Establish connection
        conn = psycopg2.connect(**conn_params)
        print("Connection successful!")
        # Create cursor object
        cursor = conn.cursor()
        # Execute query statement
        cursor.execute(query)
        # Get query results
        rows = cursor.fetchall()
        # Process result data
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        # Convert to JSON format
        json_result = json.dumps(result, default=default_serializer, ensure_ascii=False)
        return json_result
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()', '[{"name": "query", "type": "string", "source": "reference", "is_required": true}]', '[{"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "host", "label": "host", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "host is required", "required": true}, {"max": 200, "min": 1, "message": "host length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}, {"attrs": {"maxlength": 20, "minlength": 1, "show-word-limit": true}, "field": "port", "label": "port", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "port is required", "required": true}, {"max": 20, "min": 1, "message": "port length must be between 1 and 20 characters", "trigger": "blur"}]}, "default_value": "5432", "show_default_value": false}, {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "user", "label": "user", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "user is required", "required": true}, {"max": 200, "min": 1, "message": "user length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "root", "show_default_value": false}, {"attrs": {"type": "password", "maxlength": 200, "minlength": 1, "show-password": true, "show-word-limit": true}, "field": "password", "label": "password", "required": true, "input_type": "PasswordInput", "props_info": {"rules": [{"message": "password is required", "required": true}, {"max": 200, "min": 1, "message": "password length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}, {"attrs": {"maxlength": 200, "minlength": 1, "show-word-limit": true}, "field": "database", "label": "database", "required": true, "input_type": "TextInput", "props_info": {"rules": [{"message": "database is required", "required": true}, {"max": 200, "min": 1, "message": "database length must be between 1 and 200 characters", "trigger": "blur"}]}, "default_value": "x", "show_default_value": false}]', './tool/postgresql/icon.png', true, 'INTERNAL', 'INTERNAL', null, 'None', null, 'f0dd8f71-e4ee-11ee-8c84-a8a1595801ab', 'default');
