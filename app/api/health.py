# app/api/health.py

from flask_restx import Namespace, Resource
from datetime import datetime

ns = Namespace('health', description='Health check operations')

@ns.route('/')
class HealthCheck(Resource):
    def get(self):
        """Health check endpoint."""
        return {
            "status": "OK",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }, 200