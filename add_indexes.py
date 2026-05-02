import sqlite3

def add_indexes():
    """Add indexes to existing database for better performance"""
    conn = sqlite3.connect('migrant_workers.db')
    cursor = conn.cursor()
    
    print("Adding indexes to optimize database performance...")
    
    # Indexes for workers table
    indexes = [
        ('idx_workers_unique_id', 'workers', 'unique_id'),
        ('idx_workers_name', 'workers', 'name'),
        ('idx_workers_mobile', 'workers', 'mobile'),
        ('idx_workers_registration_date', 'workers', 'registration_date'),
        ('idx_workers_origin_state', 'workers', 'origin_state'),
        
        # Indexes for grievances table
        ('idx_grievances_worker_id', 'grievances', 'worker_id'),
        ('idx_grievances_unique_worker_id', 'grievances', 'unique_worker_id'),
        ('idx_grievances_status', 'grievances', 'status'),
        ('idx_grievances_created_at', 'grievances', 'created_at'),
        ('idx_grievances_issue_type', 'grievances', 'issue_type'),
        
        # Indexes for admin_users table
        ('idx_admin_users_username', 'admin_users', 'username'),
        ('idx_admin_users_role', 'admin_users', 'role'),
    ]
    
    for idx_name, table_name, column_name in indexes:
        try:
            cursor.execute(f'CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name}({column_name})')
            print(f"✓ Created index: {idx_name}")
        except sqlite3.Error as e:
            print(f"✗ Error creating index {idx_name}: {e}")
    
    # Create composite indexes for common query patterns
    composite_indexes = [
        ('idx_workers_name_mobile', 'workers', 'name, mobile'),
        ('idx_grievances_status_created', 'grievances', 'status, created_at'),
    ]
    
    for idx_name, table_name, columns in composite_indexes:
        try:
            cursor.execute(f'CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name}({columns})')
            print(f"✓ Created composite index: {idx_name}")
        except sqlite3.Error as e:
            print(f"✗ Error creating composite index {idx_name}: {e}")
    
    conn.commit()
    
    # Analyze database for query optimization
    print("\nAnalyzing database for query optimization...")
    cursor.execute('ANALYZE')
    conn.commit()
    
    # Show index statistics
    print("\nIndex Statistics:")
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' ORDER BY tbl_name, name")
    indexes = cursor.fetchall()
    
    current_table = None
    for idx_name, table_name in indexes:
        if table_name != current_table:
            print(f"\n{table_name}:")
            current_table = table_name
        print(f"  - {idx_name}")
    
    conn.close()
    print("\n✓ Database optimization complete!")

if __name__ == '__main__':
    add_indexes()
