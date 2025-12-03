-- ============================================================================
-- Online Course Registration System (OCRS)
-- Seed Data - Sample Data for Development and Testing
-- Version: 1.0
-- ============================================================================

-- ============================================================================
-- 1. ROLES
-- ============================================================================
INSERT INTO role (role_name) VALUES
('student'),
('faculty'),
('admin');

-- ============================================================================
-- 2. DEPARTMENTS
-- ============================================================================
INSERT INTO department (code, name, description) VALUES
('CMSC', 'Computer Science', 'Department of Computer Science and Information Technology'),
('MATH', 'Mathematics', 'Department of Mathematics and Statistics'),
('ENG', 'English', 'Department of English and Literature'),
('HIST', 'History', 'Department of History and Social Sciences'),
('BIO', 'Biology', 'Department of Biological Sciences'),
('CHEM', 'Chemistry', 'Department of Chemistry'),
('PHYS', 'Physics', 'Department of Physics and Astronomy'),
('ECON', 'Economics', 'Department of Economics and Business');

-- ============================================================================
-- 3. TERMS
-- ============================================================================
INSERT INTO term (name, year, start_date, end_date, is_current) VALUES
('Spring', 2025, '2025-01-15', '2025-05-15', 0),
('Summer', 2025, '2025-06-01', '2025-08-15', 0),
('Fall', 2025, '2025-09-01', '2025-12-15', 1),
('Spring', 2026, '2026-01-15', '2026-05-15', 0);

-- ============================================================================
-- 4. USER ACCOUNTS
-- Password for all users: "Password123!" (bcrypt hashed)
-- ============================================================================

-- Admin Users
INSERT INTO user_account (role_id, email, password_hash, first_name, last_name) VALUES
(3, 'admin@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'System', 'Administrator'),
(3, 'chris.davis@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Christopher', 'Davis');

-- Faculty Users
INSERT INTO user_account (role_id, email, password_hash, first_name, last_name) VALUES
(2, 'j.smith@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'John', 'Smith'),
(2, 'e.johnson@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Emily', 'Johnson'),
(2, 'r.williams@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Robert', 'Williams'),
(2, 'l.brown@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Lisa', 'Brown'),
(2, 'm.davis@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Michael', 'Davis'),
(2, 's.miller@umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Sarah', 'Miller');

-- Student Users
INSERT INTO user_account (role_id, email, password_hash, first_name, last_name) VALUES
(1, 'maurice.a@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Maurice', 'Adovoekpe'),
(1, 'mansour.c@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Mansour', 'Cheyo'),
(1, 'nelvis.l@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Nelvis', 'Lumvalla'),
(1, 'sritej.n@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Sritej', 'Nadella'),
(1, 'steven.n@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Steven', 'Nguyen'),
(1, 'michael.s@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Michael', 'Sibley'),
(1, 'xu.w@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Xu', 'Wang'),
(1, 'ronell.w@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Ronell', 'Wilder'),
(1, 'alice.cooper@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Alice', 'Cooper'),
(1, 'bob.martin@student.umgc.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2Ztl3V8GgW', 'Bob', 'Martin');

-- ============================================================================
-- 5. FACULTY PROFILES
-- ============================================================================
INSERT INTO faculty_profile (user_id, employee_number, dept_id, title) VALUES
(3, 'F1001', 1, 'Professor'),
(4, 'F1002', 1, 'Associate Professor'),
(5, 'F1003', 2, 'Professor'),
(6, 'F1004', 3, 'Assistant Professor'),
(7, 'F1005', 5, 'Professor'),
(8, 'F1006', 8, 'Associate Professor');

-- ============================================================================
-- 6. STUDENT PROFILES
-- ============================================================================
INSERT INTO student_profile (user_id, student_number, dept_id, enrollment_year, level) VALUES
(9, 'S2025001', 1, 2022, 'Senior'),
(10, 'S2025002', 1, 2022, 'Senior'),
(11, 'S2025003', 1, 2023, 'Junior'),
(12, 'S2025004', 1, 2023, 'Junior'),
(13, 'S2025005', 1, 2024, 'Sophomore'),
(14, 'S2025006', 1, 2024, 'Sophomore'),
(15, 'S2025007', 2, 2024, 'Sophomore'),
(16, 'S2025008', 1, 2023, 'Junior'),
(17, 'S2025009', 8, 2025, 'Freshman'),
(18, 'S2025010', 1, 2025, 'Freshman');

-- ============================================================================
-- 7. COURSES
-- ============================================================================

-- Computer Science Courses
INSERT INTO course (dept_id, course_number, title, description, credits) VALUES
(1, '140', 'Intro to Programming', 'Introduction to programming using Python. Covers basic syntax, control structures, and problem-solving.', 3.0),
(1, '201', 'Computer Science I', 'First course in computer science using Java. Object-oriented programming fundamentals.', 3.0),
(1, '202', 'Computer Science II', 'Data structures and algorithms. Continuation of CMSC 201.', 3.0),
(1, '341', 'Data Structures', 'Advanced data structures including trees, graphs, and hash tables.', 3.0),
(1, '330', 'Advanced Programming Languages', 'Survey of programming language paradigms including functional and logic programming.', 3.0),
(1, '403', 'Database Management', 'Database design, SQL, normalization, and database implementation.', 3.0),
(1, '430', 'Software Engineering', 'Software development lifecycle, requirements analysis, design patterns, and testing.', 3.0),
(1, '451', 'Computer Networks', 'Network protocols, architectures, and internet technologies.', 3.0),
(1, '495', 'Computer Science Capstone', 'Capstone project integrating all aspects of computer science curriculum.', 3.0);

-- Mathematics Courses
INSERT INTO course (dept_id, course_number, title, description, credits) VALUES
(2, '140', 'Calculus I', 'Limits, derivatives, and introduction to integrals.', 4.0),
(2, '141', 'Calculus II', 'Integration techniques, series, and sequences.', 4.0),
(2, '240', 'Calculus III', 'Multivariable calculus and vector analysis.', 4.0),
(2, '250', 'Discrete Mathematics', 'Logic, sets, combinatorics, and graph theory.', 3.0),
(2, '307', 'Linear Algebra', 'Vector spaces, matrices, eigenvalues, and linear transformations.', 3.0);

-- English Courses
INSERT INTO course (dept_id, course_number, title, description, credits) VALUES
(3, '101', 'English Composition', 'Academic writing and critical thinking skills.', 3.0),
(3, '102', 'Literature and Composition', 'Analysis of literary works and advanced composition.', 3.0);

-- ============================================================================
-- 8. COURSE PREREQUISITES
-- ============================================================================
INSERT INTO course_prerequisite (course_id, prereq_course_id) VALUES
-- CMSC 201 requires CMSC 140
(2, 1),
-- CMSC 202 requires CMSC 201
(3, 2),
-- CMSC 341 requires CMSC 202
(4, 3),
-- CMSC 330 requires CMSC 202
(5, 3),
-- CMSC 403 requires CMSC 341
(6, 4),
-- CMSC 430 requires CMSC 330
(7, 5),
-- CMSC 451 requires CMSC 341
(8, 4),
-- CMSC 495 requires CMSC 430 and CMSC 403
(9, 7),
(9, 6),
-- MATH 141 requires MATH 140
(11, 10),
-- MATH 240 requires MATH 141
(12, 11),
-- ENG 102 requires ENG 101
(16, 15);

-- ============================================================================
-- 9. SECTIONS - Fall 2025
-- ============================================================================

-- CMSC Sections
INSERT INTO section (course_id, term_id, section_number, instructor_id, capacity, location, status) VALUES
-- CMSC 140 - Multiple sections
(1, 3, '0101', 1, 30, 'Room 201', 'Scheduled'),
(1, 3, '0102', 1, 30, 'Room 202', 'Scheduled'),
-- CMSC 201
(2, 3, '0101', 1, 25, 'Room 203', 'Scheduled'),
(2, 3, '0102', 2, 25, 'Room 204', 'Scheduled'),
-- CMSC 202
(3, 3, '0101', 1, 25, 'Room 205', 'Scheduled'),
-- CMSC 341
(4, 3, '0101', 2, 20, 'Room 206', 'Scheduled'),
-- CMSC 330
(5, 3, '0101', 1, 20, 'Room 207', 'Scheduled'),
-- CMSC 403
(6, 3, '0101', 2, 20, 'Room 208', 'Scheduled'),
-- CMSC 430
(7, 3, '0101', 1, 20, 'Room 209', 'Scheduled'),
-- CMSC 451
(8, 3, '0101', 2, 20, 'Room 210', 'Scheduled'),
-- CMSC 495 - The Capstone (small capacity for testing waitlist)
(9, 3, '0101', 1, 5, 'Room 301', 'Scheduled');

-- MATH Sections
INSERT INTO section (course_id, term_id, section_number, instructor_id, capacity, location, status) VALUES
(10, 3, '0101', 3, 35, 'Math Building 101', 'Scheduled'),
(11, 3, '0101', 3, 30, 'Math Building 102', 'Scheduled'),
(12, 3, '0101', 3, 25, 'Math Building 103', 'Scheduled'),
(13, 3, '0101', 3, 30, 'Math Building 104', 'Scheduled');

-- ENG Sections
INSERT INTO section (course_id, term_id, section_number, instructor_id, capacity, location, status) VALUES
(15, 3, '0101', 4, 25, 'Humanities 201', 'Scheduled'),
(16, 3, '0101', 4, 25, 'Humanities 202', 'Scheduled');

-- ============================================================================
-- 10. SECTION SCHEDULES
-- ============================================================================

-- CMSC 140 Section 0101 - MWF 10:00-11:00
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(1, 'Monday', '10:00:00', '11:00:00'),
(1, 'Wednesday', '10:00:00', '11:00:00'),
(1, 'Friday', '10:00:00', '11:00:00');

-- CMSC 140 Section 0102 - TTh 14:00-15:30
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(2, 'Tuesday', '14:00:00', '15:30:00'),
(2, 'Thursday', '14:00:00', '15:30:00');

-- CMSC 201 Section 0101 - MWF 11:00-12:00
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(3, 'Monday', '11:00:00', '12:00:00'),
(3, 'Wednesday', '11:00:00', '12:00:00'),
(3, 'Friday', '11:00:00', '12:00:00');

-- CMSC 201 Section 0102 - TTh 09:30-11:00
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(4, 'Tuesday', '09:30:00', '11:00:00'),
(4, 'Thursday', '09:30:00', '11:00:00');

-- CMSC 202 Section 0101 - MWF 13:00-14:00
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(5, 'Monday', '13:00:00', '14:00:00'),
(5, 'Wednesday', '13:00:00', '14:00:00'),
(5, 'Friday', '13:00:00', '14:00:00');

-- CMSC 341 Section 0101 - TTh 11:00-12:30
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(6, 'Tuesday', '11:00:00', '12:30:00'),
(6, 'Thursday', '11:00:00', '12:30:00');

-- CMSC 330 Section 0101 - MW 14:00-15:30
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(7, 'Monday', '14:00:00', '15:30:00'),
(7, 'Wednesday', '14:00:00', '15:30:00');

-- CMSC 403 Section 0101 - TTh 14:00-15:30
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(8, 'Tuesday', '14:00:00', '15:30:00'),
(8, 'Thursday', '14:00:00', '15:30:00');

-- CMSC 430 Section 0101 - MW 16:00-17:30
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(9, 'Monday', '16:00:00', '17:30:00'),
(9, 'Wednesday', '16:00:00', '17:30:00');

-- CMSC 495 Section 0101 - Th 18:00-21:00
INSERT INTO section_schedule (section_id, day_of_week, start_time, end_time) VALUES
(11, 'Thursday', '18:00:00', '21:00:00');

-- ============================================================================
-- 11. SAMPLE ENROLLMENTS
-- ============================================================================

-- Student 1 (Maurice) enrollments
INSERT INTO enrollment (student_id, section_id, enrollment_status) VALUES
(1, 9, 'Enrolled'),  -- CMSC 430
(1, 6, 'Enrolled');  -- CMSC 341

-- Student 2 (Mansour) enrollments
INSERT INTO enrollment (student_id, section_id, enrollment_status) VALUES
(2, 8, 'Enrolled'),  -- CMSC 403
(2, 7, 'Enrolled');  -- CMSC 330

-- Student 3 (Nelvis) enrollments
INSERT INTO enrollment (student_id, section_id, enrollment_status) VALUES
(3, 5, 'Enrolled'),  -- CMSC 202
(3, 18, 'Enrolled'); -- ENG 102

-- Student 4 (Sritej) enrollments
INSERT INTO enrollment (student_id, section_id, enrollment_status) VALUES
(4, 5, 'Enrolled'),  -- CMSC 202
(4, 14, 'Enrolled'); -- MATH 307

-- Fill CMSC 495 to capacity (5 students) to test waitlist
INSERT INTO enrollment (student_id, section_id, enrollment_status) VALUES
(5, 11, 'Enrolled'),  -- Steven
(6, 11, 'Enrolled'),  -- Michael
(7, 11, 'Enrolled'),  -- Xu
(8, 11, 'Enrolled'),  -- Ronell
(1, 11, 'Enrolled');  -- Maurice (5th spot - now full)

-- ============================================================================
-- 12. SYSTEM SETTINGS
-- ============================================================================
INSERT INTO system_setting (name, value) VALUES
('max_credits_per_term', '18'),
('min_credits_per_term', '12'),
('enrollment_open', 'true'),
('current_term_id', '3'),
('waitlist_enabled', 'true'),
('system_maintenance', 'false');

-- ============================================================================
-- END OF SEED DATA
-- ============================================================================