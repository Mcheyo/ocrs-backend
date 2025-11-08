"""
OCRS Backend - Authorization Decorators
JWT token validation and role-based access control
"""

from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from src.utils.responses import unauthorized_response, forbidden_response
from src.utils.logger import setup_logger
from src.auth.models import UserModel

logger = setup_logger('ocrs.auth.decorators')


def require_auth(fn):
    """
    Decorator to require valid JWT token
    
    Usage:
        @require_auth
        def protected_route():
            user_id = get_jwt_identity()
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Authentication failed: {e}")
            return unauthorized_response("Invalid or missing authentication token")
    
    return wrapper


def require_role(*allowed_roles):
    """
    Decorator to require specific role(s)
    
    Usage:
        @require_role('admin')
        def admin_only_route():
            ...
        
        @require_role('admin', 'faculty')
        def admin_or_faculty_route():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                # Get user info from token
                claims = get_jwt()
                user_role = claims.get('role')
                
                # Check if user has required role
                if user_role not in allowed_roles:
                    logger.warning(
                        f"Access denied: user role '{user_role}' not in {allowed_roles}"
                    )
                    return forbidden_response(
                        f"This action requires one of the following roles: {', '.join(allowed_roles)}"
                    )
                
                return fn(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Authorization error: {e}")
                return unauthorized_response("Invalid authentication token")
        
        return wrapper
    return decorator


def get_current_user():
    """
    Get current authenticated user from JWT token
    
    Returns:
        dict: User info or None
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return UserModel.get_user_by_id(user_id)
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        return None


def require_self_or_role(*allowed_roles):
    """
    Decorator to require user is accessing their own data OR has specific role
    
    Usage:
        @require_self_or_role('admin')
        def get_user_data(user_id):
            # User can access their own data, or admin can access any
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                current_user_id = get_jwt_identity()
                claims = get_jwt()
                user_role = claims.get('role')
                
                # Get target user_id from kwargs
                target_user_id = kwargs.get('user_id')
                
                # Allow if user is accessing their own data
                if current_user_id == target_user_id:
                    return fn(*args, **kwargs)
                
                # Allow if user has required role
                if user_role in allowed_roles:
                    return fn(*args, **kwargs)
                
                logger.warning(
                    f"Access denied: user {current_user_id} cannot access data for user {target_user_id}"
                )
                return forbidden_response("You don't have permission to access this resource")
                
            except Exception as e:
                logger.error(f"Authorization error: {e}")
                return unauthorized_response("Invalid authentication token")
        
        return wrapper
    return decorator