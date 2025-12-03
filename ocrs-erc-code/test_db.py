import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='ocrs_user',
        password='SecurePassword123!',
        database='ocrs_db'
    )
    
    if conn.is_connected():
        print("✅ Python connection successful!")
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM user_account")
        users = cursor.fetchone()[0]
        print(f"📊 Users: {users}")
        
        cursor.execute("SELECT COUNT(*) FROM course")
        courses = cursor.fetchone()[0]
        print(f"📚 Courses: {courses}")
        
        cursor.execute("SELECT COUNT(*) FROM section")
        sections = cursor.fetchone()[0]
        print(f"🏢 Sections: {sections}")
        
        cursor.execute("SELECT email FROM user_account WHERE role_id = 3 LIMIT 1")
        admin = cursor.fetchone()[0]
        print(f"👤 Admin user: {admin}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ DATABASE SETUP COMPLETE AND VERIFIED!")
        
except Exception as e:
    print(f"❌ Error: {e}")
