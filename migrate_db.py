import sqlite3
from werkzeug.security import generate_password_hash

def migrate_database():
    """Add new tables and columns for enhanced features"""
    conn = sqlite3.connect('migrant_workers.db')
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    # Add password field to workers table for login
    try:
        cursor.execute('ALTER TABLE workers ADD COLUMN password_hash TEXT')
        print("✓ Added password_hash to workers table")
    except sqlite3.OperationalError:
        print("- password_hash column already exists")
    
    # Add aadhaar field to workers table (optional)
    try:
        cursor.execute('ALTER TABLE workers ADD COLUMN aadhaar TEXT')
        print("✓ Added aadhaar to workers table")
    except sqlite3.OperationalError:
        print("- aadhaar column already exists")
    
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
    print("✓ Created job_openings table")
    
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
    print("✓ Created job_applications table")
    
    # Create indexes for new tables
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_openings_status ON job_openings(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_openings_posted_date ON job_openings(posted_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_job_id ON job_applications(job_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_worker_id ON job_applications(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_mobile ON workers(mobile)')
    print("✓ Created indexes for new tables")
    
    # Update existing workers to have default passwords (mobile number)
    cursor.execute('SELECT id, mobile, password_hash FROM workers')
    workers = cursor.fetchall()
    for worker_id, mobile, password_hash in workers:
        if not password_hash:
            default_password = generate_password_hash(mobile)
            cursor.execute('UPDATE workers SET password_hash = ? WHERE id = ?', (default_password, worker_id))
    print(f"✓ Updated {len(workers)} workers with default passwords")
    
    conn.commit()
    
    # Analyze database
    cursor.execute('ANALYZE')
    conn.commit()
    
    conn.close()
    print("\n✓ Database migration completed successfully!")
    print("\nNote: Existing workers can login with their mobile number as password")

if __name__ == '__main__':
    migrate_database()
