"""
API endpoint tests
"""

import pytest


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_root_endpoint(self, client):
        """Test / endpoint"""
        response = client.get('/')
        assert response.status_code == 200


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_login_success(self, client):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'email': 'admin@umgc.edu',
            'password': 'Password123!'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'access_token' in data['data']
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'email': 'admin@umgc.edu',
            'password': 'WrongPassword'
        })
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    def test_register_new_user(self, client):
        """Test user registration"""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@student.umgc.edu',
            'password': 'NewPassword123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        })
        # May get 409 if user exists from previous test
        assert response.status_code in [201, 409]
    
    def test_get_current_user(self, client, student_token):
        """Test /me endpoint"""
        response = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {student_token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'user_id' in data['data']


class TestCourseEndpoints:
    """Test course endpoints"""
    
    def test_get_all_courses(self, client):
        """Test getting all courses"""
        response = client.get('/api/courses/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'courses' in data['data']
    
    def test_get_course_by_id(self, client):
        """Test getting specific course"""
        response = client.get('/api/courses/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'course_id' in data['data']
    
    def test_search_courses(self, client):
        """Test course search"""
        response = client.get('/api/courses/search?q=programming')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_get_departments(self, client):
        """Test getting all departments"""
        response = client.get('/api/courses/departments')
        assert response.status_code == 200
        data = response.get_json()
        assert 'departments' in data['data']


class TestEnrollmentEndpoints:
    """Test enrollment endpoints"""
    
    def test_get_my_enrollments(self, client, student_token):
        """Test getting student enrollments"""
        response = client.get('/api/enrollments/my-enrollments', headers={
            'Authorization': f'Bearer {student_token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'enrollments' in data['data']
    
    def test_get_my_schedule(self, client, student_token):
        """Test getting student schedule"""
        response = client.get('/api/enrollments/my-schedule', headers={
            'Authorization': f'Bearer {student_token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_unauthorized_enrollment_access(self, client):
        """Test enrollment endpoint without token"""
        response = client.get('/api/enrollments/my-enrollments')
        assert response.status_code == 401


class TestAdminEndpoints:
    """Test admin endpoints"""
    
    def test_get_system_stats(self, client, admin_token):
        """Test admin stats endpoint"""
        response = client.get('/api/admin/stats', headers={
            'Authorization': f'Bearer {admin_token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_student_cannot_access_admin(self, client, student_token):
        """Test that students cannot access admin endpoints"""
        response = client.get('/api/admin/stats', headers={
            'Authorization': f'Bearer {student_token}'
        })
        assert response.status_code == 403


class TestFacultyEndpoints:
    """Test faculty endpoints"""
    
    def test_get_faculty_sections(self, client, faculty_token):
        """Test getting faculty sections"""
        response = client.get('/api/faculty/my-sections', headers={
            'Authorization': f'Bearer {faculty_token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'sections' in data['data']
    
    def test_student_cannot_access_faculty(self, client, student_token):
        """Test that students cannot access faculty endpoints"""
        response = client.get('/api/faculty/my-sections', headers={
            'Authorization': f'Bearer {student_token}'
        })
        assert response.status_code == 403