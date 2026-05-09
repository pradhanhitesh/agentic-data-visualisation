import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from routes.assets import assets_bp
from tools.extensions import limiter

# Load environment variables
env_path = os.path.join(
    os.path.dirname(__file__),
    "credentials.env"
)

# Load environment variables from credentials.env
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)

# Create app
def create_app():
    app = Flask(__name__)

    # App configuration
    app.config["JSON_SORT_KEYS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024

    # CORS configuration
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": os.getenv("CORS_ORIGINS", "*").split(",")
            }
        }
    )

    # Initialize limiter
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(
        assets_bp,
        url_prefix="/api/v1/assets"
    )

    # Index route
    @app.route("/")
    @limiter.exempt
    def index():
        return jsonify({
            "message": "API running"
        }), 200

    # Health route
    @app.route("/api/v1/health")
    @limiter.exempt
    def health():
        return jsonify({
            "status": "ok"
        }), 200

    # Error handlers
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "rate_limit_exceeded",
            "message": str(e)
        }), 429

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({
            "error": "not_found"
        }), 404

    @app.errorhandler(500)
    def internal_error(_):
        return jsonify({
            "error": "internal_server_error"
        }), 500

    return app

# App instance
app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 9898)),
        debug=False
    )