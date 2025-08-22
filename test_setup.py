#!/usr/bin/env python3
"""
Test script to validate database connection and setup
"""

import psycopg2
import configparser
import sys

def test_database_connection():
    """Test database connection and table setup"""
    try:
        # Load configuration
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Test connection
        print("🔍 Testing database connection...")
        connection = psycopg2.connect(
            host=config['postgresql']['host'],
            port=config['postgresql']['port'],
            dbname=config['postgresql']['dbname'],
            user=config['postgresql']['user'],
            password=config['postgresql']['password']
        )
        
        print("✅ Database connection successful!")
        
        # Test table existence
        cursor = connection.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'job_listings'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("✅ job_listings table exists")
            
            # Check table structure
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'job_listings'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print("📋 Table structure:")
            for col_name, col_type in columns:
                print(f"   - {col_name}: {col_type}")
                
        else:
            print("⚠️ job_listings table does not exist - will be created on first run")
        
        # Check existing data
        cursor.execute("SELECT COUNT(*) FROM job_listings;")
        job_count = cursor.fetchone()[0]
        print(f"📊 Current jobs in database: {job_count}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Database setup validation complete!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("🔍 Testing Python dependencies...")
    
    required_modules = [
        'requests',
        'psycopg2',
        'selenium',
        'webdriver_manager',
        'brotli'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ Missing modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed!")
        return True

def main():
    """Run all tests"""
    print("🚀 Running setup validation tests")
    print("=" * 40)
    
    deps_ok = test_dependencies()
    print()
    
    if deps_ok:
        db_ok = test_database_connection()
        
        if db_ok:
            print("\n🎉 All tests passed! Ready to run scraper.py")
            sys.exit(0)
        else:
            print("\n❌ Database setup needs attention")
            sys.exit(1)
    else:
        print("\n❌ Install missing dependencies first")
        sys.exit(1)

if __name__ == "__main__":
    main()
