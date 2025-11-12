from flask import Blueprint, jsonify

test_bp = Blueprint("test", __name__)  # no prefix -> /ping

@test_bp.get("/ping")
def ping():
    return jsonify({"ok": True, "message": "Backend is connected!"}), 200
