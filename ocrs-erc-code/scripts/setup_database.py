#!/usr/bin/env python3
"""
OCRS Backend - Database Setup Script
Automates database initialization and seeding
"""

import sys
import os
import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import get_config

config = get_config()


def get_mysql_connection(include_db=False):
    """Get MySQL connection"""
    try:
        conn_params = {
            'host': config.DB_CONFIG['host'],
            'user': config.DB_CONFIG['user'],
            'password': config.DB_CONFIG['password'],
            'charset': config.DB_CONFIG['charset']
        }
        
        if include_db:
            conn_params['database'] = config.DB_CONFIG['database']
        
        return mysql.connector.connect(**conn_params)
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


def create_database():
    """Create the OCRS database"""
    print("\n📦 Creating database...")
    
    conn = get_mysql_connection(include_db=False)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create database
        db_name = config.DB_CONFIG['database']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} "
                      f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"✅ Database '{db_name}' created successfully")
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def run_sql_file(filename, description):
    """Execute SQL file"""
    print(f"\n🔧 {description}...")
    
    conn = get_mysql_connection(include_db=True)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Read SQL file
        with open(filename, 'r') as f:
            sql_content = f.read()
        
        # Split and execute statements
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)
        
        conn.commit()
        print(f"✅ {description} completed successfully")
        return True
    except Error as e:
        print(f"❌ Error executing {filename}: {e}")
        conn.rollback()
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def test_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    conn = get_mysql_connection(include_db=True)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"✅ Connected to MySQL version: {version}")
        
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"✅ Using database: {db_name}")
        
        return True
    except Error as e:
        print(f"❌ Connection test failed: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def main():
    """Main setup function"""
    print("=" * 60)
    print("🎓 OCRS Backend - Database Setup")
    print("=" * 60)
    
    print("\nThis script will:")
    print("1. Create the OCRS database")
    print("2. Initialize the database schema")
    print("3. (Optional) Load seed data")
    
    # Ask for confirmation
    confirm = input("\n⚠️  This will modify your database. Continue? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Setup cancelled")
        return
    
    # Step 1: Test connection
    if not test_connection():
        print("\n❌ Setup failed: Cannot connect to MySQL")
        print("Please check your database configuration in .env file")
        return
    
    # Step 2: Create database
    if not create_database():
        print("\n❌ Setup failed: Cannot create database")
        return
    
    # Step 3: Initialize schema
    schema_file = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    if not run_sql_file(schema_file, "Initializing database schema"):
        print("\n❌ Setup failed: Cannot initialize schema")
        return
    
    # Step 4: Ask about seed data
    seed = input("\n📊 Do you want to load sample data? (yes/no): ")
    if seed.lower() in ['yes', 'y']:
        seed_file = os.path.join(os.path.dirname(__file__), '..', 'database', 'seeds', 'initial_data.sql')
        if run_sql_file(seed_file, "Loading seed data"):
            print("\n✅ Sample data loaded")
            print("\nDefault test credentials:")
            print("  Admin:   admin@umgc.edu / Password123!")
            print("  Student: maurice.a@student.umgc.edu / Password123!")
            print("  Faculty: j.smith@umgc.edu / Password123!")
    
    print("\n" + "=" * 60)
    print("✅ Database setup completed successfully!")
    print("=" * 60)
    print("\nYou can now run the application:")
    print("  python src/app.py")
    print("\nAPI Documentation will be available at:")
    print("  http://localhost:5000/api/docs")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)