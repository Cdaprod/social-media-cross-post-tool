# app/utils.py (final)

import re
from typing import Tuple, Optional
from langdetect import detect, LangDetectException
import logging
from .config import Config
import anthropic
from functools import lru_cache
import requests
from .utils import requests_retry_session

logger = logging.getLogger(__name__)

# Initialize Anthropic client
anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

PLATFORM_CONSTRAINTS = {
    "Twitter": {
        "max_length": 280,
        "prompt": """You are a social media expert. Optimize this content for Twitter (X):
- Keep it under 280 characters
- Make it engaging and shareable
- Include relevant hashtags if appropriate
- Maintain the core message

Content: {content}
"""
    },
    "Threads": {
        "max_length": 500,
        "prompt": """You are a social media expert. Optimize this content for Instagram Threads:
- Keep it under 500 characters
- Make it conversational and authentic
- Focus on storytelling
- Maintain the core message

Content: {content}
"""
    },
    "LinkedIn": {
        "max_length": 1300,
        "prompt": """You are a social media expert. Optimize this content for LinkedIn:
- Keep it under 1300 characters
- Make it professional and insightful
- Encourage engagement through questions or calls to action
- Maintain the core message

Content: {content}
"""
    }
    # Add more platforms as needed
}

def validate_content(content: str) -> Tuple[bool, Optional[str]]:
    """Validates the content for basic and advanced requirements."""
    if not content:
        return False, "Content cannot be empty"
    if len(content) > 1000:
        return False, "Content exceeds maximum length of 1000 characters"
    if not re.match(r'^[\w\s\d.,!?@#$%^&*()-=+;:\'"\[\]{}|\\/]+$', content):
        return False, "Content contains invalid characters"
    
    # Language detection
    try:
        language = detect(content)
        if language not in ['en', 'es', 'fr', 'de']:  # Supported languages
            return False, f"Unsupported language: {language}"
    except LangDetectException:
        return False, "Unable to detect language"
    
    # Prohibited content
    prohibited_words = ['badword1', 'badword2']  # Example list
    if any(word in content.lower() for word in prohibited_words):
        return False, "Content contains prohibited language"
    
    return True, None

@lru_cache(maxsize=1024)
def optimize_content(content: str, platform: str) -> str:
    """Optimizes content for the specified platform using Anthropic's Claude."""
    try:
        platform_config = PLATFORM_CONSTRAINTS[platform]
        prompt = platform_config["prompt"].format(content=content)
        
        response = anthropic_client.completions.create(
            model="claude-3.5-sonnet",
            max_tokens_to_sample=150,
            prompt=prompt,
            temperature=0.7
        )
        
        optimized_content = response.completion.strip()
        
        # Ensure content meets platform constraints
        if len(optimized_content) > platform_config["max_length"]:
            optimized_content = optimized_content[:platform_config["max_length"]]
        
        return optimized_content

    except Exception as e:
        logger.error(f"Error optimizing content for {platform}: {str(e)}")
        raise

def post_to_platform(platform: str, content: str) -> dict:
    """Posts optimized content to the specified platform."""
    if platform == "Threads":
        return post_to_threads(content)
    elif platform == "Twitter":
        return post_to_twitter(content)
    elif platform == "LinkedIn":
        return post_to_linkedin(content)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

def post_to_threads(content: str) -> dict:
    """Posts content to Threads with error handling."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.THREADS_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "app_id": Config.THREADS_APP_ID,
            "content": content
        }
        response = requests.post(
            Config.THREADS_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Threads API error: {str(e)}")
        raise

def post_to_twitter(content: str) -> dict:
    """Posts content to Twitter with error handling."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.TWITTER_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"text": content}
        session = requests_retry_session()
        response = session.post(
            Config.TWITTER_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Twitter API error: {str(e)}")
        raise

def post_to_linkedin(content: str) -> dict:
    """Posts content to LinkedIn with error handling."""
    try:
        headers = {
            "Authorization": f"Bearer {Config.LINKEDIN_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        payload = {
            "author": f"urn:li:person:{Config.LINKEDIN_PERSON_URN}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        session = requests_retry_session()
        response = session.post(
            Config.LINKEDIN_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"LinkedIn API error: {str(e)}")
        raise

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """Creates a requests session with retry strategy."""
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session