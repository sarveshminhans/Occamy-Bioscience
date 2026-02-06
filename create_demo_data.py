"""
Demo Data Population Script for Occamy Field Operations
Run this after initial setup to populate the database with sample data for testing
"""

from app import app, db, User, WorkLog, Meeting, Sale, SampleDistribution
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_demo_data():
    with app.app_context():
        print("Creating demo data...")
        
        # Create field officers
        officers = [
            {
                'username': 'rajesh_kumar',
                'email': 'rajesh@occamy.com',
                'password': 'demo123',
                'name': 'Rajesh Kumar',
                'state': 'Uttar Pradesh',
                'district': 'Lucknow',
                'phone': '9876543210'
            },
            {
                'username': 'priya_sharma',
                'email': 'priya@occamy.com',
                'password': 'demo123',
                'name': 'Priya Sharma',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'phone': '9876543211'
            },
            {
                'username': 'amit_patel',
                'email': 'amit@occamy.com',
                'password': 'demo123',
                'name': 'Amit Patel',
                'state': 'Gujarat',
                'district': 'Ahmedabad',
                'phone': '9876543212'
            }
        ]
        
        created_officers = []
        for officer_data in officers:
            officer = User.query.filter_by(username=officer_data['username']).first()
            if not officer:
                officer = User(
                    username=officer_data['username'],
                    email=officer_data['email'],
                    password_hash=generate_password_hash(officer_data['password']),
                    role='field_officer',
                    name=officer_data['name'],
                    state=officer_data['state'],
                    district=officer_data['district'],
                    phone=officer_data['phone']
                )
                db.session.add(officer)
                print(f"Created officer: {officer_data['name']}")
            created_officers.append(officer)
        
        db.session.commit()
        
        # Create work logs for the past 7 days
        villages = ['Rampur', 'Kishanganj', 'Bhagalpur', 'Munger', 'Patna Rural']
        farmer_names = ['Ram Singh', 'Mohan Lal', 'Suresh Kumar', 'Vijay Sharma', 'Rajesh Yadav']
        products = [
            {'sku': 'NUT-001', 'name': 'Calcium Supplement', 'price': 500},
            {'sku': 'NUT-002', 'name': 'Protein Boost', 'price': 750},
            {'sku': 'NUT-003', 'name': 'Vitamin Complex', 'price': 600},
        ]
        
        for days_ago in range(7):
            date = datetime.utcnow().date() - timedelta(days=days_ago)
            
            for officer in created_officers:
                # Create work log
                start_odometer = 1000 + (days_ago * 50)
                distance = random.uniform(30, 80)
                
                work_log = WorkLog(
                    user_id=officer.id,
                    date=date,
                    start_time=datetime.combine(date, datetime.min.time()) + timedelta(hours=9),
                    end_time=datetime.combine(date, datetime.min.time()) + timedelta(hours=17),
                    start_location_lat=26.8467 + random.uniform(-0.5, 0.5),
                    start_location_lng=80.9462 + random.uniform(-0.5, 0.5),
                    end_location_lat=26.8467 + random.uniform(-0.5, 0.5),
                    end_location_lng=80.9462 + random.uniform(-0.5, 0.5),
                    odometer_start=start_odometer,
                    odometer_end=start_odometer + distance,
                    distance_traveled=distance,
                    status='ended'
                )
                db.session.add(work_log)
                
                # Create 2-4 meetings per day
                num_meetings = random.randint(2, 4)
                for _ in range(num_meetings):
                    meeting_type = random.choice(['one_on_one', 'group'])
                    
                    if meeting_type == 'one_on_one':
                        meeting = Meeting(
                            user_id=officer.id,
                            meeting_type='one_on_one',
                            date=datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(10, 16)),
                            person_name=random.choice(farmer_names),
                            person_category=random.choice(['Farmer', 'Seller', 'Influencer']),
                            contact_number=f"98765432{random.randint(10, 99)}",
                            business_potential=random.choice(['5-10 kg', '20-30 kg', '50-100 kg', '100+ kg']),
                            location_lat=26.8467 + random.uniform(-0.5, 0.5),
                            location_lng=80.9462 + random.uniform(-0.5, 0.5),
                            location_name=random.choice(villages),
                            notes=f"Discussed product benefits and pricing"
                        )
                    else:
                        meeting = Meeting(
                            user_id=officer.id,
                            meeting_type='group',
                            date=datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(10, 16)),
                            village=random.choice(villages),
                            attendees_count=random.randint(15, 50),
                            group_meeting_type=random.choice(['Training', 'Demo', 'Awareness Session']),
                            location_lat=26.8467 + random.uniform(-0.5, 0.5),
                            location_lng=80.9462 + random.uniform(-0.5, 0.5),
                            location_name=random.choice(villages),
                            notes=f"Conducted session on product usage"
                        )
                    db.session.add(meeting)
                
                # Create 1-3 sample distributions per day
                num_samples = random.randint(1, 3)
                for _ in range(num_samples):
                    product = random.choice(products)
                    sample = SampleDistribution(
                        user_id=officer.id,
                        date=datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(10, 16)),
                        recipient_name=random.choice(farmer_names),
                        recipient_type=random.choice(['Farmer', 'Distributor']),
                        product_name=product['name'],
                        quantity=random.choice([0.5, 1.0, 2.0]),
                        unit='kg',
                        purpose=random.choice(['trial', 'demo', 'follow-up']),
                        location_lat=26.8467 + random.uniform(-0.5, 0.5),
                        location_lng=80.9462 + random.uniform(-0.5, 0.5),
                        location_name=random.choice(villages),
                        notes='Sample provided for trial'
                    )
                    db.session.add(sample)
                
                # Create 1-2 sales per day
                num_sales = random.randint(1, 2)
                for _ in range(num_sales):
                    product = random.choice(products)
                    sale_type = random.choice(['B2C', 'B2B'])
                    quantity = random.randint(5, 50) if sale_type == 'B2B' else random.randint(1, 10)
                    
                    sale = Sale(
                        user_id=officer.id,
                        date=datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(10, 16)),
                        sale_type=sale_type,
                        customer_name=random.choice(farmer_names),
                        customer_type='Distributor' if sale_type == 'B2B' else 'Farmer',
                        contact_number=f"98765432{random.randint(10, 99)}",
                        product_sku=product['sku'],
                        product_name=product['name'],
                        pack_size='1 kg',
                        quantity=quantity,
                        unit_price=product['price'],
                        total_amount=quantity * product['price'],
                        mode='direct' if sale_type == 'B2C' else 'via_distributor',
                        is_repeat_order=random.choice([True, False]),
                        location_lat=26.8467 + random.uniform(-0.5, 0.5),
                        location_lng=80.9462 + random.uniform(-0.5, 0.5),
                        location_name=random.choice(villages),
                        notes='Transaction completed successfully'
                    )
                    db.session.add(sale)
        
        db.session.commit()
        
        print("\n✅ Demo data created successfully!")
        print("\nDemo Field Officer Credentials:")
        print("=" * 50)
        for officer in officers:
            print(f"Username: {officer['username']}")
            print(f"Password: demo123")
            print(f"Name: {officer['name']}")
            print(f"State: {officer['state']}")
            print("-" * 50)
        
        print("\nAdmin Credentials:")
        print("Username: admin")
        print("Password: admin123")
        print("\nYou can now login and explore the system!")

if __name__ == '__main__':
    create_demo_data()
