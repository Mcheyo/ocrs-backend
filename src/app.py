import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from config.config import get_config
from src.utils.logger import setup_logger
from src.utils.responses import error_response
from src.chatbot.routes import chatbot_bp

logger = setup_logger("ocrs.app")


def create_app(config_name=None):
    app = Flask(__name__)

    config = get_config(config_name)
    app.config.from_object(config)

    init_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_health_check(app)

    logger.info(f"Application started in {config_name or 'development'} mode")
    return app


def init_extensions(app):
    CORS(app, origins=app.config["CORS_ORIGINS"])
    logger.info("CORS initialized")

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response("Token has expired", 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return error_response("Invalid token", 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return error_response("Authorization token required", 401)

    logger.info("JWT Manager initialized")

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "OCRS API",
            "description": "Online Course Registration System API Documentation",
            "version": "1.0.0",
            "contact": {
                "name": "OCRS Team",
                "email": "admin@umgc.edu",
            },
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
            }
        },
        "security": [{"Bearer": []}],
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    logger.info("Swagger documentation initialized at /api/docs")


def register_blueprints(app):
    from src.auth.routes import auth_bp
    from src.courses.routes import courses_bp
    from src.enrollments.routes import enrollments_bp
    from src.admin.routes import admin_bp
    from src.faculty.routes import faculty_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(courses_bp, url_prefix="/api/courses")
    app.register_blueprint(enrollments_bp, url_prefix="/api/enrollments")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(faculty_bp, url_prefix="/api/faculty")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

    logger.info("Blueprints registered")


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return error_response("Bad request", 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return error_response("Unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(error):
        return error_response("Forbidden", 403)

    @app.errorhandler(404)
    def not_found(error):
        return error_response("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response("Method not allowed", 405)

    @app.errorhandler(409)
    def conflict(error):
        return error_response("Resource conflict", 409)

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return error_response("Unprocessable entity", 422)

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal server error: {error}")
        return error_response("Internal server error", 500)

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.exception(f"Unhandled exception: {error}")
        return error_response("An unexpected error occurred", 500)

    logger.info("Error handlers registered")


def register_health_check(app):
    @app.route("/health", methods=["GET"])
    def health_root():
        return jsonify(
            {
                "status": "healthy",
                "service": "OCRS Backend",
                "version": app.config.get("APP_VERSION", "1.0.0"),
            }
        ), 200

    @app.route("/api/health", methods=["GET"])
    def api_health():
        return jsonify(
            {
                "status": "healthy",
                "service": "OCRS Backend API",
                "version": app.config.get("APP_VERSION", "1.0.0"),
                "components": {"app": "ok"},
            }
        ), 200

    @app.route("/api/health/app", methods=["GET"])
    def api_health_app():
        return jsonify(
            {
                "status": "healthy",
                "service": "OCRS Backend",
                "component": "app",
                "version": app.config.get("APP_VERSION", "1.0.0"),
            }
        ), 200

    @app.route("/", methods=["GET"])
    def index():
        return jsonify(
            {
                "message": "Welcome to OCRS API",
                "version": app.config.get("APP_VERSION", "1.0.0"),
                "documentation": "/api/docs",
            }
        ), 200

    logger.info("Health check endpoints registered")


app = create_app()

if __name__ == "__main__":
    config = get_config()
    app.run(host="0.0.0.0", port=5001, debug=True)
