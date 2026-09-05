"""Celery application initialization."""

from celery import Celery

from app.core.config import get_settings


settings = get_settings()
celery = Celery("meetai", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

