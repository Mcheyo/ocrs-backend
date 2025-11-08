"""
OCRS Backend - Course Utilities
Helper functions for course management
"""

from src.utils.logger import setup_logger

logger = setup_logger('ocrs.courses.utils')


def format_course_response(course, include_sections=False, sections=None, prerequisites=None):
    """
    Format course data for API response
    
    Args:
        course (dict): Course data
        include_sections (bool): Include section information
        sections (list): Section data
        prerequisites (list): Prerequisite courses
        
    Returns:
        dict: Formatted course data
    """
    if not course:
        return None
    
    formatted = {
        'course_id': course.get('course_id'),
        'course_number': course.get('course_number'),
        'title': course.get('title'),
        'description': course.get('description'),
        'credits': float(course.get('credits', 0)),
        'department': {
            'dept_id': course.get('dept_id'),
            'code': course.get('dept_code'),
            'name': course.get('dept_name')
        },
        'full_course_code': f"{course.get('dept_code')} {course.get('course_number')}",
        'is_active': bool(course.get('is_active', 1))
    }
    
    # Add prerequisites if provided
    if prerequisites is not None:
        formatted['prerequisites'] = [
            {
                'course_id': prereq.get('course_id'),
                'course_code': prereq.get('course_code'),
                'title': prereq.get('title')
            }
            for prereq in prerequisites
        ]
    
    # Add sections if provided
    if include_sections and sections is not None:
        formatted['sections'] = [
            format_section_response(section)
            for section in sections
        ]
    
    return formatted


def format_section_response(section):
    """
    Format section data for API response
    
    Args:
        section (dict): Section data
        
    Returns:
        dict: Formatted section data
    """
    if not section:
        return None
    
    enrolled = section.get('enrolled_count', 0)
    capacity = section.get('capacity', 0)
    available_seats = max(0, capacity - enrolled)
    is_full = enrolled >= capacity
    
    return {
        'section_id': section.get('section_id'),
        'section_number': section.get('section_number'),
        'capacity': capacity,
        'enrolled_count': enrolled,
        'available_seats': available_seats,
        'waitlist_count': section.get('waitlist_count', 0),
        'is_full': is_full,
        'location': section.get('location'),
        'status': section.get('status'),
        'term': {
            'term_id': section.get('term_id'),
            'name': section.get('term_name'),
            'year': section.get('term_year')
        },
        'instructor': {
            'name': section.get('instructor_name'),
            'email': section.get('instructor_email')
        } if section.get('instructor_name') else None
    }


def format_department_response(department):
    """
    Format department data for API response
    
    Args:
        department (dict): Department data
        
    Returns:
        dict: Formatted department data
    """
    if not department:
        return None
    
    return {
        'dept_id': department.get('dept_id'),
        'code': department.get('code'),
        'name': department.get('name'),
        'description': department.get('description'),
        'course_count': department.get('course_count', 0)
    }
