"""
OCRS Backend - Faculty Models
Database operations for faculty functions
"""

from src.utils.database import execute_query, execute_update, get_db_cursor
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.faculty.models')


class FacultyModel:
    """Faculty database operations"""
    
    @staticmethod
    def get_faculty_id_from_user(user_id):
        """Get faculty profile ID from user ID"""
        try:
            result = execute_query(
                "SELECT faculty_id FROM faculty_profile WHERE user_id = %s",
                (user_id,),
                fetch_one=True
            )
            return result['faculty_id'] if result else None
        except Exception as e:
            logger.error(f"Error fetching faculty ID: {e}")
            return None
    
    @staticmethod
    def get_faculty_sections(faculty_id, term_id=None):
        """Get all sections assigned to faculty"""
        try:
            query = """
                SELECT 
                    s.section_id,
                    s.section_number,
                    s.capacity,
                    s.location,
                    s.status,
                    c.course_id,
                    c.course_number,
                    c.title as course_title,
                    c.credits,
                    d.code as dept_code,
                    t.term_id,
                    t.name as term_name,
                    t.year as term_year,
                    t.is_current,
                    COALESCE(enrolled.count, 0) as enrolled_count,
                    COALESCE(waitlist.count, 0) as waitlist_count
                FROM section s
                JOIN course c ON s.course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                JOIN term t ON s.term_id = t.term_id
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
                WHERE s.instructor_id = (
                    SELECT user_id FROM faculty_profile WHERE faculty_id = %s
                )
            """
            
            params = [faculty_id]
            
            if term_id:
                query += " AND t.term_id = %s"
                params.append(term_id)
            else:
                query += " AND t.is_current = 1"
            
            query += " ORDER BY t.year DESC, t.name, d.code, c.course_number"
            
            return execute_query(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Error fetching faculty sections: {e}")
            return []
    
    @staticmethod
    def get_section_roster(section_id, faculty_id):
        """Get roster for a specific section"""
        try:
            # First verify faculty teaches this section
            verify = execute_query("""
                SELECT s.section_id 
                FROM section s
                JOIN faculty_profile fp ON s.instructor_id = fp.user_id
                WHERE s.section_id = %s AND fp.faculty_id = %s
            """, (section_id, faculty_id), fetch_one=True)
            
            if not verify:
                return None  # Faculty doesn't teach this section
            
            query = """
                SELECT 
                    e.enrollment_id,
                    e.enrollment_status,
                    e.grade,
                    sp.student_id,
                    sp.student_number,
                    u.user_id,
                    u.email,
                    u.first_name,
                    u.last_name,
                    sp.level
                FROM enrollment e
                JOIN student_profile sp ON e.student_id = sp.student_id
                JOIN user_account u ON sp.user_id = u.user_id
                WHERE e.section_id = %s
                AND e.enrollment_status IN ('Enrolled', 'Completed')
                ORDER BY u.last_name, u.first_name
            """
            
            return execute_query(query, (section_id,))
            
        except Exception as e:
            logger.error(f"Error fetching roster: {e}")
            return []
    
    @staticmethod
    def update_grade(enrollment_id, grade, faculty_id):
        """Update student grade for an enrollment"""
        try:
            # Verify faculty teaches this section
            verify = execute_query("""
                SELECT e.enrollment_id
                FROM enrollment e
                JOIN section s ON e.section_id = s.section_id
                JOIN faculty_profile fp ON s.instructor_id = fp.user_id
                WHERE e.enrollment_id = %s AND fp.faculty_id = %s
            """, (enrollment_id, faculty_id), fetch_one=True)
            
            if not verify:
                return False
            
            # Validate grade
            valid_grades = ['A', 'B', 'C', 'D', 'F', 'P', 'NP', 'W', 'I']
            if grade not in valid_grades:
                return False
            
            execute_update(
                "UPDATE enrollment SET grade = %s WHERE enrollment_id = %s",
                (grade, enrollment_id)
            )
            
            logger.info(f"Grade updated for enrollment {enrollment_id}: {grade}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating grade: {e}")
            return False
    
    @staticmethod
    def get_section_statistics(section_id, faculty_id):
        """Get statistics for a section"""
        try:
            # Verify faculty teaches this section
            verify = execute_query("""
                SELECT s.section_id 
                FROM section s
                JOIN faculty_profile fp ON s.instructor_id = fp.user_id
                WHERE s.section_id = %s AND fp.faculty_id = %s
            """, (section_id, faculty_id), fetch_one=True)
            
            if not verify:
                return None
            
            query = """
                SELECT 
                    s.capacity,
                    COUNT(CASE WHEN e.enrollment_status = 'Enrolled' THEN 1 END) as enrolled_count,
                    COUNT(CASE WHEN e.enrollment_status = 'Dropped' THEN 1 END) as dropped_count,
                    COUNT(CASE WHEN e.enrollment_status = 'Completed' THEN 1 END) as completed_count,
                    COUNT(CASE WHEN e.grade = 'A' THEN 1 END) as grade_a,
                    COUNT(CASE WHEN e.grade = 'B' THEN 1 END) as grade_b,
                    COUNT(CASE WHEN e.grade = 'C' THEN 1 END) as grade_c,
                    COUNT(CASE WHEN e.grade = 'D' THEN 1 END) as grade_d,
                    COUNT(CASE WHEN e.grade = 'F' THEN 1 END) as grade_f,
                    (SELECT COUNT(*) FROM waitlist WHERE section_id = s.section_id AND status = 'Active') as waitlist_count
                FROM section s
                LEFT JOIN enrollment e ON s.section_id = e.section_id
                WHERE s.section_id = %s
                GROUP BY s.section_id, s.capacity
            """
            
            return execute_query(query, (section_id,), fetch_one=True)
            
        except Exception as e:
            logger.error(f"Error fetching section statistics: {e}")
            return None