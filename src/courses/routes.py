"""
OCRS Backend - Course Routes
API endpoints for course management
"""

from flask import Blueprint, request
from src.courses.models import CourseModel, DepartmentModel
from src.courses.utils import (
    format_course_response, format_section_response, format_department_response
)
from src.utils.responses import success_response, error_response, not_found_response
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.courses.routes')

# Create Blueprint
courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/', methods=['GET'])
def get_courses():
    """
    Get all courses with optional filters
    ---
    tags:
      - Courses
    parameters:
      - name: dept_id
        in: query
        type: integer
        description: Filter by department ID
      - name: min_credits
        in: query
        type: number
        description: Minimum credits
      - name: max_credits
        in: query
        type: number
        description: Maximum credits
      - name: level
        in: query
        type: string
        description: Course level (1, 2, 3, 4)
        enum: ['1', '2', '3', '4']
      - name: limit
        in: query
        type: integer
        default: 50
        description: Results per page
      - name: offset
        in: query
        type: integer
        default: 0
        description: Pagination offset
    responses:
      200:
        description: List of courses
    """
    try:
        # Get query parameters
        dept_id = request.args.get('dept_id', type=int)
        min_credits = request.args.get('min_credits', type=float)
        max_credits = request.args.get('max_credits', type=float)
        level = request.args.get('level')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Validate limit
        limit = min(max(1, limit), 100)  # Between 1 and 100
        
        # Get courses
        courses = CourseModel.get_all_courses(
            dept_id=dept_id,
            min_credits=min_credits,
            max_credits=max_credits,
            level=level,
            limit=limit,
            offset=offset
        )
        
        # Get total count for pagination
        total = CourseModel.get_total_courses(dept_id=dept_id)
        
        # Format response
        formatted_courses = [format_course_response(course) for course in courses]
        
        return success_response(
            data={
                'courses': formatted_courses,
                'pagination': {
                    'total': total,
                    'limit': limit,
                    'offset': offset,
                    'has_more': (offset + limit) < total
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        return error_response("An error occurred while fetching courses", 500)


@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """
    Get course by ID with full details
    ---
    tags:
      - Courses
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: Course ID
      - name: include_sections
        in: query
        type: boolean
        default: false
        description: Include section information
    responses:
      200:
        description: Course details
      404:
        description: Course not found
    """
    try:
        include_sections = request.args.get('include_sections', 'false').lower() == 'true'
        
        # Get course
        course = CourseModel.get_course_by_id(course_id)
        
        if not course:
            return not_found_response("Course not found")
        
        # Get prerequisites
        prerequisites = CourseModel.get_course_prerequisites(course_id)
        
        # Get sections if requested
        sections = None
        if include_sections:
            sections = CourseModel.get_course_sections(course_id)
        
        # Format response
        formatted_course = format_course_response(
            course,
            include_sections=include_sections,
            sections=sections,
            prerequisites=prerequisites
        )
        
        return success_response(data=formatted_course)
        
    except Exception as e:
        logger.error(f"Error fetching course {course_id}: {e}")
        return error_response("An error occurred while fetching course", 500)


@courses_bp.route('/search', methods=['GET'])
def search_courses():
    """
    Search courses by keyword
    ---
    tags:
      - Courses
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Search term
      - name: dept_id
        in: query
        type: integer
        description: Filter by department
      - name: limit
        in: query
        type: integer
        default: 50
        description: Maximum results
    responses:
      200:
        description: Search results
      400:
        description: Missing search term
    """
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return error_response("Search term is required", 400)
        
        if len(search_term) < 2:
            return error_response("Search term must be at least 2 characters", 400)
        
        dept_id = request.args.get('dept_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        limit = min(max(1, limit), 100)
        
        # Search courses
        courses = CourseModel.search_courses(search_term, dept_id=dept_id, limit=limit)
        
        # Format response
        formatted_courses = [format_course_response(course) for course in courses]
        
        return success_response(
            data={
                'courses': formatted_courses,
                'search_term': search_term,
                'result_count': len(formatted_courses)
            }
        )
        
    except Exception as e:
        logger.error(f"Error searching courses: {e}")
        return error_response("An error occurred during search", 500)


@courses_bp.route('/<int:course_id>/prerequisites', methods=['GET'])
def get_prerequisites(course_id):
    """
    Get prerequisites for a course
    ---
    tags:
      - Courses
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: Course ID
    responses:
      200:
        description: List of prerequisite courses
      404:
        description: Course not found
    """
    try:
        # Check if course exists
        course = CourseModel.get_course_by_id(course_id)
        
        if not course:
            return not_found_response("Course not found")
        
        # Get prerequisites
        prerequisites = CourseModel.get_course_prerequisites(course_id)
        
        # Format response
        formatted_prereqs = [
            {
                'course_id': prereq.get('course_id'),
                'course_code': prereq.get('course_code'),
                'title': prereq.get('title'),
                'credits': float(prereq.get('credits', 0))
            }
            for prereq in prerequisites
        ]
        
        return success_response(
            data={
                'course': {
                    'course_id': course['course_id'],
                    'course_code': f"{course['dept_code']} {course['course_number']}",
                    'title': course['title']
                },
                'prerequisites': formatted_prereqs
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching prerequisites: {e}")
        return error_response("An error occurred", 500)


@courses_bp.route('/<int:course_id>/sections', methods=['GET'])
def get_course_sections(course_id):
    """
    Get all sections for a course
    ---
    tags:
      - Courses
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: Course ID
      - name: term_id
        in: query
        type: integer
        description: Filter by term (defaults to current term)
    responses:
      200:
        description: List of sections
      404:
        description: Course not found
    """
    try:
        term_id = request.args.get('term_id', type=int)
        
        # Check if course exists
        course = CourseModel.get_course_by_id(course_id)
        
        if not course:
            return not_found_response("Course not found")
        
        # Get sections
        sections = CourseModel.get_course_sections(course_id, term_id=term_id)
        
        # Format response
        formatted_sections = [format_section_response(section) for section in sections]
        
        return success_response(
            data={
                'course': {
                    'course_id': course['course_id'],
                    'course_code': f"{course['dept_code']} {course['course_number']}",
                    'title': course['title']
                },
                'sections': formatted_sections,
                'section_count': len(formatted_sections)
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching sections: {e}")
        return error_response("An error occurred", 500)


@courses_bp.route('/departments', methods=['GET'])
def get_departments():
    """
    Get all departments
    ---
    tags:
      - Courses
    responses:
      200:
        description: List of departments
    """
    try:
        departments = DepartmentModel.get_all_departments()
        
        # Format response
        formatted_depts = [format_department_response(dept) for dept in departments]
        
        return success_response(data={'departments': formatted_depts})
        
    except Exception as e:
        logger.error(f"Error fetching departments: {e}")
        return error_response("An error occurred", 500)


@courses_bp.route('/departments/<string:dept_code>', methods=['GET'])
def get_department_courses(dept_code):
    """
    Get all courses in a department
    ---
    tags:
      - Courses
    parameters:
      - name: dept_code
        in: path
        type: string
        required: true
        description: Department code (e.g., CMSC)
    responses:
      200:
        description: List of courses
      404:
        description: Department not found
    """
    try:
        # Get department
        department = DepartmentModel.get_department_by_code(dept_code)
        
        if not department:
            return not_found_response("Department not found")
        
        # Get courses
        courses = CourseModel.get_courses_by_department(dept_code)
        
        # Format response
        formatted_courses = [format_course_response(course) for course in courses]
        
        return success_response(
            data={
                'department': format_department_response(department),
                'courses': formatted_courses,
                'course_count': len(formatted_courses)
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching department courses: {e}")
        return error_response("An error occurred", 500)
