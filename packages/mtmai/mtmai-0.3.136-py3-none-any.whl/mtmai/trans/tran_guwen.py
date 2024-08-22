"""
# 模型训练, 让llama3.18b模型具备将现代汉语转换为古文风格的文章
- 资料库：https://github.com/NiuTrans/Classical-Modern
- 参考别人的训练数据集： https://huggingface.co/datasets/AISPIN/shiji-70liezhuan
- 别人训练好的模型 参考： https://huggingface.co/AISPIN/Llama-3.1-8B-bnb-4bit-wenyanwen
- 参考视频： https://www.youtube.com/watch?v=Tq6qPw8EUVg

"""

import logging
from multiprocessing import Process

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger()


def start_tran_guwen():
    logger.info("start_tran_guwen")


@router.get("/tran_clickbait")
def tran_clickbait():
    """古文训练"""
    proc = Process(target=start_tran_guwen)
    proc.start()
    # proc.join()
    return ""
