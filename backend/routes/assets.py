import os
import uuid
import shutil

from flask import Blueprint, request, jsonify, send_from_directory
from tools.extensions import limiter
from pipepline.alpha import run_pipeline
from tools.report import save_report

# Register blueprint
assets_bp = Blueprint("assets", __name__, url_prefix="/api/v1/assets")

# Define base directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sessions")
)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

@assets_bp.route("/upload", methods=["POST"])
@limiter.limit("5 per hour")
def upload_file():
    # Check if file is uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Get file
        file = request.files["file"]

        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return jsonify({"error": f"Only .csv and .xlsx files are allowed. Got '{ext}'"}), 400

        # Generate session ID
        session_id = uuid.uuid4().hex

        session_path = os.path.join(BASE_DIR, session_id)
        os.makedirs(session_path, exist_ok=True)

        file_path = os.path.join(session_path, file.filename)
        file.save(file_path)

        # Trigger pipeline here
        run_pipeline(filepath=file_path, session_id=session_id)

        return jsonify({
            "session_id": session_id,
            "filename": file.filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@assets_bp.route("/<session_id>", methods=["GET"])
def get_session(session_id):
    session_path = os.path.join(BASE_DIR, session_id)

    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found"}), 404

    # Insights
    insight_path = os.path.join(session_path, "insight.md")
    insight = ""
    if os.path.exists(insight_path):
        with open(insight_path, "r", encoding="utf-8") as f:
            insight = f.read()

    # Plots
    plots_dir = os.path.join(session_path, "plots")
    plots = []

    if os.path.exists(plots_dir):
        for file in os.listdir(plots_dir):
            plots.append(f"/api/v1/assets/{session_id}/plots/{file}")

    return jsonify({
        "session_id": session_id,
        "insight": insight,
        "plots": plots
    })

@assets_bp.route("/<session_id>/plots/<filename>")
def serve_plot(session_id, filename):
    plots_dir = os.path.join(BASE_DIR, session_id, "plots")
    return send_from_directory(plots_dir, filename)

@assets_bp.route("/download/<session_id>", methods=["GET"])
def generate_report(session_id):
    session_path = os.path.join(BASE_DIR, session_id)
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found"}), 404
    
    report_path = save_report(session_id)
    if not report_path:
        return jsonify({"error": "Failed to generate report"}), 500
    
    return send_from_directory(session_path, "report.pdf", as_attachment=True)


@assets_bp.route("/delete/<session_id>", methods=["GET"])
def delete_session(session_id):
    session_path = os.path.join(BASE_DIR, session_id)
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found"}), 404
    
    try:
        shutil.rmtree(session_path)
        return jsonify({"message": "Session deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
