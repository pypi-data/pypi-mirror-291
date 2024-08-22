import logging
import threading

from fastapi import APIRouter
from opentelemetry import trace

from mtmai.worker import worker

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/start_worker")
async def start_worker():
    threading.Thread(target=worker.run_worker).start()
