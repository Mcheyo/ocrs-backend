"""
OCRS Backend - Database Connection Module
Manages MySQL database connections and operations
"""

import mysql.connector
from mysql.connector import Error, pooling
from contextlib import contextmanager
import logging
from config.config import get_config

logger = logging.getLogger(__name__)

# Get configuration
config = get_config()


class DatabaseConnection:
    """Singleton database connection manager"""
    
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance
    
    def _initialize_pool(self):
        """Initialize database connection pool"""
        try:
            self._connection_pool = pooling.MySQLConnectionPool(
                pool_name="ocrs_pool",
                pool_size=10,
                pool_reset_session=True,
                **config.DB_CONFIG
            )
            logger.info("Database connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error initializing database connection pool: {e}")
            raise
    
    def get_connection(self):
        """
        Get a connection from the pool
        
        Returns:
            mysql.connector.connection.MySQLConnection: Database connection
        """
        try:
            return self._connection_pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
    
    @contextmanager
    def get_cursor(self, dictionary=True, buffered=True):
        """
        Context manager for database cursor
        
        Args:
            dictionary (bool): Return rows as dictionaries
            buffered (bool): Buffer results
            
        Yields:
            tuple: (connection, cursor)
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=dictionary, buffered=buffered)
            yield connection, cursor
            connection.commit()
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


# Global database instance
db = DatabaseConnection()


@contextmanager
def get_db_cursor(dictionary=True, buffered=True):
    """
    Convenient context manager for database operations
    
    Args:
        dictionary (bool): Return rows as dictionaries
        buffered (bool): Buffer results
        
    Yields:
        tuple: (connection, cursor)
        
    Example:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    with db.get_cursor(dictionary=dictionary, buffered=buffered) as (conn, cursor):
        yield conn, cursor


def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """
    Execute a SELECT query and return results
    
    Args:
        query (str): SQL query
        params (tuple/dict): Query parameters
        fetch_one (bool): Fetch only one result
        fetch_all (bool): Fetch all results
        
    Returns:
        dict/list: Query results
    """
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return None
    except Error as e:
        logger.error(f"Query execution error: {e}")
        raise


def execute_update(query, params=None):
    """
    Execute an INSERT, UPDATE, or DELETE query
    
    Args:
        query (str): SQL query
        params (tuple/dict): Query parameters
        
    Returns:
        int: Number of affected rows or last inserted ID
    """
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute(query, params or ())
            
            # Return last inserted ID for INSERT operations
            if cursor.lastrowid:
                return cursor.lastrowid
            
            # Return affected rows for UPDATE/DELETE operations
            return cursor.rowcount
    except Error as e:
        logger.error(f"Update execution error: {e}")
        raise


def execute_many(query, params_list):
    """
    Execute a query with multiple parameter sets
    
    Args:
        query (str): SQL query
        params_list (list): List of parameter tuples/dicts
        
    Returns:
        int: Number of affected rows
    """
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.executemany(query, params_list)
            return cursor.rowcount
    except Error as e:
        logger.error(f"Batch execution error: {e}")
        raise


def test_connection():
    """
    Test database connection
    
    Returns:
        bool: True if connection successful
    """
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            logger.info("Database connection test successful")
            return result is not None
    except Error as e:
        logger.error(f"Database connection test failed: {e}")
        return False


def init_database():
    """
    Initialize database with schema
    This should be run once during setup
    """
    try:
        # Read schema file
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        with get_db_cursor() as (conn, cursor):
            # Split by semicolons and execute each statement
            for statement in schema_sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        
        logger.info("Database schema initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False


def seed_database():
    """
    Seed database with initial data
    """
    try:
        # Read seed file
        with open('database/seeds/initial_data.sql', 'r') as f:
            seed_sql = f.read()
        
        # Execute seed data
        with get_db_cursor() as (conn, cursor):
            for statement in seed_sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        
        logger.info("Database seeded successfully")
        return True
    except Exception as e:
        logger.error(f"Database seeding error: {e}")
        return False


# Utility functions for common operations

def get_by_id(table, id_column, id_value):
    """
    Get a single record by ID
    
    Args:
        table (str): Table name
        id_column (str): ID column name
        id_value: ID value
        
    Returns:
        dict: Record or None
    """
    query = f"SELECT * FROM {table} WHERE {id_column} = %s"
    return execute_query(query, (id_value,), fetch_one=True)


def get_all(table, conditions=None, order_by=None, limit=None):
    """
    Get all records from a table with optional filtering
    
    Args:
        table (str): Table name
        conditions (str): WHERE clause (without WHERE keyword)
        order_by (str): ORDER BY clause
        limit (int): LIMIT value
        
    Returns:
        list: List of records
    """
    query = f"SELECT * FROM {table}"
    
    if conditions:
        query += f" WHERE {conditions}"
    
    if order_by:
        query += f" ORDER BY {order_by}"
    
    if limit:
        query += f" LIMIT {limit}"
    
    return execute_query(query, fetch_all=True)


def insert_record(table, data):
    """
    Insert a record into a table
    
    Args:
        table (str): Table name
        data (dict): Column-value pairs
        
    Returns:
        int: Inserted record ID
    """
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    return execute_update(query, tuple(data.values()))


def update_record(table, id_column, id_value, data):
    """
    Update a record in a table
    
    Args:
        table (str): Table name
        id_column (str): ID column name
        id_value: ID value
        data (dict): Column-value pairs to update
        
    Returns:
        int: Number of affected rows
    """
    set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
    
    params = list(data.values()) + [id_value]
    return execute_update(query, tuple(params))


def delete_record(table, id_column, id_value):
    """
    Delete a record from a table
    
    Args:
        table (str): Table name
        id_column (str): ID column name
        id_value: ID value
        
    Returns:
        int: Number of affected rows
    """
    query = f"DELETE FROM {table} WHERE {id_column} = %s"
    return execute_update(query, (id_value,))