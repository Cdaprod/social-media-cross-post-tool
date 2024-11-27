# app/threads.py

import requests
import logging
from typing import Dict, Any
from .config import Config
from .utils import requests_retry_session

logger = logging.getLogger(__name__)

def get_thread_replies(thread_id: str) -> Dict[str, Any]:
    """Fetch replies to a specific thread."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.THREADS_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        url = f"{Config.THREADS_API_URL}/{thread_id}/replies"
        session = requests_retry_session()
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching replies for thread {thread_id}: {str(e)}")
        raise

def reply_to_thread(thread_id: str, message: str) -> Dict[str, Any]:
    """Post a reply to a specific thread."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.THREADS_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "content": message
        }
        url = f"{Config.THREADS_API_URL}/{thread_id}/replies"
        session = requests_retry_session()
        response = session.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting reply to thread {thread_id}: {str(e)}")
        raise

def delete_thread_reply(thread_id: str, reply_id: str) -> Dict[str, Any]:
    """Delete a reply from a thread."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.THREADS_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        url = f"{Config.THREADS_API_URL}/{thread_id}/replies/{reply_id}"
        session = requests_retry_session()
        response = session.delete(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting reply {reply_id} from thread {thread_id}: {str(e)}")
        raise

def get_thread_insights(thread_id: str) -> Dict[str, Any]:
    """Fetch insights for a specific thread."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.THREADS_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        url = f"{Config.THREADS_API_URL}/{thread_id}/insights"
        session = requests_retry_session()
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching insights for thread {thread_id}: {str(e)}")
        raise

def publish_thread(content: str) -> Dict[str, Any]:
    """Publish new content to Threads."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.THREADS_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "content": content
        }
        url = Config.THREADS_API_URL
        session = requests_retry_session()
        response = session.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error publishing new thread: {str(e)}")
        raise