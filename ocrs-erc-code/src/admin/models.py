"""
OCRS Backend - Admin Models
Database operations for admin functions
"""

from src.utils.database import execute_query, execute_update, get_db_cursor
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.admin.models')


class AdminStatsModel:
    """System statistics for admin dashboard"""
    
    @staticmethod
    def get_system_stats():
        """Get overall system statistics"""
        try:
            query = """
                SELECT 
                    (SELECT COUNT(*) FROM user_account WHERE is_active = 1) as total_users,
                    (SELECT COUNT(*) FROM user_account ua JOIN role r ON ua.role_id = r.role_id 
                     WHERE r.role_name = 'student' AND ua.is_active = 1) as total_students,
                    (SELECT COUNT(*) FROM user_account ua JOIN role r ON ua.role_id = r.role_id 
                     WHERE r.role_name = 'faculty' AND ua.is_active = 1) as total_faculty,
                    (SELECT COUNT(*) FROM course WHERE is_active = 1) as total_courses,
                    (SELECT COUNT(*) FROM section s JOIN term t ON s.term_id = t.term_id 
                     WHERE t.is_current = 1) as current_sections,
                    (SELECT COUNT(*) FROM enrollment e JOIN section s ON e.section_id = s.section_id
                     JOIN term t ON s.term_id = t.term_id 
                     WHERE t.is_current = 1 AND e.enrollment_status = 'Enrolled') as current_enrollments
            """
            return execute_query(query, fetch_one=True)
        except Exception as e:
            logger.error(f"Error fetching system stats: {e}")
            return None
    
    @staticmethod
    def get_enrollment_stats_by_term(term_id=None):
        """Get enrollment statistics by term"""
        try:
            query = """
                SELECT 
                    t.term_id,
                    t.name as term_name,
                    t.year,
                    COUNT(DISTINCT e.student_id) as enrolled_students,
                    COUNT(DISTINCT s.section_id) as sections_offered,
                    COUNT(e.enrollment_id) as total_enrollments,
                    COALESCE(SUM(c.credits), 0) as total_credit_hours
                FROM term t
                LEFT JOIN section s ON t.term_id = s.term_id
                LEFT JOIN enrollment e ON s.section_id = e.section_id AND e.enrollment_status = 'Enrolled'
                LEFT JOIN course c ON s.course_id = c.course_id
            """
            
            if term_id:
                query += " WHERE t.term_id = %s"
                query += " GROUP BY t.term_id, t.name, t.year"
                return execute_query(query, (term_id,), fetch_one=True)
            else:
                query += " GROUP BY t.term_id, t.name, t.year ORDER BY t.year DESC, t.name"
                return execute_query(query)
                
        except Exception as e:
            logger.error(f"Error fetching enrollment stats: {e}")
            return [] if not term_id else None


class AdminEnrollmentModel:
    """Admin enrollment management"""
    
    @staticmethod
    def get_all_enrollments(term_id=None, status=None, limit=100, offset=0):
        """Get all enrollments with filters"""
        try:
            query = """
                SELECT 
                    e.enrollment_id,
                    e.enrollment_status,
                    e.grade,
                    CONCAT(u.first_name, ' ', u.last_name) as student_name,
                    u.email as student_email,
                    sp.student_number,
                    CONCAT(d.code, ' ', c.course_number) as course_code,
                    c.title as course_title,
                    s.section_number,
                    t.name as term_name,
                    t.year as term_year
                FROM enrollment e
                JOIN student_profile sp ON e.student_id = sp.student_id
                JOIN user_account u ON sp.user_id = u.user_id
                JOIN section s ON e.section_id = s.section_id
                JOIN course c ON s.course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                JOIN term t ON s.term_id = t.term_id
                WHERE 1=1
            """
            
            params = []
            
            if term_id:
                query += " AND t.term_id = %s"
                params.append(term_id)
            
            if status:
                query += " AND e.enrollment_status = %s"
                params.append(status)
            
            query += " ORDER BY t.year DESC, t.name, student_name LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            return execute_query(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Error fetching all enrollments: {e}")
            return []


class AdminCourseModel:
    """Admin course management"""
    
    @staticmethod
    def create_course(dept_id, course_number, title, description, credits):
        """Create a new course"""
        try:
            with get_db_cursor() as (conn, cursor):
                cursor.execute("""
                    INSERT INTO course (dept_id, course_number, title, description, credits, is_active)
                    VALUES (%s, %s, %s, %s, %s, 1)
                """, (dept_id, course_number, title, description, credits))
                
                course_id = cursor.lastrowid
                logger.info(f"Course created: {course_id}")
                return course_id
                
        except Exception as e:
            logger.error(f"Error creating course: {e}")
            return None
    
    @staticmethod
    def update_course(course_id, **kwargs):
        """Update course details"""
        try:
            allowed_fields = ['title', 'description', 'credits', 'is_active']
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    updates.append(f"{field} = %s")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(course_id)
            query = f"UPDATE course SET {', '.join(updates)} WHERE course_id = %s"
            
            execute_update(query, tuple(params))
            logger.info(f"Course updated: {course_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating course: {e}")
            return False
    
    @staticmethod
    def deactivate_course(course_id):
        """Deactivate a course"""
        try:
            execute_update("UPDATE course SET is_active = 0 WHERE course_id = %s", (course_id,))
            logger.info(f"Course deactivated: {course_id}")
            return True
        except Exception as e:
            logger.error(f"Error deactivating course: {e}")
            return False