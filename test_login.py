import sqlite3
from werkzeug.security import check_password_hash

def test_worker_login():
    """Test if worker can login with their credentials"""
    
    # Get mobile number from user
    mobile = input("Enter mobile number: ")
    password = input("Enter password: ")
    
    # Connect to database
    conn = sqlite3.connect('migrant_workers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get worker
    worker = cursor.execute('SELECT * FROM workers WHERE mobile = ?', (mobile,)).fetchone()
    
    if not worker:
        print(f"❌ No worker found with mobile: {mobile}")
        conn.close()
        return
    
    print(f"\n✓ Worker found:")
    print(f"  ID: {worker['id']}")
    print(f"  Name: {worker['name']}")
    print(f"  Unique ID: {worker['unique_id']}")
    print(f"  Mobile: {worker['mobile']}")
    
    # Check password
    if not worker['password_hash']:
        print(f"\n❌ No password set for this worker!")
        print(f"   Password hash is NULL")
        conn.close()
        return
    
    print(f"\n  Password hash exists: {worker['password_hash'][:50]}...")
    
    # Verify password
    if check_password_hash(worker['password_hash'], password):
        print(f"\n✅ Password is CORRECT! Login should work.")
    else:
        print(f"\n❌ Password is INCORRECT!")
        print(f"   Please check if you entered the correct password.")
    
    conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("Worker Login Test")
    print("=" * 60)
    test_worker_login()
