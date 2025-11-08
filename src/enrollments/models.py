"""
OCRS Backend - Enrollment Models
Database operations for enrollment management
"""

from src.utils.database import execute_query, execute_update, get_db_cursor
from src.utils.logger import setup_logger
from datetime import datetime

logger = setup_logger('ocrs.enrollments.models')


class EnrollmentModel:
    """Enrollment database operations"""
    
    @staticmethod
    def enroll_student(student_id, section_id):
        """
        Enroll a student in a section
        
        Args:
            student_id (int): Student profile ID
            section_id (int): Section ID
            
        Returns:
            dict: Enrollment data or None if failed
        """
        try:
            with get_db_cursor() as (conn, cursor):
                # Check if already enrolled
                cursor.execute("""
                    SELECT enrollment_id, enrollment_status 
                    FROM enrollment 
                    WHERE student_id = %s AND section_id = %s
                """, (student_id, section_id))
                
                existing = cursor.fetchone()
                if existing:
                    if existing['enrollment_status'] == 'Enrolled':
                        return {'error': 'Already enrolled in this section', 'code': 'ALREADY_ENROLLED'}
                    elif existing['enrollment_status'] == 'Dropped':
                        # Re-enroll
                        cursor.execute("""
                            UPDATE enrollment 
                            SET enrollment_status = 'Enrolled', enrollment_date = NOW()
                            WHERE enrollment_id = %s
                        """, (existing['enrollment_id'],))
                        return EnrollmentModel.get_enrollment_by_id(existing['enrollment_id'])
                
                # Check section capacity
                cursor.execute("""
                    SELECT s.capacity, s.status,
                           COALESCE(COUNT(e.enrollment_id), 0) as enrolled_count
                    FROM section s
                    LEFT JOIN enrollment e ON s.section_id = e.section_id 
                        AND e.enrollment_status = 'Enrolled'
                    WHERE s.section_id = %s
                    GROUP BY s.section_id, s.capacity, s.status
                """, (section_id,))
                
                section = cursor.fetchone()
                if not section:
                    return {'error': 'Section not found', 'code': 'SECTION_NOT_FOUND'}
                
                if section['status'] != 'Scheduled':
                    return {'error': 'Section is not available for enrollment', 'code': 'SECTION_UNAVAILABLE'}
                
                if section['enrolled_count'] >= section['capacity']:
                    return {'error': 'Section is full', 'code': 'SECTION_FULL'}
                
                # Insert enrollment
                cursor.execute("""
                    INSERT INTO enrollment (student_id, section_id, enrollment_status)
                    VALUES (%s, %s, 'Enrolled')
                """, (student_id, section_id))
                
                enrollment_id = cursor.lastrowid
                
                logger.info(f"Student {student_id} enrolled in section {section_id}")
                return EnrollmentModel.get_enrollment_by_id(enrollment_id)
                
        except Exception as e:
            logger.error(f"Error enrolling student: {e}")
            return {'error': 'Failed to enroll student', 'code': 'ENROLLMENT_FAILED'}
    
    @staticmethod
    def drop_enrollment(student_id, section_id):
        """
        Drop a student from a section
        
        Args:
            student_id (int): Student profile ID
            section_id (int): Section ID
            
        Returns:
            bool: True if successful
        """
        try:
            with get_db_cursor() as (conn, cursor):
                cursor.execute("""
                    UPDATE enrollment 
                    SET enrollment_status = 'Dropped'
                    WHERE student_id = %s AND section_id = %s 
                    AND enrollment_status = 'Enrolled'
                """, (student_id, section_id))
                
                if cursor.rowcount == 0:
                    return False
                
                logger.info(f"Student {student_id} dropped section {section_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error dropping enrollment: {e}")
            return False
    
    @staticmethod
    def get_student_enrollments(student_id, term_id=None):
        """
        Get all enrollments for a student
        
        Args:
            student_id (int): Student profile ID
            term_id (int): Optional term filter
            
        Returns:
            list: List of enrollments
        """
        try:
            query = """
                SELECT 
                    e.enrollment_id,
                    e.enrollment_date,
                    e.enrollment_status,
                    e.grade,
                    s.section_id,
                    s.section_number,
                    s.location,
                    c.course_id,
                    c.course_number,
                    c.title as course_title,
                    c.credits,
                    d.code as dept_code,
                    t.term_id,
                    t.name as term_name,
                    t.year as term_year,
                    CONCAT(u.first_name, ' ', u.last_name) as instructor_name
                FROM enrollment e
                JOIN section s ON e.section_id = s.section_id
                JOIN course c ON s.course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                JOIN term t ON s.term_id = t.term_id
                LEFT JOIN user_account u ON s.instructor_id = u.user_id
                WHERE e.student_id = %s
            """
            
            params = [student_id]
            
            if term_id:
                query += " AND s.term_id = %s"
                params.append(term_id)
            
            query += " ORDER BY t.year DESC, t.name, d.code, c.course_number"
            
            return execute_query(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Error fetching student enrollments: {e}")
            return []
    
    @staticmethod
    def get_enrollment_by_id(enrollment_id):
        """
        Get enrollment by ID
        
        Args:
            enrollment_id (int): Enrollment ID
            
        Returns:
            dict: Enrollment details or None
        """
        try:
            query = """
                SELECT 
                    e.enrollment_id,
                    e.student_id,
                    e.section_id,
                    e.enrollment_date,
                    e.enrollment_status,
                    e.grade,
                    s.section_number,
                    c.course_id,
                    c.course_number,
                    c.title as course_title,
                    c.credits,
                    d.code as dept_code
                FROM enrollment e
                JOIN section s ON e.section_id = s.section_id
                JOIN course c ON s.course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                WHERE e.enrollment_id = %s
            """
            return execute_query(query, (enrollment_id,), fetch_one=True)
            
        except Exception as e:
            logger.error(f"Error fetching enrollment: {e}")
            return None
    
    @staticmethod
    def check_schedule_conflict(student_id, section_id):
        """
        Check if enrolling in a section creates a schedule conflict
        
        Args:
            student_id (int): Student profile ID
            section_id (int): Section ID to check
            
        Returns:
            dict: Conflict information or None if no conflict
        """
        try:
            query = """
                SELECT 
                    c.title as conflicting_course,
                    s.section_number as conflicting_section,
                    ss1.day_of_week,
                    ss1.start_time,
                    ss1.end_time
                FROM section_schedule ss1
                JOIN section s ON ss1.section_id = s.section_id
                JOIN course c ON s.course_id = c.course_id
                JOIN enrollment e ON s.section_id = e.section_id
                WHERE e.student_id = %s 
                AND e.enrollment_status = 'Enrolled'
                AND EXISTS (
                    SELECT 1 
                    FROM section_schedule ss2
                    WHERE ss2.section_id = %s
                    AND ss2.day_of_week = ss1.day_of_week
                    AND (
                        (ss2.start_time < ss1.end_time AND ss2.end_time > ss1.start_time)
                    )
                )
                LIMIT 1
            """
            return execute_query(query, (student_id, section_id), fetch_one=True)
            
        except Exception as e:
            logger.error(f"Error checking schedule conflict: {e}")
            return None
    
    @staticmethod
    def check_prerequisites(student_id, course_id):
        """
        Check if student has completed prerequisites for a course
        
        Args:
            student_id (int): Student profile ID
            course_id (int): Course ID
            
        Returns:
            dict: Missing prerequisites or None if all met
        """
        try:
            query = """
                SELECT 
                    c.course_id,
                    c.title,
                    CONCAT(d.code, ' ', c.course_number) as course_code
                FROM course_prerequisite cp
                JOIN course c ON cp.prereq_course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                WHERE cp.course_id = %s
                AND NOT EXISTS (
                    SELECT 1 
                    FROM enrollment e
                    JOIN section s ON e.section_id = s.section_id
                    WHERE e.student_id = %s
                    AND s.course_id = cp.prereq_course_id
                    AND e.enrollment_status = 'Enrolled'
                    AND (e.grade IS NULL OR e.grade IN ('A', 'B', 'C', 'D', 'P'))
                )
            """
            missing = execute_query(query, (course_id, student_id))
            
            if missing:
                return {
                    'has_prerequisites': True,
                    'prerequisites_met': False,
                    'missing_prerequisites': missing
                }
            
            # Check if course has any prerequisites
            prereq_check = execute_query(
                "SELECT COUNT(*) as count FROM course_prerequisite WHERE course_id = %s",
                (course_id,),
                fetch_one=True
            )
            
            return {
                'has_prerequisites': prereq_check['count'] > 0,
                'prerequisites_met': True,
                'missing_prerequisites': []
            }
            
        except Exception as e:
            logger.error(f"Error checking prerequisites: {e}")
            return None
    
    @staticmethod
    def get_student_credit_hours(student_id, term_id):
        """
        Get total credit hours for a student in a term
        
        Args:
            student_id (int): Student profile ID
            term_id (int): Term ID
            
        Returns:
            float: Total credit hours
        """
        try:
            query = """
                SELECT COALESCE(SUM(c.credits), 0) as total_credits
                FROM enrollment e
                JOIN section s ON e.section_id = s.section_id
                JOIN course c ON s.course_id = c.course_id
                WHERE e.student_id = %s 
                AND s.term_id = %s
                AND e.enrollment_status = 'Enrolled'
            """
            result = execute_query(query, (student_id, term_id), fetch_one=True)
            return float(result['total_credits']) if result else 0.0
            
        except Exception as e:
            logger.error(f"Error getting credit hours: {e}")
            return 0.0


class WaitlistModel:
    """Waitlist database operations"""
    
    @staticmethod
    def add_to_waitlist(student_id, section_id):
        """
        Add student to section waitlist
        
        Args:
            student_id (int): Student profile ID
            section_id (int): Section ID
            
        Returns:
            dict: Waitlist entry or None
        """
        try:
            with get_db_cursor() as (conn, cursor):
                # Check if already on waitlist
                cursor.execute("""
                    SELECT waitlist_id 
                    FROM waitlist 
                    WHERE student_id = %s AND section_id = %s AND status = 'Active'
                """, (student_id, section_id))
                
                if cursor.fetchone():
                    return {'error': 'Already on waitlist', 'code': 'ALREADY_ON_WAITLIST'}
                
                # Get current waitlist position
                cursor.execute("""
                    SELECT COUNT(*) as position 
                    FROM waitlist 
                    WHERE section_id = %s AND status = 'Active'
                """, (section_id,))
                
                position = cursor.fetchone()['position'] + 1
                
                # Insert waitlist entry
                cursor.execute("""
                    INSERT INTO waitlist (student_id, section_id, position, status)
                    VALUES (%s, %s, %s, 'Active')
                """, (student_id, section_id, position))
                
                waitlist_id = cursor.lastrowid
                
                logger.info(f"Student {student_id} added to waitlist for section {section_id} at position {position}")
                
                return {
                    'waitlist_id': waitlist_id,
                    'position': position,
                    'status': 'Active'
                }
                
        except Exception as e:
            logger.error(f"Error adding to waitlist: {e}")
            return {'error': 'Failed to add to waitlist', 'code': 'WAITLIST_FAILED'}
    
    @staticmethod
    def get_student_waitlists(student_id):
        """
        Get all waitlist entries for a student
        
        Args:
            student_id (int): Student profile ID
            
        Returns:
            list: Waitlist entries
        """
        try:
            query = """
                SELECT 
                    w.waitlist_id,
                    w.position,
                    w.status,
                    w.added_date,
                    s.section_id,
                    s.section_number,
                    c.title as course_title,
                    CONCAT(d.code, ' ', c.course_number) as course_code
                FROM waitlist w
                JOIN section s ON w.section_id = s.section_id
                JOIN course c ON s.course_id = c.course_id
                JOIN department d ON c.dept_id = d.dept_id
                WHERE w.student_id = %s AND w.status = 'Active'
                ORDER BY w.added_date
            """
            return execute_query(query, (student_id,))
            
        except Exception as e:
            logger.error(f"Error fetching waitlists: {e}")
            return []
