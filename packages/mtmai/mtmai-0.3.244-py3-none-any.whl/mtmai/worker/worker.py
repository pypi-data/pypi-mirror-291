import json
import logging
import time

from mtmai.worker import mq

logger = logging.getLogger()

queue_name = "ping"


def init_queue():
    mq.create_queue(queue_name)


def ping():
    mq.send_msg(queue_name, json.dumps({"ping": "value-ping"}))


def consum_messages():
    while True:
        new_messages = mq.read_msg(queue_name, 10, 1)
        if new_messages:
            try:
                # logger.info("读取到消息: %s", new_message)
                for msg in new_messages:
                    message_tuple = (msg,)
                    consum_item(message_tuple)
                    mq.delete_msg(queue_name, message_tuple[1])
            except Exception as e:  # noqa: BLE001
                # TODO: 放入死信队列
                logger.info("消息消费失败 %s", e)
        else:
            logger.info("暂无新消息, 稍后再试...")
        time.sleep(2)


def consum_item(item_str: str):
    logger.info("消费一个消息 %s", item_str)


def run_worker():
    logger.info("🚀 worker start ...")
    init_queue()
    ping()
    consum_messages()
