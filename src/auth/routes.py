"""
OCRS Backend - Authentication Routes
User registration, login, logout, and profile management
"""

from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from src.auth.models import UserModel
from src.auth.decorators import require_auth, require_role, get_current_user
from src.utils.responses import (
    success_response, error_response, created_response,
    unauthorized_response, validation_error_response
)
from src.utils.validators import (
    validate_email_address, validate_password, validate_name,
    validate_required_fields
)
from src.utils.logger import setup_logger
from datetime import timedelta

logger = setup_logger('ocrs.auth.routes')

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user account
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - first_name
            - last_name
          properties:
            email:
              type: string
              example: student@umgc.edu
            password:
              type: string
              example: SecurePassword123!
            first_name:
              type: string
              example: John
            last_name:
              type: string
              example: Doe
            role:
              type: string
              enum: [student, faculty, admin]
              default: student
    responses:
      201:
        description: User created successfully
      400:
        description: Validation error
      409:
        description: Email already exists
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return validation_error_response({
                'missing_fields': missing
            })
        
        # Validate email
        is_valid, email_or_error = validate_email_address(data['email'])
        if not is_valid:
            return validation_error_response({'email': email_or_error})
        
        email = email_or_error
        
        # Validate password
        is_valid, error_msg = validate_password(data['password'])
        if not is_valid:
            return validation_error_response({'password': error_msg})
        
        # Validate names
        is_valid, error_msg = validate_name(data['first_name'], 'First name')
        if not is_valid:
            return validation_error_response({'first_name': error_msg})
        
        is_valid, error_msg = validate_name(data['last_name'], 'Last name')
        if not is_valid:
            return validation_error_response({'last_name': error_msg})
        
        # Get role (default: student)
        role = data.get('role', 'student')
        if role not in ['student', 'faculty', 'admin']:
            return validation_error_response({'role': 'Invalid role'})
        
        # Only admins can create non-student accounts
        # (You can add this check later when you have admin auth working)
        
        # Create user
        user = UserModel.create_user(
            email=email,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role_name=role
        )
        
        if not user:
            return error_response('Email already exists or user creation failed', 409)
        
        # Remove sensitive data
        user_data = {
            'user_id': user['user_id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'role': user['role_name'],
            'created_at': user['created_at'].isoformat() if user.get('created_at') else None
        }
        
        logger.info(f"New user registered: {email}")
        return created_response(user_data, 'User registered successfully')
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return error_response('Registration failed', 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login and receive JWT tokens
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: admin@umgc.edu
            password:
              type: string
              example: Password123!
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              type: object
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return validation_error_response({
                'message': 'Email and password are required'
            })
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Get user by email
        user = UserModel.get_user_by_email(email)
        
        if not user:
            logger.warning(f"Login attempt for non-existent user: {email}")
            return unauthorized_response('Invalid email or password')
        
        # Verify password
        if not UserModel.verify_password(password, user['password_hash']):
            logger.warning(f"Failed login attempt for: {email}")
            return unauthorized_response('Invalid email or password')
        
        # Update last login
        UserModel.update_last_login(user['user_id'])
        
        # Create JWT tokens with additional claims
        additional_claims = {
            'role': user['role_name'],
            'email': user['email']
        }
        
        access_token = create_access_token(
            identity=user['user_id'],
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=user['user_id'],
            additional_claims=additional_claims
        )
        
        # Prepare user data (without password hash)
        user_data = {
            'user_id': user['user_id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'role': user['role_name']
        }
        
        logger.info(f"User logged in: {email}")
        
        return success_response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_data
        }, 'Login successful')
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return error_response('Login failed', 500)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Token refreshed
      401:
        description: Invalid refresh token
    """
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Create new access token with same claims
        new_access_token = create_access_token(
            identity=current_user_id,
            additional_claims={
                'role': claims.get('role'),
                'email': claims.get('email')
            }
        )
        
        return success_response({
            'access_token': new_access_token
        }, 'Token refreshed successfully')
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return error_response('Token refresh failed', 500)


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_profile():
    """
    Get current authenticated user's profile
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: User profile
      401:
        description: Not authenticated
    """
    try:
        user_id = get_jwt_identity()
        user = UserModel.get_user_profile(user_id)
        
        if not user:
            return error_response('User not found', 404)
        
        return success_response(user)
        
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return error_response('Failed to get profile', 500)


@auth_bp.route('/password', methods=['PUT'])
@require_auth
def change_password():
    """
    Change user password
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - current_password
            - new_password
          properties:
            current_password:
              type: string
            new_password:
              type: string
    responses:
      200:
        description: Password changed
      400:
        description: Validation error
      401:
        description: Invalid current password
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Validate required fields
        if not data or not data.get('current_password') or not data.get('new_password'):
            return validation_error_response({
                'message': 'Current password and new password are required'
            })
        
        # Get user
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return error_response('User not found', 404)
        
        # Verify current password
        user_with_hash = UserModel.get_user_by_email(user['email'])
        if not UserModel.verify_password(data['current_password'], user_with_hash['password_hash']):
            return unauthorized_response('Current password is incorrect')
        
        # Validate new password
        is_valid, error_msg = validate_password(data['new_password'])
        if not is_valid:
            return validation_error_response({'new_password': error_msg})
        
        # Update password
        success = UserModel.update_password(user_id, data['new_password'])
        
        if not success:
            return error_response('Failed to update password', 500)
        
        logger.info(f"Password changed for user: {user['email']}")
        return success_response(message='Password changed successfully')
        
    except Exception as e:
        logger.error(f"Change password error: {e}")
        return error_response('Failed to change password', 500)


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    Logout (token invalidation handled client-side)
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Logged out successfully
    """
    # In a JWT system, logout is typically handled client-side by deleting the token
    # For server-side logout, you would need to implement a token blacklist
    
    user_id = get_jwt_identity()
    logger.info(f"User logged out: {user_id}")
    
    return success_response(message='Logged out successfully')
