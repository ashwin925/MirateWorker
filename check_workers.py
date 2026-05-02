import sqlite3

def check_all_workers():
    """Check all workers in database"""
    
    conn = sqlite3.connect('migrant_workers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    workers = cursor.execute('SELECT id, unique_id, name, mobile, password_hash FROM workers').fetchall()
    
    print("=" * 80)
    print(f"Total Workers: {len(workers)}")
    print("=" * 80)
    
    for worker in workers:
        print(f"\nWorker #{worker['id']}")
        print(f"  Unique ID: {worker['unique_id']}")
        print(f"  Name: {worker['name']}")
        print(f"  Mobile: {worker['mobile']}")
        
        if worker['password_hash']:
            print(f"  Password: ✓ SET (hash: {worker['password_hash'][:30]}...)")
        else:
            print(f"  Password: ✗ NOT SET (NULL)")
    
    print("\n" + "=" * 80)
    
    # Check for workers without passwords
    no_password = cursor.execute('SELECT COUNT(*) as count FROM workers WHERE password_hash IS NULL').fetchone()
    
    if no_password['count'] > 0:
        print(f"\n⚠️  WARNING: {no_password['count']} worker(s) have no password set!")
        print("   These workers cannot login.")
    else:
        print(f"\n✓ All workers have passwords set.")
    
    conn.close()

if __name__ == '__main__':
    check_all_workers()
