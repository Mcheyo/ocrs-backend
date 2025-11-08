"""
OCRS Backend - Response Utilities
Standardized API response formatting
"""

from flask import jsonify
from datetime import datetime


def success_response(data=None, message=None, status_code=200):
    """
    Create a successful response
    
    Args:
        data: Response data
        message (str): Success message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': True,
        'timestamp': datetime.utcnow().isoformat(),
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message, status_code=400, errors=None):
    """
    Create an error response
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        errors (dict/list): Detailed error information
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': False,
        'timestamp': datetime.utcnow().isoformat(),
        'error': {
            'message': message,
            'code': status_code
        }
    }
    
    if errors:
        response['error']['details'] = errors
    
    return jsonify(response), status_code


def validation_error_response(errors):
    """
    Create a validation error response
    
    Args:
        errors (dict/list): Validation errors
        
    Returns:
        tuple: (response, status_code)
    """
    return error_response(
        message='Validation failed',
        status_code=422,
        errors=errors
    )


def not_found_response(resource='Resource'):
    """
    Create a not found response
    
    Args:
        resource (str): Resource name
        
    Returns:
        tuple: (response, status_code)
    """
    return error_response(
        message=f'{resource} not found',
        status_code=404
    )


def unauthorized_response(message='Unauthorized'):
    """
    Create an unauthorized response
    
    Args:
        message (str): Error message
        
    Returns:
        tuple: (response, status_code)
    """
    return error_response(
        message=message,
        status_code=401
    )


def forbidden_response(message='Forbidden'):
    """
    Create a forbidden response
    
    Args:
        message (str): Error message
        
    Returns:
        tuple: (response, status_code)
    """
    return error_response(
        message=message,
        status_code=403
    )


def conflict_response(message='Resource conflict'):
    """
    Create a conflict response
    
    Args:
        message (str): Error message
        
    Returns:
        tuple: (response, status_code)
    """
    return error_response(
        message=message,
        status_code=409
    )


def server_error_response(message='Internal server error'):
    """
    Create a server error response
    
    Args:
        message (str): Error message
        
    Returns:
        tuple: (response, status_code)
    """
    return error_response(
        message=message,
        status_code=500
    )


def created_response(data=None, message='Resource created successfully'):
    """
    Create a resource created response
    
    Args:
        data: Created resource data
        message (str): Success message
        
    Returns:
        tuple: (response, status_code)
    """
    return success_response(data=data, message=message, status_code=201)


def paginated_response(items, page, per_page, total):
    """
    Create a paginated response
    
    Args:
        items (list): List of items for current page
        page (int): Current page number
        per_page (int): Items per page
        total (int): Total number of items
        
    Returns:
        tuple: (response, status_code)
    """
    total_pages = (total + per_page - 1) // per_page
    
    data = {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }
    
    return success_response(data=data)