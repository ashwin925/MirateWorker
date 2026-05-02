# Sample Login Credentials

## 🔐 Admin Login

**URL:** http://localhost:5000/admin/login

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |

**Admin Capabilities:**
- Full system access
- Create/manage job openings
- View and update all grievances
- Manage all workers
- Add new admin/staff users
- Download reports (CSV)
- Update job application statuses

---

## 👷 Sample Worker Logins

**URL:** http://localhost:5000/worker/login

**Note:** Password is same as mobile number for all sample workers

| Worker ID | Name | Mobile | Password | Origin State | Skills |
|-----------|------|--------|----------|--------------|--------|
| TN-MIG-2025-000001 | Rajesh Kumar | 9876543210 | 9876543210 | Bihar | Mason, Plastering |
| TN-MIG-2025-000002 | Amit Singh | 9876543220 | 9876543220 | Uttar Pradesh | Carpenter, Welding |
| TN-MIG-2025-000003 | Priya Devi | 9876543230 | 9876543230 | Jharkhand | Tailoring, Packaging |
| TN-MIG-2025-000004 | Suresh Yadav | 9876543240 | 9876543240 | Madhya Pradesh | Machine Operator |
| TN-MIG-2025-000005 | Lakshmi Bai | 9876543250 | 9876543250 | Odisha | Weaving, Quality Check |
| TN-MIG-2025-000006 | Ramesh Prasad | 9876543260 | 9876543260 | West Bengal | Electrician, Plumbing |
| TN-MIG-2025-000007 | Sunita Kumari | 9876543270 | 9876543270 | Chhattisgarh | Cooking, Cleaning |
| TN-MIG-2025-000008 | Vijay Sharma | 9876543280 | 9876543280 | Rajasthan | Driver, Loading |
| TN-MIG-2025-000009 | Anita Verma | 9876543290 | 9876543290 | Assam | Nursing Assistant |
| TN-MIG-2025-000010 | Manoj Tiwari | 9876543300 | 9876543300 | Bihar | Weaving, Dyeing |

**Worker Capabilities:**
- View personal profile
- Download professional ID card (PDF)
- Submit grievances
- Browse job openings
- Apply for jobs with cover letter
- Track application status
- View grievance status

---

## 📊 Sample Data Summary

### Workers: 10
- From 8 different states (Bihar, UP, Jharkhand, MP, Odisha, West Bengal, Chhattisgarh, Rajasthan, Assam)
- Various skill sets (Construction, Manufacturing, Services, Healthcare)
- All registered with unique IDs

### Job Openings: 10
1. Construction Worker - ABC Construction Ltd (Chennai)
2. Factory Worker - XYZ Manufacturing (Coimbatore)
3. Delivery Driver - Quick Logistics (Madurai)
4. Housekeeping Staff - Grand Hotel (Salem)
5. Warehouse Helper - Storage Solutions (Trichy)
6. Security Guard - SecureMax Services (Vellore)
7. Cook - Tasty Foods Restaurant (Erode)
8. Electrician - Power Solutions (Tirunelveli)
9. Tailor - Fashion Garments (Thanjavur)
10. Painter - Color World (Kanchipuram)

### Grievances: 10
- **Status Breakdown:**
  - Pending: 4
  - In Progress: 3
  - Resolved: 2
- **Types:** Payment Disputes, Workplace Issues, Health Issues, Harassment, Missing Documents, Legal Aid

### Job Applications: 15
- **Status Breakdown:**
  - Pending: 7
  - Shortlisted: 3
  - Selected: 3
  - Rejected: 2

---

## 🧪 Testing Scenarios

### Scenario 1: Worker Registration & Login
1. Go to homepage
2. Click "Register Now"
3. Fill in all details
4. Create password
5. Login with mobile and password
6. Access dashboard

### Scenario 2: Job Application
1. Login as worker (e.g., 9876543210)
2. Browse jobs
3. View job details
4. Submit application with cover letter
5. Check application status in dashboard

### Scenario 3: Grievance Submission
1. Login as worker
2. Go to "Submit Grievance"
3. Select issue type
4. Describe the problem
5. Submit
6. Track status in dashboard

### Scenario 4: Admin Management
1. Login as admin
2. View dashboard statistics
3. Manage grievances (update status)
4. Review job applications
5. Update application status
6. Download reports

### Scenario 5: ID Card Download
1. Login as any worker
2. Click "Download ID Card"
3. Get professional PDF with:
   - Government branding
   - Worker photo placeholder
   - All details
   - QR code
   - Security features

---

## 🔄 Quick Reset

To reset the database with sample data:

```bash
# Delete existing database
del migrant_workers.db

# Initialize fresh database
python setup.py

# Populate with sample data
python populate_sample_data.py
```

---

## ⚠️ Important Notes

1. **Change Default Passwords:** Always change default admin password in production
2. **Sample Data:** This is test data for demonstration purposes only
3. **Mobile Numbers:** Sample mobile numbers are fictional
4. **Aadhaar Numbers:** Sample Aadhaar numbers are for testing only
5. **Security:** Never use these credentials in production environment

---

## 📞 Support

For testing issues or questions:
- Check console logs for errors
- Verify database is populated: `python check_workers.py`
- Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**Last Updated:** 2025-01-15
**Database Version:** 1.0
**Sample Data Version:** 1.0
