# app/tasks.py

from celery import Celery
from .config import Config
from .utils import post_to_platform
import logging

logger = logging.getLogger(__name__)

celery = Celery(
    __name__,
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

@celery.task(bind=True)
def post_content_task(self, platform: str, content: str, client_id: str):
    """Celery task to post content to a platform."""
    try:
        result = post_to_platform(platform, content)
        logger.info(f"Posted to {platform} for client {client_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to post to {platform}: {str(e)}")
        self.retry(exc=e, countdown=60, max_retries=3)
        return {"error": str(e), "platform": platform}