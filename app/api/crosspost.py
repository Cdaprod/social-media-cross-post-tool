# app/api/crosspost.py

from flask_restx import Namespace, Resource, fields
from flask import request
from ..utils import validate_content, optimize_content
from ..tasks import post_content_task
from ..rate_limiter import RedisRateLimiter
from ..config import Config, PLATFORM_CONSTRAINTS
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

ns = Namespace('crosspost', description='Cross-post operations')

post_model = ns.model('Post', {
    'content': fields.String(required=True, description='Content to cross-post')
})

# Initialize Rate Limiter
rate_limiter = RedisRateLimiter(Config.REDIS_URL, Config.RATE_LIMIT_REQUESTS, Config.RATE_LIMIT_WINDOW)

@ns.route('/')
class CrossPost(Resource):
    @ns.expect(post_model)
    def post(self):
        """Cross-post content between Threads, Twitter, and LinkedIn."""
        try:
            # Rate limiting check
            client_id = request.headers.get('X-API-Key', 'default')
            if not rate_limiter.is_allowed(client_id):
                return {"error": "Rate limit exceeded"}, 429

            # Input validation
            data = request.get_json()
            if not data:
                return {"error": "No JSON data provided"}, 400

            content = data.get('content')
            is_valid, error_message = validate_content(content)
            if not is_valid:
                return {"error": error_message}, 400

            # Optimize content for each platform
            optimized_content = {}
            for platform in PLATFORM_CONSTRAINTS.keys():
                optimized_content[platform] = optimize_content(content, platform)

            # Enqueue tasks
            task_results = {}
            for platform, opt_content in optimized_content.items():
                task = post_content_task.delay(platform, opt_content, client_id)
                task_results[platform] = task.id  # Return task IDs to client

            logger.info(f"Cross-post tasks enqueued for client {client_id}")

            return {
                "message": "Cross-post tasks enqueued",
                "tasks": task_results,
                "timestamp": datetime.utcnow().isoformat()
            }, 202

        except Exception as e:
            logger.error(f"Error in crosspost: {str(e)}")
            return {"error": "Internal server error"}, 500