"""
Unit Tests for Occamy Field Operations System
Run with: python -m pytest tests.py -v
or: python tests.py
"""

import unittest
import json
from datetime import datetime, date
from app import app, db, User, WorkLog, Meeting, Sale, SampleDistribution
from werkzeug.security import generate_password_hash

class OccamyTestCase(unittest.TestCase):
    """Base test case with setup and teardown"""
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_occamy.db'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Create test admin
            admin = User(
                username='test_admin',
                email='admin@test.com',
                password_hash=generate_password_hash('test123'),
                role='admin',
                name='Test Admin'
            )
            db.session.add(admin)
            
            # Create test field officer
            officer = User(
                username='test_officer',
                email='officer@test.com',
                password_hash=generate_password_hash('test123'),
                role='field_officer',
                name='Test Officer',
                state='Test State',
                district='Test District'
            )
            db.session.add(officer)
            db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def login(self, username, password):
        """Helper function to login"""
        return self.client.post('/login',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )
    
    def logout(self):
        """Helper function to logout"""
        return self.client.get('/logout')


class AuthenticationTests(OccamyTestCase):
    """Test authentication and authorization"""
    
    def test_login_page_loads(self):
        """Test that login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_valid_admin_login(self):
        """Test admin can login with valid credentials"""
        response = self.login('test_admin', 'test123')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['role'], 'admin')
    
    def test_valid_officer_login(self):
        """Test field officer can login with valid credentials"""
        response = self.login('test_officer', 'test123')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['role'], 'field_officer')
    
    def test_invalid_login(self):
        """Test login fails with invalid credentials"""
        response = self.login('test_admin', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
    
    def test_logout(self):
        """Test logout redirects to login"""
        self.login('test_admin', 'test123')
        response = self.logout()
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)


class AdminAPITests(OccamyTestCase):
    """Test admin API endpoints"""
    
    def test_admin_dashboard_requires_auth(self):
        """Test admin dashboard requires authentication"""
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_admin_dashboard_accessible(self):
        """Test admin can access dashboard"""
        self.login('test_admin', 'test123')
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_stats_endpoint(self):
        """Test admin stats endpoint returns data"""
        self.login('test_admin', 'test123')
        response = self.client.get('/api/admin/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('active_officers', data)
        self.assertIn('total_meetings', data)
    
    def test_admin_can_create_user(self):
        """Test admin can create new field officer"""
        self.login('test_admin', 'test123')
        user_data = {
            'username': 'new_officer',
            'email': 'new@test.com',
            'password': 'password123',
            'name': 'New Officer',
            'state': 'New State'
        }
        response = self.client.post('/api/admin/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_duplicate_username_rejected(self):
        """Test creating user with duplicate username fails"""
        self.login('test_admin', 'test123')
        user_data = {
            'username': 'test_officer',  # Already exists
            'email': 'different@test.com',
            'password': 'password123',
            'name': 'Duplicate User'
        }
        response = self.client.post('/api/admin/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_officer_cannot_access_admin_endpoints(self):
        """Test field officer cannot access admin endpoints"""
        self.login('test_officer', 'test123')
        response = self.client.get('/api/admin/stats')
        self.assertEqual(response.status_code, 403)


class FieldOfficerAPITests(OccamyTestCase):
    """Test field officer API endpoints"""
    
    def test_officer_dashboard_requires_auth(self):
        """Test officer dashboard requires authentication"""
        response = self.client.get('/field/dashboard')
        self.assertEqual(response.status_code, 302)
    
    def test_officer_dashboard_accessible(self):
        """Test officer can access their dashboard"""
        self.login('test_officer', 'test123')
        response = self.client.get('/field/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_start_work_day(self):
        """Test starting work day"""
        self.login('test_officer', 'test123')
        work_data = {
            'latitude': 26.8467,
            'longitude': 80.9462,
            'odometer': 1000
        }
        response = self.client.post('/api/field/worklog/start',
            data=json.dumps(work_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_cannot_start_work_twice(self):
        """Test cannot start work day twice"""
        self.login('test_officer', 'test123')
        work_data = {
            'latitude': 26.8467,
            'longitude': 80.9462,
            'odometer': 1000
        }
        # First start
        self.client.post('/api/field/worklog/start',
            data=json.dumps(work_data),
            content_type='application/json'
        )
        # Second start (should fail)
        response = self.client.post('/api/field/worklog/start',
            data=json.dumps(work_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_log_one_on_one_meeting(self):
        """Test logging one-on-one meeting"""
        self.login('test_officer', 'test123')
        meeting_data = {
            'meeting_type': 'one_on_one',
            'person_name': 'Test Farmer',
            'person_category': 'Farmer',
            'business_potential': '10-20 kg',
            'latitude': 26.8467,
            'longitude': 80.9462
        }
        response = self.client.post('/api/field/meeting',
            data=json.dumps(meeting_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_log_group_meeting(self):
        """Test logging group meeting"""
        self.login('test_officer', 'test123')
        meeting_data = {
            'meeting_type': 'group',
            'village': 'Test Village',
            'attendees_count': 25,
            'latitude': 26.8467,
            'longitude': 80.9462
        }
        response = self.client.post('/api/field/meeting',
            data=json.dumps(meeting_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_log_sample_distribution(self):
        """Test logging sample distribution"""
        self.login('test_officer', 'test123')
        sample_data = {
            'recipient_name': 'Test Farmer',
            'product_name': 'Test Product',
            'quantity': 1.0,
            'unit': 'kg',
            'purpose': 'trial',
            'latitude': 26.8467,
            'longitude': 80.9462
        }
        response = self.client.post('/api/field/sample',
            data=json.dumps(sample_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_record_b2c_sale(self):
        """Test recording B2C sale"""
        self.login('test_officer', 'test123')
        sale_data = {
            'sale_type': 'B2C',
            'customer_name': 'Test Customer',
            'product_sku': 'TEST-001',
            'product_name': 'Test Product',
            'quantity': 5,
            'unit_price': 100,
            'total_amount': 500,
            'latitude': 26.8467,
            'longitude': 80.9462
        }
        response = self.client.post('/api/field/sale',
            data=json.dumps(sale_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_record_b2b_sale(self):
        """Test recording B2B sale"""
        self.login('test_officer', 'test123')
        sale_data = {
            'sale_type': 'B2B',
            'customer_name': 'Test Distributor',
            'customer_type': 'Distributor',
            'product_sku': 'TEST-001',
            'product_name': 'Test Product',
            'quantity': 50,
            'unit_price': 100,
            'total_amount': 5000,
            'latitude': 26.8467,
            'longitude': 80.9462
        }
        response = self.client.post('/api/field/sale',
            data=json.dumps(sale_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_get_my_activities(self):
        """Test getting personal activity statistics"""
        self.login('test_officer', 'test123')
        response = self.client.get('/api/field/my-activities?days=7')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('meetings', data)
        self.assertIn('sales', data)


class DatabaseModelTests(OccamyTestCase):
    """Test database models"""
    
    def test_create_user(self):
        """Test creating user in database"""
        with app.app_context():
            user = User(
                username='model_test',
                email='model@test.com',
                password_hash=generate_password_hash('test'),
                role='field_officer',
                name='Model Test'
            )
            db.session.add(user)
            db.session.commit()
            
            retrieved = User.query.filter_by(username='model_test').first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.name, 'Model Test')
    
    def test_create_work_log(self):
        """Test creating work log"""
        with app.app_context():
            user = User.query.filter_by(username='test_officer').first()
            work_log = WorkLog(
                user_id=user.id,
                date=date.today(),
                start_location_lat=26.8467,
                start_location_lng=80.9462,
                odometer_start=1000
            )
            db.session.add(work_log)
            db.session.commit()
            
            retrieved = WorkLog.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(retrieved)
    
    def test_create_meeting(self):
        """Test creating meeting"""
        with app.app_context():
            user = User.query.filter_by(username='test_officer').first()
            meeting = Meeting(
                user_id=user.id,
                meeting_type='one_on_one',
                person_name='Test Person',
                person_category='Farmer',
                location_lat=26.8467,
                location_lng=80.9462
            )
            db.session.add(meeting)
            db.session.commit()
            
            retrieved = Meeting.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(retrieved)
    
    def test_user_relationships(self):
        """Test user relationships work"""
        with app.app_context():
            user = User.query.filter_by(username='test_officer').first()
            
            # Create related records
            meeting = Meeting(user_id=user.id, meeting_type='one_on_one')
            sale = Sale(user_id=user.id, sale_type='B2C', customer_name='Test',
                       product_sku='TEST', product_name='Test', quantity=1)
            
            db.session.add_all([meeting, sale])
            db.session.commit()
            
            # Check relationships
            self.assertEqual(len(user.meetings), 1)
            self.assertEqual(len(user.sales), 1)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(AuthenticationTests))
    suite.addTests(loader.loadTestsFromTestCase(AdminAPITests))
    suite.addTests(loader.loadTestsFromTestCase(FieldOfficerAPITests))
    suite.addTests(loader.loadTestsFromTestCase(DatabaseModelTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
