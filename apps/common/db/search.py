# coding=utf-8
"""
    @project: maxkb
    @Author：Tiger
    @file： search.py
    @date：2023/10/7 18:20
    @desc:
"""
import hashlib
from typing import Dict, Any

from django.db import DEFAULT_DB_ALIAS, models, connections
from django.db.models import QuerySet

from common.db.compiler import AppSQLCompiler
from common.db.sql_execute import select_one, select_list, update_execute
from common.result import Page

# Add modelcache
_model_cache = {}


def get_dynamics_model(attr: dict, table_name='dynamics'):
    """
    getpieces dynamicdjangoModel
    :param attr:       ModelFields
    :param table_name: Table name
    :return: django Model
    """
    # createCache key, based on propertyand table name
    cache_key = hashlib.md5(f"{table_name}_{str(sorted(attr.items()))}".encode()).hexdigest()
    # print(f'cache_key: {cache_key}')

    # likeIfModelAlready exists，Directly return cachedModel
    if cache_key in _model_cache:
        return _model_cache[cache_key]

    attributes = {
        "__module__": "knowledge.models",
        "Meta": type("Meta", (), {'db_table': table_name}),
        **attr
    }

    # useUnique class names avoid conflicts
    class_name = f'Dynamics_{cache_key[:8]}'
    model_class = type(class_name, (models.Model,), attributes)

    # cacheModel
    _model_cache[cache_key] = model_class

    return model_class


def generate_sql_by_query_dict(queryset_dict: Dict[str, QuerySet], select_string: str,
                               field_replace_dict: None | Dict[str, Dict[str, str]] = None, with_table_name=False):
    """
    generate Querysql
    :param with_table_name:
    :param queryset_dict: Morecondition Querycondition
    :param select_string: Querysql
    :param field_replace_dict:  Need to be replacedQueryFields,Generally does not need to be passed in if there is a special need to pass in
    :return: sql:Requires Querysql params: sql parameter
    """

    params_dict: Dict[int, Any] = {}
    result_params = []
    for key in queryset_dict.keys():
        value = queryset_dict.get(key)
        sql, params = compiler_queryset(value, None if field_replace_dict is None else field_replace_dict.get(key),
                                        with_table_name)
        params_dict = {**params_dict, select_string.index("${" + key + "}"): params}
        select_string = select_string.replace("${" + key + "}", sql)

    for key in sorted(list(params_dict.keys())):
        result_params = [*result_params, *params_dict.get(key)]
    return select_string, result_params


def generate_sql_by_query(queryset: QuerySet, select_string: str,
                          field_replace_dict: None | Dict[str, str] = None, with_table_name=False):
    """
    generate Querysql
    :param queryset:            Querycondition
    :param select_string:       originalsql
    :param field_replace_dict:  Need to be replacedQueryFields,Generally does not need to be passed in if there is a special need to pass in
    :return:  sql:Requires Querysql params: sql parameter
    """
    sql, params = compiler_queryset(queryset, field_replace_dict, with_table_name)
    return select_string + " " + sql, params


def compiler_queryset(queryset: QuerySet, field_replace_dict: None | Dict[str, str] = None, with_table_name=False):
    """
    parse querysetQueryobject
    :param with_table_name:
    :param queryset:            Queryobject
    :param field_replace_dict:  Need to be replacedQueryFields,Generally does not need to be passed in if there is a special need to pass in
    :return: sql:Requires Querysql params: sql parameter
    """
    q = queryset.query
    compiler = q.get_compiler(DEFAULT_DB_ALIAS)
    if field_replace_dict is None:
        field_replace_dict = get_field_replace_dict(queryset)
    app_sql_compiler = AppSQLCompiler(q, using=DEFAULT_DB_ALIAS, connection=compiler.connection,
                                      field_replace_dict=field_replace_dict)
    sql, params = app_sql_compiler.get_query_str(with_table_name=with_table_name)
    return sql, params


def native_search(queryset: QuerySet | Dict[str, QuerySet], select_string: str,
                  field_replace_dict: None | Dict[str, Dict[str, str]] | Dict[str, str] = None,
                  with_search_one=False, with_table_name=False):
    """
    complexQuery
    :param with_table_name:     generatesqlYesNoInclude table name
    :param queryset:            QueryconditionConstructor
    :param select_string:       QueryPrefix Excludes where limit etc.information
    :param field_replace_dict:  Need to be replacedFields
    :param with_search_one:     Query
    :return: Queryresult
    """
    if isinstance(queryset, Dict):
        exec_sql, exec_params = generate_sql_by_query_dict(queryset, select_string, field_replace_dict, with_table_name)
    else:
        exec_sql, exec_params = generate_sql_by_query(queryset, select_string, field_replace_dict, with_table_name)
    if with_search_one:
        return select_one(exec_sql, exec_params)
    else:
        return select_list(exec_sql, exec_params)


def native_update(queryset: QuerySet | Dict[str, QuerySet], select_string: str,
                  field_replace_dict: None | Dict[str, Dict[str, str]] | Dict[str, str] = None,
                  with_table_name=False):
    """
    complexQuery
    :param with_table_name:     generatesqlYesNoInclude table name
    :param queryset:            QueryconditionConstructor
    :param select_string:       QueryPrefix Excludes where limit etc.information
    :param field_replace_dict:  Need to be replacedFields
    :return: Queryresult
    """
    if isinstance(queryset, Dict):
        exec_sql, exec_params = generate_sql_by_query_dict(queryset, select_string, field_replace_dict, with_table_name)
    else:
        exec_sql, exec_params = generate_sql_by_query(queryset, select_string, field_replace_dict, with_table_name)
    return update_execute(exec_sql, exec_params)


def page_search(current_page: int, page_size: int, queryset: QuerySet, post_records_handler):
    """
    PagingQuery
    :param current_page:         Current page
    :param page_size:            Per page size
    :param queryset:             Querycondition
    :param post_records_handler: NumberAccording toProcessingdevice
    :return:  Paging results
    """
    total = QuerySet(query=queryset.query.clone(), model=queryset.model).count()
    result = queryset.all()[((current_page - 1) * page_size):(current_page * page_size)]
    return Page(total, list(map(post_records_handler, result)), current_page, page_size)


def native_page_search(current_page: int, page_size: int, queryset: QuerySet | Dict[str, QuerySet], select_string: str,
                       field_replace_dict=None,
                       post_records_handler=lambda r: r,
                       with_table_name=False):
    """
    Complex pagingQuery
    :param with_table_name:
    :param current_page:          Current page
    :param page_size:             Per page size
    :param queryset:              Querycondition
    :param select_string:         Query
    :param field_replace_dict:    Special Fields replacement
    :param post_records_handler:  NumberAccording torowProcessingdevice
    :return: Paging results
    """
    if isinstance(queryset, Dict):
        exec_sql, exec_params = generate_sql_by_query_dict(queryset, select_string, field_replace_dict, with_table_name)
    else:
        exec_sql, exec_params = generate_sql_by_query(queryset, select_string, field_replace_dict, with_table_name)
    total_sql = "SELECT \"count\"(*) FROM (%s) temp" % exec_sql
    total = select_one(total_sql, exec_params)
    limit_sql = connections[DEFAULT_DB_ALIAS].ops.limit_offset_sql(
        ((current_page - 1) * page_size), (current_page * page_size)
    )
    page_sql = exec_sql + " " + limit_sql
    result = select_list(page_sql, exec_params)
    return Page(total.get("count"), list(map(post_records_handler, result)), current_page, page_size)


def native_page_handler(page_size: int,
                        queryset: QuerySet | Dict[str, QuerySet],
                        select_string: str,
                        field_replace_dict=None,
                        with_table_name=False,
                        primary_key=None,
                        get_primary_value=None,
                        primary_queryset: str = None,
                        ):
    if isinstance(queryset, Dict):
        exec_sql, exec_params = generate_sql_by_query_dict({**queryset,
            primary_queryset: queryset[primary_queryset].order_by(
                primary_key)}, select_string, field_replace_dict, with_table_name)
    else:
        exec_sql, exec_params = generate_sql_by_query(queryset.order_by(
            primary_key), select_string, field_replace_dict, with_table_name)
    total_sql = "SELECT \"count\"(*) FROM (%s) temp" % exec_sql
    total = select_one(total_sql, exec_params)
    processed_count = 0
    last_id = None
    while processed_count < total.get("count"):
        if last_id is not None:
            if isinstance(queryset, Dict):
                exec_sql, exec_params = generate_sql_by_query_dict({**queryset,
                    primary_queryset: queryset[primary_queryset].filter(
                        **{f"{primary_key}__gt": last_id}).order_by(
                        primary_key)},
                    select_string, field_replace_dict,
                    with_table_name)
            else:
                exec_sql, exec_params = generate_sql_by_query(
                    queryset.filter(**{f"{primary_key}__gt": last_id}).order_by(
                        primary_key),
                    select_string, field_replace_dict,
                    with_table_name)
        limit_sql = connections[DEFAULT_DB_ALIAS].ops.limit_offset_sql(
            0, page_size
        )
        page_sql = exec_sql + " " + limit_sql
        result = select_list(page_sql, exec_params)
        yield result
        processed_count += page_size
        last_id = get_primary_value(result[-1])


def get_field_replace_dict(queryset: QuerySet):
    """
    getNeed to be replacedFields default “xxx.xxx”needs to be replaced by “xxx”."xxx"
    :param queryset: Queryobject
    :return: Character code that needs to be replaced
    """
    result = {}
    for field in queryset.model._meta.local_fields:
        if field.attname.__contains__("."):
            replace_field = to_replace_field(field.attname)
            result.__setitem__('"' + field.attname + '"', replace_field)
    return result


def to_replace_field(field: str):
    """
    Willfield Convert to Need to be replacedfield  “xxx.xxx”needs to be replaced by “xxx”."xxx" Replace only fieldInclude.ofFields
    :param field: django fieldFields
    :return: ReplacementFields
    """
    split_field = field.split(".")
    return ".".join(list(map(lambda sf: '"' + sf + '"', split_field)))
