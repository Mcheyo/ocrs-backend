-- ============================================================================
-- Online Course Registration System (OCRS)
-- Database Schema - MySQL 8.0+
-- Version: 1.0
-- Created: November 2025
-- Language: MySQL
-- ============================================================================

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS waitlist;
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS section_schedule;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS course_prerequisite;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS term;
DROP TABLE IF EXISTS faculty_profile;
DROP TABLE IF EXISTS student_profile;
DROP TABLE IF EXISTS user_account;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS system_setting;

-- ============================================================================
-- 1. ROLE TABLE
-- Stores user role types (student, faculty, admin)
-- ============================================================================
CREATE TABLE role (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_role_name (role_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. DEPARTMENT TABLE
-- Contains academic departments
-- ============================================================================
CREATE TABLE department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_dept_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. USER_ACCOUNT TABLE
-- Main user authentication and profile table for all users
-- ============================================================================
CREATE TABLE user_account (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE RESTRICT,
    INDEX idx_email (email),
    INDEX idx_role_id (role_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. STUDENT_PROFILE TABLE
-- Student-specific information
-- ============================================================================
CREATE TABLE student_profile (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    dept_id INT,
    enrollment_year YEAR,
    major_dept_id SMALLINT,
    level ENUM('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate') DEFAULT 'Freshman',
    FOREIGN KEY (user_id) REFERENCES user_account(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id) ON DELETE SET NULL,
    INDEX idx_student_number (student_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 5. FACULTY_PROFILE TABLE
-- Faculty-specific information
-- ============================================================================
CREATE TABLE faculty_profile (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    employee_number VARCHAR(20) NOT NULL UNIQUE,
    dept_id INT,
    title VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id) ON DELETE SET NULL,
    INDEX idx_employee_number (employee_number),
    INDEX idx_dept_id (dept_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 6. TERM TABLE
-- Academic terms/semesters
-- ============================================================================
CREATE TABLE term (
    term_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    year YEAR NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_term (name, year),
    INDEX idx_year (year),
    INDEX idx_current (is_current),
    CHECK (end_date > start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 7. COURSE TABLE
-- Course catalog
-- ============================================================================
CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_id INT NOT NULL,
    course_number VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    credits DECIMAL(3,1) NOT NULL,
    is_retired TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id) ON DELETE RESTRICT,
    UNIQUE KEY unique_course (dept_id, course_number),
    INDEX idx_course_number (course_number),
    INDEX idx_title (title),
    CHECK (credits > 0 AND credits <= 9.0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 8. COURSE_PREREQUISITE TABLE
-- Defines prerequisite relationships between courses
-- ============================================================================
CREATE TABLE course_prerequisite (
    course_id INT NOT NULL,
    prereq_course_id INT NOT NULL,
    PRIMARY KEY (course_id, prereq_course_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (prereq_course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    CHECK (course_id != prereq_course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 9. SECTION TABLE
-- Specific course offerings in a term
-- ============================================================================
CREATE TABLE section (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    term_id INT NOT NULL,
    section_number VARCHAR(10) NOT NULL,
    instructor_id INT,
    capacity SMALLINT NOT NULL,
    location VARCHAR(100),
    status ENUM('Scheduled', 'Cancelled', 'Completed') DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (term_id) REFERENCES term(term_id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES faculty_profile(faculty_id) ON DELETE SET NULL,
    UNIQUE KEY unique_section (course_id, term_id, section_number),
    INDEX idx_term (term_id),
    INDEX idx_instructor (instructor_id),
    INDEX idx_status (status),
    CHECK (capacity > 0 AND capacity <= 500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 10. SECTION_SCHEDULE TABLE
-- Meeting times for each section
-- ============================================================================
CREATE TABLE section_schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (section_id) REFERENCES section(section_id) ON DELETE CASCADE,
    INDEX idx_section (section_id),
    INDEX idx_day (day_of_week),
    CHECK (end_time > start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 11. ENROLLMENT TABLE
-- Student course enrollments
-- ============================================================================
CREATE TABLE enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    enrollment_status ENUM('Enrolled', 'Dropped', 'Completed', 'Withdrawn') DEFAULT 'Enrolled',
    grade VARCHAR(10),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student_profile(student_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES section(section_id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id, section_id),
    INDEX idx_student (student_id),
    INDEX idx_section (section_id),
    INDEX idx_status (enrollment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 12. WAITLIST TABLE
-- Waitlist for full sections
-- ============================================================================
CREATE TABLE waitlist (
    waitlist_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    student_id INT NOT NULL,
    position INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES section(section_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES student_profile(student_id) ON DELETE CASCADE,
    UNIQUE KEY unique_waitlist (section_id, student_id),
    INDEX idx_section_position (section_id, position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 13. AUDIT_LOG TABLE
-- System activity logging
-- ============================================================================
CREATE TABLE audit_log (
    audit_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(100) NOT NULL,
    object_type VARCHAR(50),
    object_id INT,
    details JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_account(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_action (action_type),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 14. SYSTEM_SETTING TABLE
-- Global system configuration
-- ============================================================================
CREATE TABLE system_setting (
    name VARCHAR(100) PRIMARY KEY,
    value VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Trigger: Auto-increment waitlist position
DELIMITER //
CREATE TRIGGER before_waitlist_insert 
BEFORE INSERT ON waitlist
FOR EACH ROW
BEGIN
    DECLARE next_position INT;
    
    SELECT COALESCE(MAX(position), 0) + 1 INTO next_position
    FROM waitlist
    WHERE section_id = NEW.section_id;
    
    SET NEW.position = next_position;
END//
DELIMITER ;

-- Trigger: Prevent enrollment over capacity
DELIMITER //
CREATE TRIGGER before_enrollment_insert
BEFORE INSERT ON enrollment
FOR EACH ROW
BEGIN
    DECLARE section_capacity INT;
    DECLARE current_enrollment INT;
    
    -- Get section capacity
    SELECT capacity INTO section_capacity
    FROM section
    WHERE section_id = NEW.section_id;
    
    -- Count current enrollments
    SELECT COUNT(*) INTO current_enrollment
    FROM enrollment
    WHERE section_id = NEW.section_id 
    AND enrollment_status = 'Enrolled';
    
    -- Check if section is full
    IF current_enrollment >= section_capacity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Section is at full capacity';
    END IF;
END//
DELIMITER ;

-- Trigger: Log enrollment actions
DELIMITER //
CREATE TRIGGER after_enrollment_insert
AFTER INSERT ON enrollment
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (user_id, action_type, object_type, object_id, details)
    SELECT u.user_id, 'ENROLLMENT_CREATE', 'enrollment', NEW.enrollment_id,
           JSON_OBJECT('section_id', NEW.section_id, 'status', NEW.enrollment_status)
    FROM student_profile sp
    JOIN user_account u ON sp.user_id = u.user_id
    WHERE sp.student_id = NEW.student_id;
END//
DELIMITER ;

-- Trigger: Log enrollment updates
DELIMITER //
CREATE TRIGGER after_enrollment_update
AFTER UPDATE ON enrollment
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (user_id, action_type, object_type, object_id, details)
    SELECT u.user_id, 'ENROLLMENT_UPDATE', 'enrollment', NEW.enrollment_id,
           JSON_OBJECT('old_status', OLD.enrollment_status, 'new_status', NEW.enrollment_status)
    FROM student_profile sp
    JOIN user_account u ON sp.user_id = u.user_id
    WHERE sp.student_id = NEW.student_id;
END//
DELIMITER ;

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Full student information
CREATE OR REPLACE VIEW vw_student_full AS
SELECT 
    u.user_id,
    u.email,
    u.first_name,
    u.last_name,
    u.is_active,
    sp.student_id,
    sp.student_number,
    sp.enrollment_year,
    sp.level,
    d.code AS dept_code,
    d.name AS dept_name
FROM user_account u
JOIN student_profile sp ON u.user_id = sp.user_id
LEFT JOIN department d ON sp.dept_id = d.dept_id
WHERE u.is_active = 1;

-- View: Course catalog with department info
CREATE OR REPLACE VIEW vw_course_catalog AS
SELECT 
    c.course_id,
    c.course_number,
    c.title,
    c.description,
    c.credits,
    d.code AS dept_code,
    d.name AS dept_name,
    c.is_retired
FROM course c
JOIN department d ON c.dept_id = d.dept_id
WHERE c.is_retired = 0;

-- View: Section details with enrollment count
CREATE OR REPLACE VIEW vw_section_details AS
SELECT 
    s.section_id,
    s.section_number,
    c.course_number,
    c.title AS course_title,
    c.credits,
    d.code AS dept_code,
    t.name AS term_name,
    t.year AS term_year,
    CONCAT(u.first_name, ' ', u.last_name) AS instructor_name,
    s.capacity,
    COUNT(e.enrollment_id) AS enrolled_count,
    s.capacity - COUNT(e.enrollment_id) AS available_seats,
    s.location,
    s.status
FROM section s
JOIN course c ON s.course_id = c.course_id
JOIN department d ON c.dept_id = d.dept_id
JOIN term t ON s.term_id = t.term_id
LEFT JOIN faculty_profile fp ON s.instructor_id = fp.faculty_id
LEFT JOIN user_account u ON fp.user_id = u.user_id
LEFT JOIN enrollment e ON s.section_id = e.section_id AND e.enrollment_status = 'Enrolled'
GROUP BY s.section_id;

-- View: Student schedule
CREATE OR REPLACE VIEW vw_student_schedule AS
SELECT 
    sp.student_id,
    e.enrollment_id,
    c.course_number,
    c.title AS course_title,
    c.credits,
    s.section_number,
    t.name AS term_name,
    t.year AS term_year,
    CONCAT(u.first_name, ' ', u.last_name) AS instructor_name,
    ss.day_of_week,
    ss.start_time,
    ss.end_time,
    s.location,
    e.enrollment_status
FROM enrollment e
JOIN student_profile sp ON e.student_id = sp.student_id
JOIN section s ON e.section_id = s.section_id
JOIN course c ON s.course_id = c.course_id
JOIN term t ON s.term_id = t.term_id
LEFT JOIN section_schedule ss ON s.section_id = ss.section_id
LEFT JOIN faculty_profile fp ON s.instructor_id = fp.faculty_id
LEFT JOIN user_account u ON fp.user_id = u.user_id
WHERE e.enrollment_status IN ('Enrolled', 'Completed');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================