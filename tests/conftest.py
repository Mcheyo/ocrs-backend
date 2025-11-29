"""
Test configuration and fixtures
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import create_app
from src.utils.database import DatabaseConnection


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def admin_token(client):
    """Get admin authentication token"""
    response = client.post('/api/auth/login', json={
        'email': 'admin@umgc.edu',
        'password': 'Password123!'
    })
    data = response.get_json()
    return data['data']['access_token']


@pytest.fixture
def student_token(client):
    """Get student authentication token"""
    response = client.post('/api/auth/login', json={
        'email': 'maurice.a@student.umgc.edu',
        'password': 'Password123!'
    })
    data = response.get_json()
    return data['data']['access_token']


@pytest.fixture
def faculty_token(client):
    """Get faculty authentication token"""
    response = client.post('/api/auth/login', json={
        'email': 'j.smith@umgc.edu',
        'password': 'Password123!'
    })
    data = response.get_json()
    return data['data']['access_token']