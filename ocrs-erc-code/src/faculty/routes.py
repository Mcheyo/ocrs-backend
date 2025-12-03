"""
OCRS Backend - Faculty Routes
API endpoints for faculty functions
"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from src.faculty.models import FacultyModel
from src.auth.decorators import require_auth, require_role
from src.utils.responses import success_response, error_response, not_found_response
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.faculty.routes')

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.route('/my-sections', methods=['GET'])
@require_auth
@require_role('faculty', 'admin')
def get_my_sections():
    """
    Get faculty's assigned sections
    ---
    tags:
      - Faculty
    security:
      - Bearer: []
    parameters:
      - name: term_id
        in: query
        type: integer
        description: Filter by term (defaults to current term)
    responses:
      200:
        description: List of assigned sections
      404:
        description: Faculty profile not found
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Get faculty profile
        faculty_id = FacultyModel.get_faculty_id_from_user(user_id)
        if not faculty_id:
            return error_response("Faculty profile not found", 404)
        
        term_id = request.args.get('term_id', type=int)
        
        # Get sections
        sections = FacultyModel.get_faculty_sections(faculty_id, term_id=term_id)
        
        # Format response
        formatted_sections = []
        for section in sections:
            formatted_sections.append({
                'section_id': section['section_id'],
                'section_number': section['section_number'],
                'course': {
                    'course_id': section['course_id'],
                    'course_code': f"{section['dept_code']} {section['course_number']}",
                    'title': section['course_title'],
                    'credits': float(section['credits'])
                },
                'capacity': section['capacity'],
                'enrolled_count': section['enrolled_count'],
                'available_seats': section['capacity'] - section['enrolled_count'],
                'waitlist_count': section['waitlist_count'],
                'location': section['location'],
                'status': section['status'],
                'term': {
                    'term_id': section['term_id'],
                    'name': section['term_name'],
                    'year': section['term_year'],
                    'is_current': bool(section['is_current'])
                }
            })
        
        return success_response(data={
            'sections': formatted_sections,
            'count': len(formatted_sections)
        })
        
    except Exception as e:
        logger.error(f"Error fetching faculty sections: {e}")
        return error_response("An error occurred", 500)


@faculty_bp.route('/sections/<int:section_id>/roster', methods=['GET'])
@require_auth
@require_role('faculty', 'admin')
def get_section_roster(section_id):
    """
    Get roster for a specific section
    ---
    tags:
      - Faculty
    security:
      - Bearer: []
    parameters:
      - name: section_id
        in: path
        type: integer
        required: true
        description: Section ID
    responses:
      200:
        description: Class roster
      403:
        description: Not authorized to view this roster
      404:
        description: Section not found
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Get faculty profile
        faculty_id = FacultyModel.get_faculty_id_from_user(user_id)
        if not faculty_id:
            return error_response("Faculty profile not found", 404)
        
        # Get roster
        roster = FacultyModel.get_section_roster(section_id, faculty_id)
        
        if roster is None:
            return error_response(
                "You are not authorized to view this section's roster",
                403
            )
        
        # Format response
        formatted_roster = []
        for student in roster:
            formatted_roster.append({
                'enrollment_id': student['enrollment_id'],
                'student': {
                    'student_id': student['student_id'],
                    'student_number': student['student_number'],
                    'name': f"{student['first_name']} {student['last_name']}",
                    'email': student['email'],
                    'level': student['level']
                },
                'status': student['enrollment_status'],
                'grade': student['grade']
            })
        
        return success_response(data={
            'roster': formatted_roster,
            'student_count': len(formatted_roster)
        })
        
    except Exception as e:
        logger.error(f"Error fetching roster: {e}")
        return error_response("An error occurred", 500)


@faculty_bp.route('/grades/<int:enrollment_id>', methods=['PUT'])
@require_auth
@require_role('faculty', 'admin')
def update_student_grade(enrollment_id):
    """
    Update student grade
    ---
    tags:
      - Faculty
    security:
      - Bearer: []
    parameters:
      - name: enrollment_id
        in: path
        type: integer
        required: true
        description: Enrollment ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - grade
          properties:
            grade:
              type: string
              enum: [A, B, C, D, F, P, NP, W, I]
              example: A
    responses:
      200:
        description: Grade updated successfully
      400:
        description: Invalid grade
      403:
        description: Not authorized to update this grade
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Get faculty profile
        faculty_id = FacultyModel.get_faculty_id_from_user(user_id)
        if not faculty_id:
            return error_response("Faculty profile not found", 404)
        
        data = request.get_json()
        grade = data.get('grade', '').upper()
        
        if not grade:
            return error_response("Grade is required", 400)
        
        # Update grade
        success = FacultyModel.update_grade(enrollment_id, grade, faculty_id)
        
        if not success:
            return error_response(
                "Failed to update grade. Invalid grade or unauthorized access.",
                403
            )
        
        logger.info(f"Faculty {faculty_id} updated grade for enrollment {enrollment_id}: {grade}")
        
        return success_response(message="Grade updated successfully")
        
    except Exception as e:
        logger.error(f"Error updating grade: {e}")
        return error_response("An error occurred", 500)


@faculty_bp.route('/sections/<int:section_id>/statistics', methods=['GET'])
@require_auth
@require_role('faculty', 'admin')
def get_section_statistics(section_id):
    """
    Get statistics for a section
    ---
    tags:
      - Faculty
    security:
      - Bearer: []
    parameters:
      - name: section_id
        in: path
        type: integer
        required: true
        description: Section ID
    responses:
      200:
        description: Section statistics
      403:
        description: Not authorized to view this section
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Get faculty profile
        faculty_id = FacultyModel.get_faculty_id_from_user(user_id)
        if not faculty_id:
            return error_response("Faculty profile not found", 404)
        
        # Get statistics
        stats = FacultyModel.get_section_statistics(section_id, faculty_id)
        
        if not stats:
            return error_response(
                "You are not authorized to view this section's statistics",
                403
            )
        
        # Format response
        total_graded = (
            stats['grade_a'] + stats['grade_b'] + stats['grade_c'] +
            stats['grade_d'] + stats['grade_f']
        )
        
        grade_distribution = {
            'A': stats['grade_a'],
            'B': stats['grade_b'],
            'C': stats['grade_c'],
            'D': stats['grade_d'],
            'F': stats['grade_f']
        }
        
        return success_response(data={
            'capacity': stats['capacity'],
            'enrolled': stats['enrolled_count'],
            'dropped': stats['dropped_count'],
            'completed': stats['completed_count'],
            'waitlist': stats['waitlist_count'],
            'available_seats': stats['capacity'] - stats['enrolled_count'],
            'grade_distribution': grade_distribution,
            'graded_count': total_graded
        })
        
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return error_response("An error occurred", 500)