"""
Complete setup script for Tamil Nadu Migrant Worker System
Run this script to set up the database from scratch
"""

import sqlite3
from werkzeug.security import generate_password_hash
import os

def setup_database():
    """Initialize database with all tables and indexes"""
    
    print("=" * 70)
    print("Tamil Nadu Migrant Worker System - Database Setup")
    print("=" * 70)
    
    # Remove old database if exists
    if os.path.exists('migrant_workers.db'):
        response = input("\nDatabase already exists. Delete and recreate? (yes/no): ")
        if response.lower() != 'yes':
            print("Setup cancelled.")
            return
        os.remove('migrant_workers.db')
        print("✓ Old database removed")
    
    conn = sqlite3.connect('migrant_workers.db')
    cursor = conn.cursor()
    
    print("\nCreating tables...")
    
    # Create workers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            mobile TEXT NOT NULL,
            password_hash TEXT,
            origin_state TEXT NOT NULL,
            address_tn TEXT NOT NULL,
            employer_name TEXT NOT NULL,
            skills TEXT NOT NULL,
            emergency_contact TEXT NOT NULL,
            aadhaar TEXT,
            registration_date TEXT NOT NULL
        )
    ''')
    print("✓ Workers table created")
    
    # Create grievances table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER NOT NULL,
            unique_worker_id TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            resolution_notes TEXT,
            FOREIGN KEY(worker_id) REFERENCES workers(id)
        )
    ''')
    print("✓ Grievances table created")
    
    # Create admin_users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'staff'
        )
    ''')
    print("✓ Admin users table created")
    
    # Create job_openings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_openings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company_name TEXT NOT NULL,
            location TEXT NOT NULL,
            job_type TEXT NOT NULL,
            salary_range TEXT,
            description TEXT NOT NULL,
            requirements TEXT NOT NULL,
            vacancies INTEGER NOT NULL,
            posted_by INTEGER NOT NULL,
            posted_date TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY(posted_by) REFERENCES admin_users(id)
        )
    ''')
    print("✓ Job openings table created")
    
    # Create job_applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            worker_id INTEGER NOT NULL,
            unique_worker_id TEXT NOT NULL,
            application_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            cover_letter TEXT,
            admin_notes TEXT,
            FOREIGN KEY(job_id) REFERENCES job_openings(id),
            FOREIGN KEY(worker_id) REFERENCES workers(id)
        )
    ''')
    print("✓ Job applications table created")
    
    print("\nCreating indexes...")
    
    # Indexes for workers
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_unique_id ON workers(unique_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_name ON workers(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_mobile ON workers(mobile)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_registration_date ON workers(registration_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_origin_state ON workers(origin_state)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_name_mobile ON workers(name, mobile)')
    print("✓ Workers indexes created")
    
    # Indexes for grievances
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_worker_id ON grievances(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_unique_worker_id ON grievances(unique_worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_status ON grievances(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_created_at ON grievances(created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_issue_type ON grievances(issue_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_status_created ON grievances(status, created_at)')
    print("✓ Grievances indexes created")
    
    # Indexes for admin_users
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_admin_users_role ON admin_users(role)')
    print("✓ Admin users indexes created")
    
    # Indexes for job tables
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_openings_status ON job_openings(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_openings_posted_date ON job_openings(posted_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_job_id ON job_applications(job_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_worker_id ON job_applications(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(status)')
    print("✓ Job indexes created")
    
    # Create default admin user
    print("\nCreating default admin user...")
    admin_password = generate_password_hash('admin123')
    try:
        cursor.execute('INSERT INTO admin_users (username, password_hash, role) VALUES (?, ?, ?)',
                      ('admin', admin_password, 'admin'))
        print("✓ Default admin user created")
    except sqlite3.IntegrityError:
        print("- Admin user already exists")
    
    # Analyze database
    cursor.execute('ANALYZE')
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ Database setup completed successfully!")
    print("=" * 70)
    print("\nDefault Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n⚠️  IMPORTANT: Change the default password after first login!")
    print("\nYou can now run the application:")
    print("  python app.py")
    print("=" * 70)

if __name__ == '__main__':
    setup_database()
