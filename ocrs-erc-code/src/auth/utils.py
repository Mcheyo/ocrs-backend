"""
OCRS Backend - Authentication Utilities
Helper functions for authentication
"""

from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.auth.utils')


def generate_tokens(user_id, role_name):
    """
    Generate JWT access and refresh tokens
    
    Args:
        user_id (int): User ID
        role_name (str): User role
        
    Returns:
        dict: Contains access_token and refresh_token
    """
    try:
        # Create additional claims
        additional_claims = {
            'role': role_name
        }
        
        # Generate tokens with user_id as identity
        access_token = create_access_token(
            identity=str(user_id),
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=str(user_id),
            additional_claims=additional_claims
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except Exception as e:
        logger.error(f"Error generating tokens: {e}")
        return None


def format_user_response(user):
    """
    Format user data for API response (remove sensitive data)
    
    Args:
        user (dict): User data from database
        
    Returns:
        dict: Formatted user data
    """
    if not user:
        return None
    
    # Remove password hash and other sensitive fields
    safe_user = {
        'user_id': user.get('user_id'),
        'email': user.get('email'),
        'first_name': user.get('first_name'),
        'last_name': user.get('last_name'),
        'role': user.get('role_name'),
        'is_active': bool(user.get('is_active')),
        'created_at': str(user.get('created_at')) if user.get('created_at') else None
    }
    
    return safe_user