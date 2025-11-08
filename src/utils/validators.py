"""
OCRS Backend - Validation Utilities
Input validation and sanitization functions
"""

import re
from email_validator import validate_email, EmailNotValidError
from config.config import get_config

config = get_config()


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_password(password):
    """
    Validate password against security requirements
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < config.PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {config.PASSWORD_MIN_LENGTH} characters"
    
    if config.PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if config.PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if config.PASSWORD_REQUIRE_DIGITS and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if config.PASSWORD_REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def validate_email_address(email):
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, normalized_email or error_message)
    """
    if not email:
        return False, "Email is required"
    
    try:
        # Validate and normalize email
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)


def validate_name(name, field_name="Name"):
    """
    Validate person name
    
    Args:
        name (str): Name to validate
        field_name (str): Field name for error messages
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not name:
        return False, f"{field_name} is required"
    
    if len(name) < 2:
        return False, f"{field_name} must be at least 2 characters"
    
    if len(name) > 80:
        return False, f"{field_name} must not exceed 80 characters"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s'-]+$", name):
        return False, f"{field_name} contains invalid characters"
    
    return True, ""


def validate_student_number(student_number):
    """
    Validate student number format
    
    Args:
        student_number (str): Student number to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not student_number:
        return False, "Student number is required"
    
    # Format: S followed by 7 digits (e.g., S2025001)
    if not re.match(r'^S\d{7}$', student_number):
        return False, "Invalid student number format (must be S followed by 7 digits)"
    
    return True, ""


def validate_course_number(course_number):
    """
    Validate course number format
    
    Args:
        course_number (str): Course number to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not course_number:
        return False, "Course number is required"
    
    # Format: 3-4 digits
    if not re.match(r'^\d{3,4}$', course_number):
        return False, "Invalid course number format (must be 3-4 digits)"
    
    return True, ""


def validate_credits(credits):
    """
    Validate course credits
    
    Args:
        credits (float): Credits to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        credits = float(credits)
    except (TypeError, ValueError):
        return False, "Credits must be a number"
    
    if credits <= 0:
        return False, "Credits must be greater than 0"
    
    if credits > 9:
        return False, "Credits cannot exceed 9"
    
    # Allow only .0 or .5 decimals
    if credits % 0.5 != 0:
        return False, "Credits must be in 0.5 increments"
    
    return True, ""


def validate_section_number(section_number):
    """
    Validate section number format
    
    Args:
        section_number (str): Section number to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not section_number:
        return False, "Section number is required"
    
    # Format: 4 digits (e.g., 0101)
    if not re.match(r'^\d{4}$', section_number):
        return False, "Invalid section number format (must be 4 digits)"
    
    return True, ""


def validate_capacity(capacity):
    """
    Validate section capacity
    
    Args:
        capacity (int): Capacity to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        capacity = int(capacity)
    except (TypeError, ValueError):
        return False, "Capacity must be an integer"
    
    if capacity <= 0:
        return False, "Capacity must be greater than 0"
    
    if capacity > 500:
        return False, "Capacity cannot exceed 500"
    
    return True, ""


def validate_year(year):
    """
    Validate year
    
    Args:
        year (int): Year to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        year = int(year)
    except (TypeError, ValueError):
        return False, "Year must be an integer"
    
    if year < 2000 or year > 2100:
        return False, "Year must be between 2000 and 2100"
    
    return True, ""


def validate_time(time_str):
    """
    Validate time format (HH:MM:SS)
    
    Args:
        time_str (str): Time string to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not time_str:
        return False, "Time is required"
    
    if not re.match(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$', time_str):
        return False, "Invalid time format (must be HH:MM:SS)"
    
    return True, ""


def validate_day_of_week(day):
    """
    Validate day of week
    
    Args:
        day (str): Day of week to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    if day not in valid_days:
        return False, f"Invalid day of week (must be one of: {', '.join(valid_days)})"
    
    return True, ""


def sanitize_string(value, max_length=None):
    """
    Sanitize string input
    
    Args:
        value (str): String to sanitize
        max_length (int): Maximum length
        
    Returns:
        str: Sanitized string
    """
    if value is None:
        return None
    
    # Convert to string and strip whitespace
    value = str(value).strip()
    
    # Truncate if needed
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present
    
    Args:
        data (dict): Data to validate
        required_fields (list): List of required field names
        
    Returns:
        tuple: (bool, list) - (is_valid, missing_fields)
    """
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    return len(missing_fields) == 0, missing_fields


def validate_enum(value, valid_values, field_name="Value"):
    """
    Validate that value is in list of valid values
    
    Args:
        value: Value to validate
        valid_values (list): List of valid values
        field_name (str): Field name for error messages
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if value not in valid_values:
        return False, f"{field_name} must be one of: {', '.join(map(str, valid_values))}"
    
    return True, ""