# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Tiger
    @file： sql_execute.py
    @date：2023/9/25 20:05
    @desc:
"""
from typing import List

from django.db import connection


def sql_execute(sql: str, params):
    """
    Execute onesql
    :param sql:     Need to executesql
    :param params:  sqlparameter
    :return:        Execution result
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = list(map(lambda d: d.name, cursor.description))
        res = cursor.fetchall()
        result = list(map(lambda row: dict(list(zip(columns, row))), res))
        cursor.close()
        return result


def update_execute(sql: str, params):
    """
      Execute onesql
      :param sql:     Need to executesql
      :param params:  sqlparameter
      :return:        Execution result
      """
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows


def select_list(sql: str, params: List):
    """
    implementsql QueryListNumberAccording to
    :param sql:     Need to executesql
    :param params:  sqlofparameter
    :return: Queryresult
    """
    result_list = sql_execute(sql, params)
    if result_list is None:
        return []
    return result_list


def select_one(sql: str, params: List):
    """
    implementsql Queryone pieceNumberAccording to
    :param sql:     Need to executesql
    :param params:  parameter
    :return: Queryresult
    """
    result_list = sql_execute(sql, params)
    if result_list is None or len(result_list) == 0:
        return None
    return result_list[0]
