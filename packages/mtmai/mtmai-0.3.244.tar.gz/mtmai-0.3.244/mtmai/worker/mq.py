import logging

import psycopg
from fastapi import APIRouter

from mtmai.core.config import settings

router = APIRouter()
logger = logging.getLogger()
# 文档: https://github.com/tembo-io/pgmq/blob/293f6e93f3799ee17016b07f4834f7bd01f7387a/README.md


def execsql(sql: str):
    logger.info("执行sql: %s", sql)
    try:
        with psycopg.connect(settings.DATABASE_URL) as connection:  # noqa: SIM117
            with connection.cursor() as cursor:
                cursor.execute(sql)
                datasets = cursor.fetchall()
                return datasets

    except psycopg.Error:
        return None


def setup_pgmq():
    """安装必要的插件"""
    return execsql("CREATE EXTENSION IF NOT EXISTS pgmq")


def create_queue(queue_name: str):
    return execsql(f"SELECT pgmq.create('{queue_name}')")


def send_msg(queue_name: str, payload: str):
    return execsql(f"SELECT pgmq.send('{queue_name}', '{payload}'")


def pop_msg(queue_name: str):
    """Read a message and immediately delete it from the queue. Returns `None` if the queue is empty."""
    return execsql(f"SELECT pgmq.pop('{queue_name}')")


def delete_msg(msg_id: int):
    """删除消息, 相当于 常规 消息队列的 消息确认"""
    return execsql(f"SELECT pgmq.delete('my_queue', {msg_id});)")


def archive_message(queue_name: str, count: int):
    """Archiving a message removes it from the queue, and inserts it to the archive table."""
    return execsql(f"SELECT pgmq.archive('{queue_name}', {count});")


def read_msg(
    queue_name: str,
    invisible: int = 10,
    limit: int = 1,
):
    result = execsql(f"SELECT pgmq.read('{queue_name}', {invisible}, {limit})")
    return result
