"""
Test Script for Occamy Field Operations System
Run this to verify that the system is working correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")
    try:
        import flask
        print("✓ Flask installed")
    except ImportError:
        print("✗ Flask not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import flask_sqlalchemy
        print("✓ Flask-SQLAlchemy installed")
    except ImportError:
        print("✗ Flask-SQLAlchemy not installed")
        return False
    
    try:
        import flask_login
        print("✓ Flask-Login installed")
    except ImportError:
        print("✗ Flask-Login not installed")
        return False
    
    try:
        import werkzeug
        print("✓ Werkzeug installed")
    except ImportError:
        print("✗ Werkzeug not installed")
        return False
    
    return True

def test_app_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'templates/login.html',
        'templates/admin_dashboard.html',
        'templates/field_dashboard.html'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist

def test_database():
    """Test if database can be created"""
    print("\nTesting database...")
    try:
        from app import app, db, User
        with app.app_context():
            # Try to query users
            users = User.query.all()
            print(f"✓ Database accessible ({len(users)} users found)")
            
            # Check if admin exists
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("✓ Default admin account exists")
            else:
                print("⚠ Default admin not found (will be created on first run)")
            
            return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_routes():
    """Test if main routes are accessible"""
    print("\nTesting routes...")
    try:
        from app import app
        with app.test_client() as client:
            # Test login page
            response = client.get('/')
            if response.status_code == 302:  # Redirect to login
                print("✓ Root route accessible")
            else:
                print(f"⚠ Root route returned status {response.status_code}")
            
            # Test login page directly
            response = client.get('/login')
            if response.status_code == 200:
                print("✓ Login page accessible")
            else:
                print(f"✗ Login page returned status {response.status_code}")
            
            return True
    except Exception as e:
        print(f"✗ Route error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Occamy Field Operations - System Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Package Imports", test_imports),
        ("File Structure", test_app_structure),
        ("Database", test_database),
        ("Routes", test_routes)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with error: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed! System is ready to use.")
        print()
        print("Next steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Login: admin / admin123")
        print()
        print("Optional: Run 'python create_demo_data.py' to add sample data")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print()
        print("Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Ensure all files are present")
        print("3. Check that you're in the correct directory")
    
    print("=" * 60)
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
