from datetime import datetime
from flask import request, jsonify
from src.chatbot import chatbot_bp
from src.utils.logger import setup_logger

logger = setup_logger("ocrs.chatbot")


def _generate_reply(message: str, current_user=None) -> str:
    if not message:
        return (
            "Hi! I’m the OCRS helper bot. Ask me something like "
            "\"What should I take next?\" or \"How do I drop a course?\""
        )

    text = message.lower().strip()

    if "what" in text and "take" in text:
        return (
            "For this demo, a typical CS path is:\n"
            "- Intro to Programming → Computer Science I → Computer Science II\n"
            "- Then Data Structures and Database Management.\n"
            "You can browse the Courses tab and check prerequisites before enrolling."
        )

    if "register" in text or "enroll" in text or "sign up" in text:
        return (
            "To register in OCRS:\n"
            "1) Log in as a student.\n"
            "2) Browse courses and choose a section that fits your schedule.\n"
            "3) Click Enroll to add it to your schedule.\n"
            "4) Review the confirmation panel to make sure everything looks correct."
        )

    if "drop" in text or "withdraw" in text:
        return (
            "To drop a course, locate it in your current schedule and choose Drop.\n"
            "The system will update your enrollment and free the seat."
        )

    if "prereq" in text or "prerequisite" in text:
        return (
            "Prerequisites are defined per course. In a full system OCRS would "
            "check your completed courses before allowing enrollment.\n"
            "For this demo, please refer to the course detail panel in the UI."
        )

    if "gpa" in text or "progress" in text:
        return (
            "In a complete OCRS deployment, I would pull your GPA and program "
            "progress from your student record. In this demo that data is not "
            "connected yet, but advisors would use OCRS to help track it."
        )

    if "help" in text or "what can you do" in text or "?" in text:
        return (
            "I can help explain how to:\n"
            "- Browse and filter courses\n"
            "- Enroll or drop a class\n"
            "- Understand prerequisites at a high level\n"
            "- Think about next courses in the CS path\n"
            "Try asking: \"What should I take after Data Structures?\""
        )

    return (
        "Thanks for your question! In this demo I only handle registration and "
        "planning topics. Try asking about:\n"
        "• how to register or drop a course\n"
        "• what courses to take next\n"
        "• where prerequisites are checked."
    )


@chatbot_bp.route("/message", methods=["POST"])
def chatbot_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    current_user = data.get("user")

    logger.info(f"Chatbot received message: {message!r}")

    reply = _generate_reply(message, current_user)

    return jsonify(
        {
            "success": True,
            "data": {
                "request": message,
                "reply": reply,
                "user": current_user,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
    ), 200
