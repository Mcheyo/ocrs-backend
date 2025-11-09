"""
OCRS Backend - Admin Routes
API endpoints for admin functions
"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from src.admin.models import AdminStatsModel, AdminEnrollmentModel, AdminCourseModel
from src.auth.decorators import require_auth, require_role
from src.utils.responses import success_response, error_response, created_response
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.admin.routes')

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/stats', methods=['GET'])
@require_auth
@require_role('admin')
def get_system_stats():
    """Get system statistics"""
    try:
        stats = AdminStatsModel.get_system_stats()
        enrollment_stats = AdminStatsModel.get_enrollment_stats_by_term()
        
        return success_response(data={
            'system': stats,
            'terms': enrollment_stats
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return error_response("An error occurred", 500)


@admin_bp.route('/enrollments', methods=['GET'])
@require_auth
@require_role('admin', 'faculty')
def get_all_enrollments():
    """Get all enrollments"""
    try:
        term_id = request.args.get('term_id', type=int)
        status = request.args.get('status')
        limit = min(request.args.get('limit', 100, type=int), 500)
        offset = request.args.get('offset', 0, type=int)
        
        enrollments = AdminEnrollmentModel.get_all_enrollments(
            term_id=term_id,
            status=status,
            limit=limit,
            offset=offset
        )
        
        return success_response(data={
            'enrollments': enrollments,
            'count': len(enrollments),
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        logger.error(f"Error fetching enrollments: {e}")
        return error_response("An error occurred", 500)


@admin_bp.route('/courses', methods=['POST'])
@require_auth
@require_role('admin')
def create_course():
    """Create a new course"""
    try:
        data = request.get_json()
        
        required = ['dept_id', 'course_number', 'title', 'credits']
        if not all(field in data for field in required):
            return error_response("Missing required fields", 400)
        
        course_id = AdminCourseModel.create_course(
            dept_id=data['dept_id'],
            course_number=data['course_number'],
            title=data['title'],
            description=data.get('description', ''),
            credits=data['credits']
        )
        
        if course_id:
            return created_response(
                data={'course_id': course_id},
                message="Course created successfully"
            )
        else:
            return error_response("Failed to create course", 500)
            
    except Exception as e:
        logger.error(f"Error creating course: {e}")
        return error_response("An error occurred", 500)


@admin_bp.route('/courses/<int:course_id>', methods=['PUT'])
@require_auth
@require_role('admin')
def update_course(course_id):
    """Update a course"""
    try:
        data = request.get_json()
        
        success = AdminCourseModel.update_course(course_id, **data)
        
        if success:
            return success_response(message="Course updated successfully")
        else:
            return error_response("Failed to update course", 500)
            
    except Exception as e:
        logger.error(f"Error updating course: {e}")
        return error_response("An error occurred", 500)


@admin_bp.route('/courses/<int:course_id>/deactivate', methods=['POST'])
@require_auth
@require_role('admin')
def deactivate_course(course_id):
    """Deactivate a course"""
    try:
        success = AdminCourseModel.deactivate_course(course_id)
        
        if success:
            return success_response(message="Course deactivated successfully")
        else:
            return error_response("Failed to deactivate course", 500)
            
    except Exception as e:
        logger.error(f"Error deactivating course: {e}")
        return error_response("An error occurred", 500)