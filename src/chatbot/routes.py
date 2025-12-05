from datetime import datetime
from flask import request, jsonify
from src.chatbot import chatbot_bp
from src.utils.logger import setup_logger

logger = setup_logger("ocrs.chatbot")


def _generate_reply(message: str, current_user=None) -> str:
    """Simple rule-based reply engine for the OCRS AI Advisor.

    It can answer:
    - Registration / system questions (how to register, drop, how OCRS works)
    - Academic advising questions (what to take next, prerequisites, GPA)
    """
    if not message:
        return (
            "Hi! I’m the OCRS AI Advisor. I can help you with registration and system questions "
            "(how to register, drop, login issues, course status) and academic planning "
            "(what courses to take next, prerequisites, GPA questions). "
            "What would you like help with?"
        )

    text = message.lower().strip()

    # ---- Academic planning / “what should I take next?” ----
    if "what" in text and "take" in text:
        return (
            "For this demo, a typical Computer Science path looks like:\n"
            "- Intro to Programming → Computer Science I → Computer Science II\n"
            "- Then Data Structures and Database Management\n"
            "- Followed by Algorithms, Software Engineering, and Capstone.\n\n"
            "You can browse the Courses tab, check prerequisites, and then click Enroll "
            "when you are ready."
        )

    # ---- Registration / enrollment workflow ----
    if "register" in text or "enroll" in text or "sign up" in text:
        return (
            "To register for a course in OCRS:\n"
            "1) Log in as a student.\n"
            "2) Go to the Courses tab and search or filter for the class you need.\n"
            "3) Check that you meet the prerequisites.\n"
            "4) Click the Enroll button for the course.\n"
            "5) Verify it appears under your My Courses panel."
        )

    # ---- Dropping / withdrawing ----
    if "drop" in text or "withdraw" in text:
        return (
            "To drop a course in OCRS:\n"
            "1) Open the dashboard and locate the course under My Courses.\n"
            "2) Click the Drop button next to that course.\n"
            "3) The enrollment status will update and the seat will be freed.\n\n"
            "Always check academic and financial deadlines before dropping a class."
        )

    # ---- Prerequisites ----
    if "prereq" in text or "prerequisite" in text:
        return (
            "Each course lists its prerequisites in the course details.\n"
            "In a full OCRS deployment, the system would check your completed courses "
            "before allowing enrollment.\n"
            "In this demo, please use the course information panel to verify prerequisites "
            "before clicking Enroll."
        )

    # ---- GPA / progress / advising-ish questions ----
    if "gpa" in text or "progress" in text or "graduation" in text:
        return (
            "In a complete OCRS system, I would read your GPA and degree progress from "
            "your student record to give precise advice.\n"
            "For this demo, GPA and program audit data are static, but you can still use OCRS "
            "to explore courses that move you toward your concentration and capstone."
        )

    # ---- General 'help' or '?' ----
    if "help" in text or "what can you do" in text or "?" in text:
        return (
            "I’m the OCRS AI Advisor. I can explain how to:\n"
            "- Browse and filter courses\n"
            "- Enroll or drop a class\n"
            "- Understand prerequisites at a high level\n"
            "- Think about which CS courses to take next\n\n"
            "Try something like:\n"
            "• \"What should I take after Data Structures?\"\n"
            "• \"How do I drop a course in OCRS?\""
        )

    # ---- Default fallback ----
    return (
        "Thanks for your question! In this demo I can help with registration and planning topics.\n"
        "Try asking about:\n"
        "• how to register or drop a course\n"
        "• what courses to take next\n"
        "• where to see prerequisites or GPA information."
    )


@chatbot_bp.route("/message", methods=["POST"])
def chatbot_message():
  """
  Chatbot endpoint for the OCRS AI Advisor.

  Expects JSON: { "message": "<user text>", "user": { ...optional... } }
  Returns: { success, data: { request, reply, user }, timestamp }
  """
  data = request.get_json(silent=True) or {}
  message = data.get("message", "")
  current_user = data.get("user")

  logger.info(f"Chatbot received message: {message!r} from user: {current_user}")

  reply = _generate_reply(message, current_user)

  return (
      jsonify(
          {
              "success": True,
              "data": {
                  "request": message,
                  "reply": reply,
                  "user": current_user,
              },
              "timestamp": datetime.utcnow().isoformat(),
          }
      ),
      200,
  )
