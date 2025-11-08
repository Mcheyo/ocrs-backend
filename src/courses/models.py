"""
OCRS Backend - Course Models
Database operations for course management
"""

from src.utils.database import execute_query, get_db_cursor
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.courses.models')


class CourseModel:
    """Course database operations"""
    
    @staticmethod
    def get_all_courses(dept_id=None, min_credits=None, max_credits=None, 
                       level=None, limit=50, offset=0):
        """
        Get all courses with optional filters
        
        Args:
            dept_id (int): Filter by department ID
            min_credits (float): Minimum credits
            max_credits (float): Maximum credits
            level (str): Course level (100, 200, 300, 400)
            limit (int): Number of results
            offset (int): Pagination offset
            
        Returns:
            list: List of courses
        """
        try:
            query = """
                SELECT 
                    c.course_id,
                    c.course_number,
                    c.title,
                    c.description,
                    c.credits,
                    c.is_active,
                    d.dept_id,
                    d.code as dept_code,
                    d.name as dept_name,
                    (SELECT COUNT(*) FROM section s WHERE s.course_id = c.course_id) as section_count
                FROM course c
                JOIN department d ON c.dept_id = d.dept_id
                WHERE c.is_active = 1
            """
            
            params = []
            
            # Add filters
            if dept_id:
                query += " AND c.dept_id = %s"
                params.append(dept_id)
            
            if min_credits:
                query += " AND c.credits >= %s"
                params.append(min_credits)
            
            if max_credits:
                query += " AND c.credits <= %s"
                params.append(max_credits)
            
            if level:
                # Level is first digit of course number (e.g., 100-level, 200-level)
                query += " AND c.course_number LIKE %s"
                params.append(f"{level}%")
            
            query += " ORDER BY d.code, c.course_number"
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            return execute_query(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Error fetching courses: {e}")
            return []
    
    @staticmethod
    def get_course_by_id(course_id):
        """
        Get course by ID with full details
        
        Args:
            course_id (int): Course ID
            
        Returns:
            dict: Course details or None
        """
        try:
            query = """
                SELECT 
                    c.course_id,
                    c.course_number,
                    c.title,
                    c.description,
                    c.credits,
                    c.is_active,
                    d.dept_id,
                    d.code as dept_code,
                    d.name as dept_name,
                    d.description as dept_description,
                    c.created_at,
                    c.updated_at
                FROM course c
                JOIN department d ON c.dept_id = d.dept_id
                WHERE c.course_id = %s
            """
            return execute_query(query, (course_id,), fetch_one=True)
            
        except Exception as e:
            logger.error(f"Error fetching course by ID: {e}")
            return None
    
    @staticmethod
    def search_courses(search_term, dept_id=None, limit=50):
        """
        Search courses by title, course number, or description
        
        Args:
            search_term (str): Search term
            dept_id (int): Optional department filter
            limit (int): Maximum results
            
        Returns:
            list: List of matching courses
        """
        try:
            query = """
                SELECT 
                    c.course_id,
                    c.course_number,
                    c.title,
                    c.description,
                    c.credits,
                    d.code as dept_code,
                    d.name as dept_name,
                    CONCAT(d.code, ' ', c.course_number, ' - ', c.title) as full_title
                FROM course c
                JOIN department d ON c.dept_id = d.dept_id
                WHERE c.is_active = 1
                AND (
                    c.title LIKE %s
                    OR c.course_number LIKE %s
                    OR c.description LIKE %s
                    OR d.code LIKE %s
                )
            """
            
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern, search_pattern]
            
            if dept_id:
                query += " AND c.dept_id = %s"
                params.append(dept_id)
            
            query += " ORDER BY d.code, c.course_number LIMIT %s"
            params.append(limit)
            
            return execute_query(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Error searching courses: {e}")
            return []
    
    @staticmethod
    def get_course_prerequisites(course_id):
        """
        Get prerequisites for a course
        
        Args:
            course_id (int): Course ID
            
        Returns:
            list: List of prerequisite courses
        """
        try:
            query = """
                SELECT 
                    c.course_id,
                    c.course_number,
                    c.title,
                    c.credits,
                    d.code as dept_code,
                    CONCAT(d.code, ' ', c.course_number) as course_code
                FROM course_prerequisite cp
                JOIN course c ON cp.prereq_course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                WHERE cp.course_id = %s
                ORDER BY d.code, c.course_number
            """
            return execute_query(query, (course_id,))
            
        except Exception as e:
            logger.error(f"Error fetching prerequisites: {e}")
            return []
    
    @staticmethod
    def get_courses_by_department(dept_code):
        """
        Get all courses in a department
        
        Args:
            dept_code (str): Department code (e.g., 'CMSC')
            
        Returns:
            list: List of courses
        """
        try:
            query = """
                SELECT 
                    c.course_id,
                    c.course_number,
                    c.title,
                    c.description,
                    c.credits,
                    d.code as dept_code,
                    d.name as dept_name
                FROM course c
                JOIN department d ON c.dept_id = d.dept_id
                WHERE d.code = %s AND c.is_active = 1
                ORDER BY c.course_number
            """
            return execute_query(query, (dept_code.upper(),))
            
        except Exception as e:
            logger.error(f"Error fetching courses by department: {e}")
            return []
    
    @staticmethod
    def get_course_sections(course_id, term_id=None):
        """
        Get all sections for a course
        
        Args:
            course_id (int): Course ID
            term_id (int): Optional term filter (defaults to current term)
            
        Returns:
            list: List of sections
        """
        try:
            query = """
                SELECT 
                    s.section_id,
                    s.section_number,
                    s.capacity,
                    s.location,
                    s.status,
                    COALESCE(enrolled.count, 0) as enrolled_count,
                    COALESCE(waitlist.count, 0) as waitlist_count,
                    t.term_id,
                    t.name as term_name,
                    t.year as term_year,
                    CONCAT(u.first_name, ' ', u.last_name) as instructor_name,
                    u.email as instructor_email
                FROM section s
                JOIN term t ON s.term_id = t.term_id
                LEFT JOIN user_account u ON s.instructor_id = u.user_id
                LEFT JOIN (
                    SELECT section_id, COUNT(*) as count 
                    FROM enrollment 
                    WHERE enrollment_status = 'Enrolled'
                    GROUP BY section_id
                ) enrolled ON s.section_id = enrolled.section_id
                LEFT JOIN (
                    SELECT section_id, COUNT(*) as count 
                    FROM waitlist 
                    WHERE status = 'Active'
                    GROUP BY section_id
                ) waitlist ON s.section_id = waitlist.section_id
                WHERE s.course_id = %s
            """
            
            params = [course_id]
            
            if term_id:
                query += " AND s.term_id = %s"
                params.append(term_id)
            else:
                query += " AND t.is_current = 1"
            
            query += " ORDER BY s.section_number"
            
            return execute_query(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Error fetching course sections: {e}")
            return []
    
    @staticmethod
    def get_total_courses(dept_id=None):
        """
        Get total count of courses (for pagination)
        
        Args:
            dept_id (int): Optional department filter
            
        Returns:
            int: Total course count
        """
        try:
            query = "SELECT COUNT(*) as count FROM course WHERE is_active = 1"
            params = []
            
            if dept_id:
                query += " AND dept_id = %s"
                params.append(dept_id)
            
            result = execute_query(query, tuple(params) if params else None, fetch_one=True)
            return result['count'] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting course count: {e}")
            return 0


class DepartmentModel:
    """Department database operations"""
    
    @staticmethod
    def get_all_departments():
        """
        Get all departments
        
        Returns:
            list: List of departments
        """
        try:
            query = """
                SELECT 
                    d.dept_id,
                    d.code,
                    d.name,
                    d.description,
                    COUNT(c.course_id) as course_count
                FROM department d
                LEFT JOIN course c ON d.dept_id = c.dept_id AND c.is_active = 1
                GROUP BY d.dept_id, d.code, d.name, d.description
                ORDER BY d.code
            """
            return execute_query(query)
            
        except Exception as e:
            logger.error(f"Error fetching departments: {e}")
            return []
    
    @staticmethod
    def get_department_by_code(dept_code):
        """
        Get department by code
        
        Args:
            dept_code (str): Department code
            
        Returns:
            dict: Department details or None
        """
        try:
            query = """
                SELECT 
                    d.dept_id,
                    d.code,
                    d.name,
                    d.description,
                    COUNT(c.course_id) as course_count
                FROM department d
                LEFT JOIN course c ON d.dept_id = c.dept_id AND c.is_active = 1
                WHERE d.code = %s
                GROUP BY d.dept_id, d.code, d.name, d.description
            """
            return execute_query(query, (dept_code.upper(),), fetch_one=True)
            
        except Exception as e:
            logger.error(f"Error fetching department: {e}")
            return None
