# Tamil Nadu Migrant Worker Registration & Support System

A comprehensive web application for registering and supporting migrant workers in Tamil Nadu, India. Built with Flask, SQLite, and modern web technologies.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Government-orange)

---

## 🌟 Features Overview

### 👥 Worker Features
- ✅ **Easy Registration** - Simple form with all required details
- ✅ **Unique Worker ID** - Auto-generated format: TN-MIG-YYYY-XXXXXX
- ✅ **Professional ID Card** - Downloadable PDF with QR code
- ✅ **Personal Dashboard** - View profile, applications, and grievances
- ✅ **Job Search** - Browse and apply for verified job openings
- ✅ **Grievance System** - Submit and track workplace issues
- ✅ **Multilingual** - English, Tamil (தமிழ்), Hindi (हिंदी)
- ✅ **Mobile Friendly** - Responsive design for all devices

### 💼 Job Management
- ✅ **Job Listings** - Browse active job opportunities
- ✅ **Detailed Job Info** - Company, location, salary, requirements
- ✅ **Easy Application** - Apply with optional cover letter
- ✅ **Status Tracking** - Pending, Shortlisted, Selected, Rejected
- ✅ **Application History** - View all past applications

### 📝 Grievance Support
- ✅ **Multiple Categories** - Workplace, Payment, Health, Legal, etc.
- ✅ **Status Updates** - Pending, In Progress, Resolved
- ✅ **Resolution Notes** - Admin feedback on grievances
- ✅ **Timeline Tracking** - Created and updated timestamps

### 🔐 Admin Features
- ✅ **Comprehensive Dashboard** - Real-time statistics
- ✅ **Worker Management** - Search, view, and manage workers
- ✅ **Grievance Management** - Update status and add notes
- ✅ **Job Management** - Create, edit, and manage job postings
- ✅ **Application Review** - View and update application status
- ✅ **CSV Reports** - Download workers and grievances data
- ✅ **User Management** - Add admin and staff users
- ✅ **Role-Based Access** - Admin vs Staff permissions

### 🎨 UI/UX Features
- ✅ **Modern Design** - Clean, professional interface
- ✅ **Orange & White Theme** - Consistent branding
- ✅ **Responsive Layout** - Works on all screen sizes
- ✅ **Intuitive Navigation** - Easy to use for all literacy levels
- ✅ **Professional Landing Page** - Hero section, features, benefits
- ✅ **Custom Components** - Cards, tables, forms, modals

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd migrant-worker-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize database**
```bash
python setup.py
```

4. **Populate sample data (optional)**
```bash
python populate_sample_data.py
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
- Open browser: http://localhost:5000
- Admin login: http://localhost:5000/admin/login
- Worker login: http://localhost:5000/worker/login

---

## 📋 Default Credentials

### Admin Access
- **Username:** `admin`
- **Password:** `admin123`

### Sample Workers (if populated)
- **Mobile:** 9876543210 to 9876543300
- **Password:** Same as mobile number

📄 **See [SAMPLE_CREDENTIALS.md](SAMPLE_CREDENTIALS.md) for complete list**

---

## 🗂️ Project Structure

```
migrant-worker-system/
├── app.py                          # Main Flask application
├── setup.py                        # Database setup script
├── populate_sample_data.py         # Sample data generator
├── init_db.py                      # Database initialization
├── requirements.txt                # Python dependencies
├── translations.json               # Multilingual translations
├── migrant_workers.db             # SQLite database (auto-created)
│
├── static/
│   ├── style.css                  # Main stylesheet
│   ├── landing.css                # Landing page styles
│   └── script.js                  # JavaScript functionality
│
├── templates/
│   ├── base.html                  # Base template
│   ├── landing.html               # Landing page
│   ├── register.html              # Worker registration
│   ├── worker_login.html          # Worker login
│   ├── worker_dashboard.html      # Worker dashboard
│   ├── worker_profile.html        # Worker profile
│   ├── grievance_form.html        # Grievance submission
│   ├── job_list.html              # Job listings
│   ├── job_detail.html            # Job details
│   ├── admin_login.html           # Admin login
│   ├── admin_dashboard.html       # Admin dashboard
│   ├── admin_workers.html         # Worker management
│   ├── admin_grievances.html      # Grievance management
│   ├── admin_jobs.html            # Job management
│   ├── admin_job_create.html      # Create job
│   ├── admin_job_applications.html # View applications
│   ├── admin_reports.html         # Download reports
│   ├── admin_add_user.html        # Add admin user
│   ├── 404.html                   # Error page
│   └── 500.html                   # Error page
│
└── docs/
    ├── README.md                  # This file
    ├── SAMPLE_CREDENTIALS.md      # Login credentials
    ├── FEATURES_UPDATE.md         # Feature documentation
    └── QUICK_START.md             # Quick start guide
```

---

## 💾 Database Schema

### Workers Table
- Unique worker ID, personal details
- Contact information
- Employment details
- Skills and qualifications
- Password hash for login
- Optional Aadhaar number

### Grievances Table
- Worker reference
- Issue type and description
- Status tracking
- Resolution notes
- Timestamps

### Job Openings Table
- Job details and requirements
- Company information
- Salary range
- Vacancies count
- Application deadline
- Status (Active/Closed)

### Job Applications Table
- Worker and job references
- Application date
- Cover letter
- Status tracking
- Admin notes

### Admin Users Table
- Username and password hash
- Role (Admin/Staff)

**All tables have proper indexes for optimal performance**

---

## 🔧 Key Technologies

- **Backend:** Flask (Python)
- **Database:** SQLite with optimized indexes
- **PDF Generation:** ReportLab
- **QR Codes:** Python qrcode library
- **Authentication:** Flask-Login
- **Security:** Werkzeug password hashing
- **Frontend:** Custom CSS (no Bootstrap)
- **Icons:** Bootstrap Icons
- **Responsive:** Mobile-first design

---

## 🌐 Multilingual Support

The system supports three languages:

1. **English** - Default language
2. **Tamil (தமிழ்)** - Primary regional language
3. **Hindi (हिंदी)** - National language

Language preference is saved in cookies and persists across sessions.

---

## 📊 Features in Detail

### Worker Registration
- Comprehensive form with validation
- Required fields: Name, Age, Gender, Mobile, Origin State, Address, Employer, Skills, Emergency Contact, Password
- Optional: Aadhaar number
- Auto-generates unique worker ID
- Creates secure password hash
- Prevents duplicate mobile numbers

### Professional ID Card PDF
- Government branding with emblem
- Worker photo placeholder with initial
- All worker details in organized format
- QR code for profile verification
- Security features and watermark
- Registration date and issuing authority
- Professional layout with color coding
- Downloadable as PDF

### Job Application System
- Browse active job openings
- Filter by location, type, company
- View detailed job descriptions
- Submit applications with cover letter
- Track application status
- Receive admin feedback
- View application history

### Grievance Management
- Six issue categories:
  - Workplace Issues
  - Payment Disputes
  - Health Issues
  - Missing/Stolen Documents
  - Abuse/Harassment
  - Legal Aid Requests
- Status tracking (Pending → In Progress → Resolved)
- Admin can add resolution notes
- Timeline tracking with timestamps

### Admin Dashboard
- Real-time statistics:
  - Total workers
  - Total grievances
  - Pending grievances
  - Today's registrations
  - Total jobs
  - Active jobs
  - Total applications
  - Pending applications
- Recent activities feed
- Quick action buttons
- Responsive charts and cards

---

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ SQL injection prevention (parameterized queries)
- ✅ CSRF protection
- ✅ Secure cookie handling
- ✅ Input validation
- ✅ XSS prevention

---

## 📱 Mobile Responsiveness

- Optimized for all screen sizes
- Touch-friendly buttons and forms
- Readable text on small screens
- Collapsible navigation
- Responsive tables
- Mobile-first design approach

---

## 🎯 Use Cases

1. **Worker Registration** - Migrant workers register and get official ID
2. **Job Matching** - Workers find suitable employment opportunities
3. **Issue Resolution** - Workers report and track workplace problems
4. **Government Tracking** - Officials monitor migrant worker welfare
5. **Employer Verification** - Verify worker credentials via QR code
6. **Data Analytics** - Generate reports for policy decisions

---

## 🛠️ Maintenance & Updates

### Database Backup
```bash
# Backup database
copy migrant_workers.db migrant_workers_backup.db
```

### Reset Database
```bash
# Delete and reinitialize
del migrant_workers.db
python setup.py
python populate_sample_data.py
```

### Check Database Status
```bash
python check_workers.py
```

### Add Indexes (if needed)
```bash
python add_indexes.py
```

---

## 📈 Performance Optimization

- Database indexes on all frequently queried columns
- Composite indexes for complex queries
- Efficient JOIN operations
- Minimal database calls per page
- Optimized PDF generation
- Cached translations
- Lightweight CSS (no Bootstrap)

---

## 🐛 Troubleshooting

### Common Issues

**Database Errors:**
```bash
del migrant_workers.db
python setup.py
```

**Port Already in Use:**
Edit `app.py` and change port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Missing Dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**Translation Not Working:**
- Clear browser cookies
- Check translations.json file
- Verify language selector in navbar

---

## 🚀 Production Deployment

For production use:

1. ✅ Change `SECRET_KEY` in `app.py`
2. ✅ Set `debug=False`
3. ✅ Use production WSGI server (Gunicorn/uWSGI)
4. ✅ Set up HTTPS with SSL certificate
5. ✅ Use PostgreSQL/MySQL instead of SQLite
6. ✅ Enable proper logging
7. ✅ Set up regular database backups
8. ✅ Configure firewall rules
9. ✅ Use environment variables for secrets
10. ✅ Set up monitoring and alerts

---

## 📞 Support & Contact

- **Government Department:** Tamil Nadu Labour Department
- **Location:** Chennai, Tamil Nadu
- **Purpose:** Migrant Worker Welfare

---

## 📄 License

This project is developed for the Tamil Nadu Government's migrant worker support initiative.

---

## 🙏 Acknowledgments

- Tamil Nadu Government
- Labour Department
- All migrant workers
- Development team

---

## 📝 Changelog

### Version 1.0.0 (2025-01-15)
- ✅ Initial release
- ✅ Worker registration and login
- ✅ Professional ID card generation
- ✅ Job management system
- ✅ Grievance tracking
- ✅ Admin dashboard
- ✅ Multilingual support
- ✅ Mobile responsive design
- ✅ Database optimization
- ✅ Sample data population

---

**Made with ❤️ for Tamil Nadu Migrant Workers**

**Version:** 1.0.0  
**Last Updated:** January 15, 2025  
**Status:** Production Ready ✅
