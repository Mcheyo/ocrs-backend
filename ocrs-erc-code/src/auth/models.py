"""
OCRS Backend - Authentication Models
Database operations for user authentication
"""

from src.utils.database import execute_query, execute_update, get_db_cursor
from src.utils.logger import setup_logger
import bcrypt
from datetime import datetime

logger = setup_logger('ocrs.auth.models')


class UserModel:
    """User authentication database operations"""
    
    @staticmethod
    def create_user(email, password, first_name, last_name, role_name='student'):
        """
        Create a new user account
        
        Args:
            email (str): User email
            password (str): Plain text password (will be hashed)
            first_name (str): First name
            last_name (str): Last name
            role_name (str): Role name ('student', 'faculty', 'admin')
            
        Returns:
            dict: Created user data or None if failed
        """
        try:
            # Hash the password
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            with get_db_cursor() as (conn, cursor):
                # Get role_id
                cursor.execute(
                    "SELECT role_id FROM role WHERE role_name = %s",
                    (role_name,)
                )
                role = cursor.fetchone()
                
                if not role:
                    logger.error(f"Role '{role_name}' not found")
                    return None
                
                role_id = role['role_id']
                
                # Insert user
                cursor.execute("""
                    INSERT INTO user_account 
                    (role_id, email, password_hash, first_name, last_name)
                    VALUES (%s, %s, %s, %s, %s)
                """, (role_id, email, password_hash, first_name, last_name))
                
                user_id = cursor.lastrowid
                
                # Get created user
                cursor.execute("""
                    SELECT u.user_id, u.email, u.first_name, u.last_name, 
                           u.is_active, r.role_name, u.created_at
                    FROM user_account u
                    JOIN role r ON u.role_id = r.role_id
                    WHERE u.user_id = %s
                """, (user_id,))
                
                user = cursor.fetchone()
                logger.info(f"User created: {email}")
                return user
                
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        
        Args:
            email (str): User email
            
        Returns:
            dict: User data or None
        """
        try:
            query = """
                SELECT u.user_id, u.email, u.password_hash, u.first_name, 
                       u.last_name, u.is_active, r.role_name, u.created_at
                FROM user_account u
                JOIN role r ON u.role_id = r.role_id
                WHERE u.email = %s
            """
            return execute_query(query, (email,), fetch_one=True)
        except Exception as e:
            logger.error(f"Error fetching user by email: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: User data or None
        """
        try:
            query = """
                SELECT u.user_id, u.email, u.first_name, u.last_name, 
                       u.is_active, r.role_name, u.created_at
                FROM user_account u
                JOIN role r ON u.role_id = r.role_id
                WHERE u.user_id = %s
            """
            return execute_query(query, (user_id,), fetch_one=True)
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            return None
    
    @staticmethod
    def verify_password(plain_password, password_hash):
        """
        Verify password against hash
        
        Args:
            plain_password (str): Plain text password
            password_hash (str): Bcrypt hashed password
            
        Returns:
            bool: True if password matches
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    @staticmethod
    def update_last_login(user_id):
        """
        Update user's last login timestamp
        
        Args:
            user_id (int): User ID
            
        Returns:
            bool: True if successful
        """
        try:
            query = "UPDATE user_account SET last_login = NOW() WHERE user_id = %s"
            execute_update(query, (user_id,))
            return True
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False
    
    @staticmethod
    def update_password(user_id, new_password):
        """
        Update user password
        
        Args:
            user_id (int): User ID
            new_password (str): New plain text password
            
        Returns:
            bool: True if successful
        """
        try:
            # Hash the new password
            password_hash = bcrypt.hashpw(
                new_password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            
            query = "UPDATE user_account SET password_hash = %s WHERE user_id = %s"
            execute_update(query, (password_hash, user_id))
            logger.info(f"Password updated for user_id: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            return False
    
    @staticmethod
    def email_exists(email):
        """
        Check if email already exists
        
        Args:
            email (str): Email to check
            
        Returns:
            bool: True if email exists
        """
        try:
            query = "SELECT COUNT(*) as count FROM user_account WHERE email = %s"
            result = execute_query(query, (email,), fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            logger.error(f"Error checking email existence: {e}")
            return False