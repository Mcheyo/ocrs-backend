"""
OCRS Backend - Authorization Decorators
Decorators for protecting routes and checking permissions
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from src.utils.responses import error_response, forbidden_response
from src.utils.logger import setup_logger

logger = setup_logger('ocrs.auth.decorators')


def require_auth(fn):
    """
    Decorator to require authentication
    
    Usage:
        @require_auth
        def protected_route():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Authentication failed: {e}")
            return error_response("Authentication required", 401)
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
                claims = get_jwt()
                user_role = claims.get('role')
                
                if user_role not in allowed_roles:
                    logger.warning(
                        f"Access denied: User with role '{user_role}' "
                        f"attempted to access route requiring {allowed_roles}"
                    )
                    return forbidden_response(
                        f"This action requires one of the following roles: {', '.join(allowed_roles)}"
                    )
                
                return fn(*args, **kwargs)
            except Exception as e:
                logger.error(f"Authorization error: {e}")
                return error_response("Authorization failed", 401)
        return wrapper
    return decorator


def get_current_user():
    """
    Get current user identity from JWT token
    
    Returns:
        dict: User identity containing user_id and role
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()  # This returns the user_id (int)
        claims = get_jwt()  # This returns all claims including 'role'
        
        return {
            'user_id': user_id,
            'role': claims.get('role')
        }
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        return None