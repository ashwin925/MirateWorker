import sqlite3
from werkzeug.security import generate_password_hash

def init_database():
    conn = sqlite3.connect('migrant_workers.db')
    cursor = conn.cursor()
    
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
    
    # Create indexes for workers table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_unique_id ON workers(unique_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_name ON workers(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_mobile ON workers(mobile)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_registration_date ON workers(registration_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_origin_state ON workers(origin_state)')
    
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
    
    # Create indexes for grievances table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_worker_id ON grievances(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_unique_worker_id ON grievances(unique_worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_status ON grievances(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_created_at ON grievances(created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_issue_type ON grievances(issue_type)')
    
    # Create admin_users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'staff'
        )
    ''')
    
    # Create indexes for admin_users table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_admin_users_role ON admin_users(role)')
    
    # Create composite indexes for common query patterns
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_name_mobile ON workers(name, mobile)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_grievances_status_created ON grievances(status, created_at)')
    
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
    
    # Create indexes for job tables
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_openings_status ON job_openings(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_openings_posted_date ON job_openings(posted_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_job_id ON job_applications(job_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_worker_id ON job_applications(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(status)')
    
    # Create default admin user
    admin_password = generate_password_hash('admin123')
    try:
        cursor.execute('INSERT INTO admin_users (username, password_hash, role) VALUES (?, ?, ?)',
                      ('admin', admin_password, 'admin'))
    except sqlite3.IntegrityError:
        print("Admin user already exists")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
    print("Default admin credentials: username='admin', password='admin123'")

if __name__ == '__main__':
    init_database()
