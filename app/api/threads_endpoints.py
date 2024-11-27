# app/api/threads_endpoints.py

from flask_restx import Namespace, Resource, fields
from flask import request
from ..threads import get_thread_replies, reply_to_thread, delete_thread_reply, get_thread_insights
from ..config import Config
from ..rate_limiter import RedisRateLimiter
import logging

logger = logging.getLogger(__name__)

ns = Namespace('threads', description='Threads operations')

# Models for request and response validation
reply_model = ns.model('Reply', {
    'message': fields.String(required=True, description='Reply message')
})

# Initialize Rate Limiter
rate_limiter = RedisRateLimiter(Config.REDIS_URL, Config.RATE_LIMIT_REQUESTS, Config.RATE_LIMIT_WINDOW)

@ns.route('/<string:thread_id>/replies')
class ThreadReplies(Resource):
    def get(self, thread_id):
        """Fetch replies to a specific thread."""
        try:
            # Rate limiting
            client_id = request.headers.get('X-API-Key', 'default')
            if not rate_limiter.is_allowed(client_id):
                return {"error": "Rate limit exceeded"}, 429

            replies = get_thread_replies(thread_id)
            return replies, 200

        except Exception as e:
            logger.error(f"Error fetching replies for thread {thread_id}: {str(e)}")
            return {"error": "Internal server error"}, 500

    @ns.expect(reply_model)
    def post(self, thread_id):
        """Post a reply to a specific thread."""
        try:
            # Rate limiting
            client_id = request.headers.get('X-API-Key', 'default')
            if not rate_limiter.is_allowed(client_id):
                return {"error": "Rate limit exceeded"}, 429

            data = request.get_json()
            message = data.get('message')
            if not message:
                return {"error": "Message content is required"}, 400

            response = reply_to_thread(thread_id, message)
            return response, 201

        except Exception as e:
            logger.error(f"Error posting reply to thread {thread_id}: {str(e)}")
            return {"error": "Internal server error"}, 500

@ns.route('/<string:thread_id>/replies/<string:reply_id>')
class ThreadReply(Resource):
    def delete(self, thread_id, reply_id):
        """Delete a reply from a thread."""
        try:
            # Rate limiting
            client_id = request.headers.get('X-API-Key', 'default')
            if not rate_limiter.is_allowed(client_id):
                return {"error": "Rate limit exceeded"}, 429

            response = delete_thread_reply(thread_id, reply_id)
            return response, 200

        except Exception as e:
            logger.error(f"Error deleting reply {reply_id} from thread {thread_id}: {str(e)}")
            return {"error": "Internal server error"}, 500

@ns.route('/<string:thread_id>/insights')
class ThreadInsights(Resource):
    def get(self, thread_id):
        """Fetch insights for a specific thread."""
        try:
            # Rate limiting
            client_id = request.headers.get('X-API-Key', 'default')
            if not rate_limiter.is_allowed(client_id):
                return {"error": "Rate limit exceeded"}, 429

            insights = get_thread_insights(thread_id)
            return insights, 200

        except Exception as e:
            logger.error(f"Error fetching insights for thread {thread_id}: {str(e)}")
            return {"error": "Internal server error"}, 500