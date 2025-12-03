"""
OCRS Backend - Authentication Routes
API endpoints for user authentication
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.auth.models import UserModel
from src.auth.utils import generate_tokens, format_user_response
from src.auth.decorators import require_auth
from src.utils.responses import (
    success_response, error_response, created_response,
    validation_error_response, unauthorized_response
)
from src.utils.validators import (
    validate_email_address, validate_password, validate_name,
    validate_required_fields
)
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.auth.routes')

# Create Blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
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
              example: student
              enum: [student, faculty, admin]
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
        
        # Extract data
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        role = data.get('role', 'student').lower()
        
        # Validate email
        is_valid, result = validate_email_address(email)
        if not is_valid:
            return validation_error_response({'email': result})
        email = result  # Use normalized email
        
        # Validate password
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return validation_error_response({'password': error_msg})
        
        # Validate names
        is_valid, error_msg = validate_name(first_name, "First name")
        if not is_valid:
            return validation_error_response({'first_name': error_msg})
        
        is_valid, error_msg = validate_name(last_name, "Last name")
        if not is_valid:
            return validation_error_response({'last_name': error_msg})
        
        # Validate role
        valid_roles = ['student', 'faculty', 'admin']
        if role not in valid_roles:
            return validation_error_response({
                'role': f"Role must be one of: {', '.join(valid_roles)}"
            })
        
        # Check if email already exists
        if UserModel.email_exists(email):
            return error_response("Email already registered", 409)
        
        # Create user
        user = UserModel.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role_name=role
        )
        
        if not user:
            return error_response("Failed to create user", 500)
        
        # Format response
        user_data = format_user_response(user)
        
        logger.info(f"User registered: {email}")
        
        return created_response(
            data=user_data,
            message="User registered successfully"
        )
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return error_response("An error occurred during registration", 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
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
      400:
        description: Validation error
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password']
        is_valid, missing = validate_required_fields(data, required_fields)
        
        if not is_valid:
            return validation_error_response({
                'missing_fields': missing
            })
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Get user
        user = UserModel.get_user_by_email(email)
        
        if not user:
            return unauthorized_response("Invalid email or password")
        
        # Check if user is active
        if not user.get('is_active'):
            return unauthorized_response("Account is inactive")
        
        # Verify password
        if not UserModel.verify_password(password, user['password_hash']):
            return unauthorized_response("Invalid email or password")
        
        # Update last login
        UserModel.update_last_login(user['user_id'])
        
        # Generate tokens
        tokens = generate_tokens(user['user_id'], user['role_name'])
        
        if not tokens:
            return error_response("Failed to generate authentication tokens", 500)
        
        # Format user data
        user_data = format_user_response(user)
        
        logger.info(f"User logged in: {email}")
        
        return success_response(
            data={
                'user': user_data,
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token']
            },
            message="Login successful"
        )
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return error_response("An error occurred during login", 500)


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """
    Get current user information
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: User information
      401:
        description: Unauthorized
    """
    try:
        user_id = int(get_jwt_identity())
        
        user = UserModel.get_user_by_id(user_id)
        
        if not user:
            return error_response("User not found", 404)
        
        user_data = format_user_response(user)
        
        return success_response(data=user_data)
        
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        return error_response("An error occurred", 500)


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    User logout
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Logout successful
      401:
        description: Unauthorized
    """
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        
        logger.info(f"User logged out: user_id={user_id}")
        
        return success_response(message="Logout successful")
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return error_response("An error occurred during logout", 500)


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
        description: Password changed successfully
      400:
        description: Validation error
      401:
        description: Invalid current password
    """
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['current_password', 'new_password']
        is_valid, missing = validate_required_fields(data, required_fields)
        
        if not is_valid:
            return validation_error_response({'missing_fields': missing})
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Validate new password
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            return validation_error_response({'new_password': error_msg})
        
        # Get user
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return error_response("User not found", 404)
        
        # Get full user with password hash
        user_with_pass = UserModel.get_user_by_email(user['email'])
        
        # Verify current password
        if not UserModel.verify_password(current_password, user_with_pass['password_hash']):
            return unauthorized_response("Current password is incorrect")
        
        # Update password
        if UserModel.update_password(user_id, new_password):
            logger.info(f"Password changed for user_id: {user_id}")
            return success_response(message="Password changed successfully")
        else:
            return error_response("Failed to update password", 500)
        
    except Exception as e:
        logger.error(f"Password change error: {e}")
        return error_response("An error occurred", 500)