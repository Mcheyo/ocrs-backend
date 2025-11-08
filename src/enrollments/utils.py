"""
OCRS Backend - Enrollment Utilities
Helper functions for enrollment management
"""

from src.utils.logger import setup_logger
from src.enrollments.models import EnrollmentModel

logger = setup_logger('ocrs.enrollments.utils')


def format_enrollment_response(enrollment):
    """
    Format enrollment data for API response
    
    Args:
        enrollment (dict): Enrollment data
        
    Returns:
        dict: Formatted enrollment data
    """
    if not enrollment:
        return None
    
    return {
        'enrollment_id': enrollment.get('enrollment_id'),
        'enrollment_date': str(enrollment.get('enrollment_date')) if enrollment.get('enrollment_date') else None,
        'status': enrollment.get('enrollment_status'),
        'grade': enrollment.get('grade'),
        'section': {
            'section_id': enrollment.get('section_id'),
            'section_number': enrollment.get('section_number'),
            'location': enrollment.get('location')
        },
        'course': {
            'course_id': enrollment.get('course_id'),
            'course_code': f"{enrollment.get('dept_code')} {enrollment.get('course_number')}",
            'title': enrollment.get('course_title'),
            'credits': float(enrollment.get('credits', 0))
        },
        'term': {
            'term_id': enrollment.get('term_id'),
            'name': enrollment.get('term_name'),
            'year': enrollment.get('term_year')
        } if enrollment.get('term_name') else None,
        'instructor': enrollment.get('instructor_name')
    }


def validate_enrollment(student_id, section_id, course_id, term_id):
    """
    Validate enrollment before processing
    
    Args:
        student_id (int): Student profile ID
        section_id (int): Section ID
        course_id (int): Course ID
        term_id (int): Term ID
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check prerequisites
    prereq_result = EnrollmentModel.check_prerequisites(student_id, course_id)
    if prereq_result and not prereq_result.get('prerequisites_met'):
        missing = prereq_result.get('missing_prerequisites', [])
        missing_courses = [p['course_code'] for p in missing]
        return False, {
            'error': 'Prerequisites not met',
            'code': 'PREREQUISITES_NOT_MET',
            'missing_prerequisites': missing_courses
        }
    
    # Check schedule conflicts
    conflict = EnrollmentModel.check_schedule_conflict(student_id, section_id)
    if conflict:
        return False, {
            'error': 'Schedule conflict detected',
            'code': 'SCHEDULE_CONFLICT',
            'conflicting_course': conflict.get('conflicting_course'),
            'day': conflict.get('day_of_week'),
            'time': f"{conflict.get('start_time')} - {conflict.get('end_time')}"
        }
    
    # Check credit hour limit (18 credits max)
    current_credits = EnrollmentModel.get_student_credit_hours(student_id, term_id)
    
    # Get course credits
    from src.courses.models import CourseModel
    course = CourseModel.get_course_by_id(course_id)
    if not course:
        return False, {'error': 'Course not found', 'code': 'COURSE_NOT_FOUND'}
    
    new_total = current_credits + float(course.get('credits', 0))
    if new_total > 18:
        return False, {
            'error': 'Credit hour limit exceeded',
            'code': 'CREDIT_LIMIT_EXCEEDED',
            'current_credits': current_credits,
            'course_credits': float(course.get('credits', 0)),
            'max_credits': 18
        }
    
    return True, None
