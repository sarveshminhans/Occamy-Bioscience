"""
Database Migration Script
Use this to migrate from SQLite to PostgreSQL or to reset database
"""

from app import app, db
from app import User, WorkLog, Meeting, Sale, SampleDistribution, LocationLog
from werkzeug.security import generate_password_hash
import sys

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")

def drop_tables():
    """Drop all database tables (DESTRUCTIVE!)"""
    with app.app_context():
        print("WARNING: This will delete all data!")
        confirm = input("Type 'DELETE ALL DATA' to confirm: ")
        if confirm == "DELETE ALL DATA":
            print("Dropping all tables...")
            db.drop_all()
            print("✓ Tables dropped successfully")
        else:
            print("✗ Operation cancelled")

def reset_database():
    """Drop and recreate all tables"""
    with app.app_context():
        print("WARNING: This will delete all data!")
        confirm = input("Type 'RESET DATABASE' to confirm: ")
        if confirm == "RESET DATABASE":
            print("Dropping all tables...")
            db.drop_all()
            print("Creating fresh tables...")
            db.create_all()
            print("✓ Database reset successfully")
            
            # Create default admin
            create_default_admin()
        else:
            print("✗ Operation cancelled")

def create_default_admin():
    """Create default admin user"""
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@occamy.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                name='System Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin created: admin / admin123")
        else:
            print("✓ Admin already exists")

def export_to_sql(filename='backup.sql'):
    """Export database to SQL file (SQLite only)"""
    import sqlite3
    import os
    
    if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        print("✗ This function only works with SQLite databases")
        return
    
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        print(f"✗ Database file not found: {db_path}")
        return
    
    print(f"Exporting database to {filename}...")
    conn = sqlite3.connect(db_path)
    with open(filename, 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    conn.close()
    print(f"✓ Database exported to {filename}")

def migrate_to_postgres():
    """Helper guide for migrating to PostgreSQL"""
    print("""
    Migration Guide: SQLite to PostgreSQL
    =====================================
    
    1. Install PostgreSQL and create database:
       $ createdb occamy_db
    
    2. Export current data:
       $ python migrate_db.py export
    
    3. Update DATABASE_URL in .env or environment:
       DATABASE_URL=postgresql://user:password@localhost/occamy_db
    
    4. Create tables in PostgreSQL:
       $ python migrate_db.py create
    
    5. Import data manually or use data migration tool
    
    6. Test the application:
       $ python app.py
    
    For production, consider using Alembic for migrations.
    """)

def show_stats():
    """Show database statistics"""
    with app.app_context():
        print("\nDatabase Statistics")
        print("=" * 50)
        print(f"Users: {User.query.count()}")
        print(f"  - Admins: {User.query.filter_by(role='admin').count()}")
        print(f"  - Field Officers: {User.query.filter_by(role='field_officer').count()}")
        print(f"Work Logs: {WorkLog.query.count()}")
        print(f"Meetings: {Meeting.query.count()}")
        print(f"  - One-on-One: {Meeting.query.filter_by(meeting_type='one_on_one').count()}")
        print(f"  - Group: {Meeting.query.filter_by(meeting_type='group').count()}")
        print(f"Sales: {Sale.query.count()}")
        print(f"  - B2C: {Sale.query.filter_by(sale_type='B2C').count()}")
        print(f"  - B2B: {Sale.query.filter_by(sale_type='B2B').count()}")
        print(f"Sample Distributions: {SampleDistribution.query.count()}")
        print(f"Location Logs: {LocationLog.query.count()}")
        print("=" * 50)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("""
Database Migration Tool
=======================

Usage: python migrate_db.py [command]

Commands:
  create        Create all database tables
  drop          Drop all database tables (DESTRUCTIVE!)
  reset         Drop and recreate all tables (DESTRUCTIVE!)
  admin         Create default admin user
  export        Export database to SQL file (SQLite only)
  migrate       Show PostgreSQL migration guide
  stats         Show database statistics

Examples:
  python migrate_db.py create
  python migrate_db.py reset
  python migrate_db.py stats
        """)
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'create': create_tables,
        'drop': drop_tables,
        'reset': reset_database,
        'admin': create_default_admin,
        'export': export_to_sql,
        'migrate': migrate_to_postgres,
        'stats': show_stats
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"✗ Unknown command: {command}")
        print("Run without arguments to see available commands")

if __name__ == '__main__':
    main()
