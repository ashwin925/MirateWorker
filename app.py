from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import qrcode
from io import BytesIO
import base64
from datetime import datetime
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tamil-nadu-migrant-worker-system-2025'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Database helper
def get_db():
    conn = sqlite3.connect('migrant_workers.db')
    conn.row_factory = sqlite3.Row
    return conn

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM admin_users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['role'])
    return None

# Load translations
def load_translations():
    with open('translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

translations = load_translations()

def get_lang():
    return request.cookies.get('lang', 'en')

@app.context_processor
def inject_translations():
    lang = get_lang()
    return dict(t=translations.get(lang, translations['en']), lang=lang)

# Generate unique worker ID
def generate_worker_id():
    conn = get_db()
    year = datetime.now().year
    last_worker = conn.execute('SELECT id FROM workers ORDER BY id DESC LIMIT 1').fetchone()
    next_id = (last_worker['id'] + 1) if last_worker else 1
    conn.close()
    return f"TN-MIG-{year}-{str(next_id).zfill(6)}"

# Generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

# Routes
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/register-form')
def register_form():
    return render_template('register.html')

@app.route('/set_language/<lang>')
def set_language(lang):
    resp = make_response(redirect(request.referrer or url_for('index')))
    resp.set_cookie('lang', lang, max_age=60*60*24*365)
    return resp

@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        mobile = request.form['mobile']
        password = request.form['password']
        origin_state = request.form['origin_state']
        address_tn = request.form['address_tn']
        employer_name = request.form['employer_name']
        skills = request.form['skills']
        emergency_contact = request.form['emergency_contact']
        aadhaar = request.form.get('aadhaar', '')  # Optional
        
        # Check if mobile already exists
        conn = get_db()
        existing = conn.execute('SELECT id FROM workers WHERE mobile = ?', (mobile,)).fetchone()
        if existing:
            flash('Mobile number already registered!', 'error')
            conn.close()
            return redirect(url_for('index'))
        
        unique_id = generate_worker_id()
        registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        password_hash = generate_password_hash(password)
        
        conn.execute('''INSERT INTO workers 
                       (unique_id, name, age, gender, mobile, password_hash, origin_state, address_tn, 
                        employer_name, skills, emergency_contact, aadhaar, registration_date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (unique_id, name, age, gender, mobile, password_hash, origin_state, address_tn,
                     employer_name, skills, emergency_contact, aadhaar, registration_date))
        conn.commit()
        conn.close()
        
        flash('Registration successful! You can now login with your mobile number and password.', 'success')
        return redirect(url_for('worker_login'))
    except Exception as e:
        flash(f'Registration failed: {str(e)}', 'error')
        return redirect(url_for('index'))

# Worker Login Routes
@app.route('/worker/login', methods=['GET', 'POST'])
def worker_login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']
        
        conn = get_db()
        worker = conn.execute('SELECT * FROM workers WHERE mobile = ?', (mobile,)).fetchone()
        conn.close()
        
        if worker:
            # Check if password_hash exists
            if not worker['password_hash']:
                flash('Your account needs password setup. Please contact admin.', 'error')
                return render_template('worker_login.html')
            
            if check_password_hash(worker['password_hash'], password):
                session['worker_id'] = worker['id']
                session['worker_unique_id'] = worker['unique_id']
                session['worker_name'] = worker['name']
                flash('Login successful!', 'success')
                return redirect(url_for('worker_dashboard'))
            else:
                flash('Invalid password', 'error')
        else:
            flash('Mobile number not registered', 'error')
    
    return render_template('worker_login.html')

@app.route('/worker/logout')
def worker_logout():
    session.pop('worker_id', None)
    session.pop('worker_unique_id', None)
    session.pop('worker_name', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/worker/dashboard')
def worker_dashboard():
    if 'worker_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('worker_login'))
    
    conn = get_db()
    worker = conn.execute('SELECT * FROM workers WHERE id = ?', (session['worker_id'],)).fetchone()
    
    # Get worker's grievances
    grievances = conn.execute('SELECT * FROM grievances WHERE worker_id = ? ORDER BY created_at DESC', 
                             (session['worker_id'],)).fetchall()
    
    # Get worker's job applications
    applications = conn.execute('''
        SELECT ja.*, jo.title, jo.company_name, jo.location, jo.salary_range
        FROM job_applications ja
        JOIN job_openings jo ON ja.job_id = jo.id
        WHERE ja.worker_id = ?
        ORDER BY ja.application_date DESC
    ''', (session['worker_id'],)).fetchall()
    
    # Get active job openings
    job_openings = conn.execute("SELECT * FROM job_openings WHERE status = 'Active' ORDER BY posted_date DESC LIMIT 5").fetchall()
    
    conn.close()
    
    # Generate QR code
    qr_data = request.url_root + 'worker/profile/' + worker['unique_id']
    qr_code = generate_qr_code(qr_data)
    
    return render_template('worker_dashboard.html', worker=worker, qr_code=qr_code, 
                         grievances=grievances, applications=applications, job_openings=job_openings)

@app.route('/worker/<unique_id>')
@app.route('/worker/profile/<unique_id>')
def worker_profile(unique_id):
    conn = get_db()
    worker = conn.execute('SELECT * FROM workers WHERE unique_id = ?', (unique_id,)).fetchone()
    conn.close()
    
    if not worker:
        flash('Worker not found', 'error')
        return redirect(url_for('index'))
    
    # Generate QR code for worker profile
    qr_data = request.url_root + 'worker/profile/' + unique_id
    qr_code = generate_qr_code(qr_data)
    
    return render_template('worker_profile.html', worker=worker, qr_code=qr_code)

@app.route('/worker/<unique_id>/pdf')
@app.route('/worker/profile/<unique_id>/pdf')
def worker_pdf(unique_id):
    conn = get_db()
    worker = conn.execute('SELECT * FROM workers WHERE unique_id = ?', (unique_id,)).fetchone()
    conn.close()
    
    if not worker:
        return "Worker not found", 404
    
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as pdf_canvas
    
    # Create professional ID card PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Define colors
    primary_orange = colors.HexColor('#FF6B35')
    dark_blue = colors.HexColor('#1E3A8A')
    light_gray = colors.HexColor('#F5F5F5')
    
    # Outer border with shadow effect
    p.setStrokeColor(colors.HexColor('#E0E0E0'))
    p.setLineWidth(1)
    p.rect(35, 35, width-70, height-70, stroke=1, fill=0)
    
    # Main border
    p.setStrokeColor(primary_orange)
    p.setLineWidth(2)
    p.rect(40, 40, width-80, height-80, stroke=1, fill=0)
    
    # Header section with gradient effect (simulated with rectangles)
    p.setFillColor(dark_blue)
    p.rect(40, height-160, width-80, 120, stroke=0, fill=1)
    
    # Orange accent bar
    p.setFillColor(primary_orange)
    p.rect(40, height-165, width-80, 5, stroke=0, fill=1)
    
    # Government emblem placeholder (circle)
    p.setFillColor(colors.white)
    p.circle(width/2, height-70, 25, stroke=0, fill=1)
    p.setFillColor(primary_orange)
    p.circle(width/2, height-70, 20, stroke=0, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height-75, "TN")
    
    # Title
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width/2, height-110, "TAMIL NADU GOVERNMENT")
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height-130, "Migrant Worker Identity Card")
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height-148, "தமிழ்நாடு அரசு - புலம்பெயர்ந்த தொழிலாளர் அடையாள அட்டை")
    
    # Worker ID section with professional styling
    p.setFillColor(light_gray)
    p.roundRect(60, height-210, width-120, 40, 5, stroke=0, fill=1)
    
    p.setFillColor(primary_orange)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(70, height-190, "WORKER ID:")
    
    p.setFillColor(dark_blue)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(160, height-192, worker['unique_id'])
    
    # Photo placeholder
    p.setFillColor(light_gray)
    p.roundRect(60, height-380, 120, 140, 8, stroke=1, fill=1)
    p.setStrokeColor(primary_orange)
    p.setLineWidth(2)
    p.roundRect(60, height-380, 120, 140, 8, stroke=1, fill=0)
    
    # Worker initial in photo placeholder
    p.setFillColor(primary_orange)
    p.setFont("Helvetica-Bold", 48)
    p.drawCentredString(120, height-320, worker['name'][0].upper())
    
    # Worker details section
    p.setFillColor(colors.black)
    y = height-250
    x_label = 200
    x_value = 340
    
    details = [
        ("Full Name", worker['name']),
        ("Age", f"{worker['age']} years"),
        ("Gender", worker['gender']),
        ("Mobile Number", worker['mobile']),
        ("Origin State", worker['origin_state']),
        ("Current Address", worker['address_tn'][:40] + "..." if len(worker['address_tn']) > 40 else worker['address_tn']),
        ("Employer", worker['employer_name']),
        ("Skills", worker['skills'][:35] + "..." if len(worker['skills']) > 35 else worker['skills']),
        ("Emergency Contact", worker['emergency_contact']),
    ]
    
    for label, value in details:
        # Label
        p.setFont("Helvetica-Bold", 9)
        p.setFillColor(colors.HexColor('#666666'))
        p.drawString(x_label, y, label.upper())
        
        # Value
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.black)
        p.drawString(x_value, y, str(value))
        
        # Separator line
        p.setStrokeColor(colors.HexColor('#E0E0E0'))
        p.setLineWidth(0.5)
        p.line(x_label, y-5, width-60, y-5)
        
        y -= 22
    
    # QR Code section
    qr_data = request.url_root + 'worker/profile/' + unique_id
    qr = qrcode.QRCode(version=1, box_size=6, border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_buffer = BytesIO()
    img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    # QR code with border
    qr_x = 70
    qr_y = 100
    p.setFillColor(colors.white)
    p.roundRect(qr_x-5, qr_y-5, 110, 110, 5, stroke=0, fill=1)
    p.setStrokeColor(primary_orange)
    p.setLineWidth(2)
    p.roundRect(qr_x-5, qr_y-5, 110, 110, 5, stroke=1, fill=0)
    p.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=100, height=100)
    
    # QR code label
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 8)
    p.drawCentredString(qr_x+50, qr_y-15, "SCAN FOR VERIFICATION")
    
    # Registration info box
    p.setFillColor(light_gray)
    p.roundRect(200, 95, 340, 35, 5, stroke=0, fill=1)
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 9)
    p.drawString(210, 115, "REGISTRATION DATE:")
    p.setFont("Helvetica", 9)
    p.drawString(330, 115, worker['registration_date'][:10])
    
    p.setFont("Helvetica-Bold", 9)
    p.drawString(210, 102, "ISSUED BY:")
    p.setFont("Helvetica", 9)
    p.drawString(280, 102, "Tamil Nadu Labour Department")
    
    # Footer section
    p.setFillColor(dark_blue)
    p.rect(40, 40, width-80, 35, stroke=0, fill=1)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 9)
    p.drawCentredString(width/2, 60, "This is an official identity card issued by the Government of Tamil Nadu")
    p.setFont("Helvetica", 7)
    p.drawCentredString(width/2, 50, "For verification and support, visit: " + request.url_root)
    
    # Watermark
    p.setFillColor(colors.HexColor('#F0F0F0'))
    p.setFont("Helvetica-Bold", 60)
    p.saveState()
    p.translate(width/2, height/2)
    p.rotate(45)
    p.drawCentredString(0, 0, "OFFICIAL")
    p.restoreState()
    
    # Security features text
    p.setFillColor(colors.HexColor('#999999'))
    p.setFont("Helvetica", 6)
    p.drawString(45, 30, f"Document ID: {worker['unique_id']} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'TN_Worker_ID_{unique_id}.pdf', mimetype='application/pdf')
    p.rect(30, 30, width-60, 40, stroke=0, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width/2, 50, "This is an official identity card issued by Tamil Nadu Government")
    p.setFont("Helvetica", 8)
    p.drawCentredString(width/2, 38, "For verification, visit: " + request.url_root)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'TN_Worker_ID_{unique_id}.pdf', mimetype='application/pdf')

@app.route('/grievance/<unique_id>')
def grievance_form(unique_id):
    conn = get_db()
    worker = conn.execute('SELECT * FROM workers WHERE unique_id = ?', (unique_id,)).fetchone()
    conn.close()
    
    if not worker:
        flash('Worker not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('grievance_form.html', worker=worker)

@app.route('/grievance_submit', methods=['POST'])
def grievance_submit():
    try:
        unique_worker_id = request.form['unique_worker_id']
        issue_type = request.form['issue_type']
        description = request.form['description']
        
        conn = get_db()
        worker = conn.execute('SELECT id FROM workers WHERE unique_id = ?', (unique_worker_id,)).fetchone()
        
        if not worker:
            flash('Worker not found', 'error')
            return redirect(url_for('index'))
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('''INSERT INTO grievances 
                       (worker_id, unique_worker_id, issue_type, description, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (worker['id'], unique_worker_id, issue_type, description, created_at, created_at))
        conn.commit()
        conn.close()
        
        flash('Grievance submitted successfully!', 'success')
        return redirect(url_for('worker_profile', unique_id=unique_worker_id))
    except Exception as e:
        flash(f'Submission failed: {str(e)}', 'error')
        return redirect(url_for('index'))

# Job Opening Routes
@app.route('/jobs')
def job_list():
    conn = get_db()
    jobs = conn.execute("SELECT * FROM job_openings WHERE status = 'Active' ORDER BY posted_date DESC").fetchall()
    conn.close()
    return render_template('job_list.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    conn = get_db()
    job = conn.execute('SELECT * FROM job_openings WHERE id = ?', (job_id,)).fetchone()
    
    if not job:
        flash('Job not found', 'error')
        conn.close()
        return redirect(url_for('job_list'))
    
    # Count applications
    app_count = conn.execute('SELECT COUNT(*) as count FROM job_applications WHERE job_id = ?', (job_id,)).fetchone()['count']
    conn.close()
    
    return render_template('job_detail.html', job=job, app_count=app_count)

@app.route('/job/<int:job_id>/apply', methods=['POST'])
def apply_job(job_id):
    if 'worker_id' not in session:
        flash('Please login to apply for jobs', 'error')
        return redirect(url_for('worker_login'))
    
    cover_letter = request.form.get('cover_letter', '')
    
    conn = get_db()
    
    # Check if already applied
    existing = conn.execute('SELECT id FROM job_applications WHERE job_id = ? AND worker_id = ?',
                           (job_id, session['worker_id'])).fetchone()
    
    if existing:
        flash('You have already applied for this job', 'error')
        conn.close()
        return redirect(url_for('job_detail', job_id=job_id))
    
    application_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''INSERT INTO job_applications 
                   (job_id, worker_id, unique_worker_id, application_date, cover_letter)
                   VALUES (?, ?, ?, ?, ?)''',
                (job_id, session['worker_id'], session['worker_unique_id'], application_date, cover_letter))
    conn.commit()
    conn.close()
    
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('worker_dashboard'))

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM admin_users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['role'])
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    conn = get_db()
    
    total_workers = conn.execute('SELECT COUNT(*) as count FROM workers').fetchone()['count']
    total_grievances = conn.execute('SELECT COUNT(*) as count FROM grievances').fetchone()['count']
    pending_grievances = conn.execute("SELECT COUNT(*) as count FROM grievances WHERE status = 'Pending'").fetchone()['count']
    total_jobs = conn.execute('SELECT COUNT(*) as count FROM job_openings').fetchone()['count']
    active_jobs = conn.execute("SELECT COUNT(*) as count FROM job_openings WHERE status = 'Active'").fetchone()['count']
    total_applications = conn.execute('SELECT COUNT(*) as count FROM job_applications').fetchone()['count']
    pending_applications = conn.execute("SELECT COUNT(*) as count FROM job_applications WHERE status = 'Pending'").fetchone()['count']
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_registrations = conn.execute('SELECT COUNT(*) as count FROM workers WHERE DATE(registration_date) = ?', (today,)).fetchone()['count']
    
    recent_workers = conn.execute('SELECT * FROM workers ORDER BY id DESC LIMIT 5').fetchall()
    recent_grievances = conn.execute('SELECT * FROM grievances ORDER BY id DESC LIMIT 5').fetchall()
    recent_applications = conn.execute('''
        SELECT ja.*, w.name, jo.title 
        FROM job_applications ja
        JOIN workers w ON ja.worker_id = w.id
        JOIN job_openings jo ON ja.job_id = jo.id
        ORDER BY ja.application_date DESC LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    stats = {
        'total_workers': total_workers,
        'total_grievances': total_grievances,
        'pending_grievances': pending_grievances,
        'today_registrations': today_registrations,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications
    }
    
    return render_template('admin_dashboard.html', stats=stats, recent_workers=recent_workers, 
                         recent_grievances=recent_grievances, recent_applications=recent_applications)

@app.route('/admin/workers')
@login_required
def admin_workers():
    search = request.args.get('search', '')
    conn = get_db()
    
    if search:
        workers = conn.execute('''SELECT * FROM workers 
                                 WHERE unique_id LIKE ? OR name LIKE ? OR mobile LIKE ?
                                 ORDER BY id DESC''',
                              (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        workers = conn.execute('SELECT * FROM workers ORDER BY id DESC').fetchall()
    
    conn.close()
    return render_template('admin_workers.html', workers=workers, search=search)

@app.route('/admin/grievances')
@login_required
def admin_grievances():
    status_filter = request.args.get('status', '')
    conn = get_db()
    
    if status_filter:
        grievances = conn.execute('SELECT * FROM grievances WHERE status = ? ORDER BY id DESC', (status_filter,)).fetchall()
    else:
        grievances = conn.execute('SELECT * FROM grievances ORDER BY id DESC').fetchall()
    
    conn.close()
    return render_template('admin_grievances.html', grievances=grievances, status_filter=status_filter)

@app.route('/admin/update_status', methods=['POST'])
@login_required
def update_status():
    grievance_id = request.form['grievance_id']
    status = request.form['status']
    resolution_notes = request.form.get('resolution_notes', '')
    
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db()
    conn.execute('UPDATE grievances SET status = ?, resolution_notes = ?, updated_at = ? WHERE id = ?',
                (status, resolution_notes, updated_at, grievance_id))
    conn.commit()
    conn.close()
    
    flash('Grievance updated successfully!', 'success')
    return redirect(url_for('admin_grievances'))

@app.route('/admin/reports')
@login_required
def admin_reports():
    return render_template('admin_reports.html')

@app.route('/admin/download_workers_csv')
@login_required
def download_workers_csv():
    conn = get_db()
    workers = conn.execute('SELECT * FROM workers').fetchall()
    conn.close()
    
    from io import StringIO
    output = StringIO()
    
    writer = csv.writer(output)
    writer.writerow(['Unique ID', 'Name', 'Age', 'Gender', 'Mobile', 'Origin State', 
                    'TN Address', 'Employer', 'Skills', 'Emergency Contact', 'Registration Date'])
    
    for worker in workers:
        writer.writerow([worker['unique_id'], worker['name'], worker['age'], worker['gender'],
                        worker['mobile'], worker['origin_state'], worker['address_tn'],
                        worker['employer_name'], worker['skills'], worker['emergency_contact'],
                        worker['registration_date']])
    
    # Convert to bytes with BOM for Excel
    output_bytes = BytesIO()
    output_bytes.write('\ufeff'.encode('utf-8'))  # BOM for Excel
    output_bytes.write(output.getvalue().encode('utf-8'))
    output_bytes.seek(0)
    
    return send_file(output_bytes, as_attachment=True, 
                    download_name='workers_report.csv', mimetype='text/csv')

@app.route('/admin/download_grievances_csv')
@login_required
def download_grievances_csv():
    conn = get_db()
    grievances = conn.execute('SELECT * FROM grievances').fetchall()
    conn.close()
    
    from io import StringIO
    output = StringIO()
    
    writer = csv.writer(output)
    writer.writerow(['ID', 'Worker ID', 'Issue Type', 'Description', 'Status', 
                    'Created At', 'Updated At', 'Resolution Notes'])
    
    for g in grievances:
        writer.writerow([g['id'], g['unique_worker_id'], g['issue_type'], g['description'],
                        g['status'], g['created_at'], g['updated_at'], g['resolution_notes'] or ''])
    
    # Convert to bytes with BOM for Excel
    output_bytes = BytesIO()
    output_bytes.write('\ufeff'.encode('utf-8'))  # BOM for Excel
    output_bytes.write(output.getvalue().encode('utf-8'))
    output_bytes.seek(0)
    
    return send_file(output_bytes, as_attachment=True,
                    download_name='grievances_report.csv', mimetype='text/csv')

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = get_db()
            conn.execute('INSERT INTO admin_users (username, password_hash, role) VALUES (?, ?, ?)',
                        (username, password_hash, role))
            conn.commit()
            conn.close()
            flash('User added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
    
    return render_template('admin_add_user.html')

# Admin Job Management
@app.route('/admin/jobs')
@login_required
def admin_jobs():
    conn = get_db()
    jobs = conn.execute('SELECT * FROM job_openings ORDER BY posted_date DESC').fetchall()
    conn.close()
    return render_template('admin_jobs.html', jobs=jobs)

@app.route('/admin/job/create', methods=['GET', 'POST'])
@login_required
def create_job():
    if request.method == 'POST':
        title = request.form['title']
        company_name = request.form['company_name']
        location = request.form['location']
        job_type = request.form['job_type']
        salary_range = request.form['salary_range']
        description = request.form['description']
        requirements = request.form['requirements']
        vacancies = request.form['vacancies']
        deadline = request.form['deadline']
        
        posted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db()
        conn.execute('''INSERT INTO job_openings 
                       (title, company_name, location, job_type, salary_range, description, 
                        requirements, vacancies, posted_by, posted_date, deadline)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (title, company_name, location, job_type, salary_range, description,
                     requirements, vacancies, current_user.id, posted_date, deadline))
        conn.commit()
        conn.close()
        
        flash('Job opening created successfully!', 'success')
        return redirect(url_for('admin_jobs'))
    
    return render_template('admin_job_create.html')

@app.route('/admin/job/<int:job_id>/applications')
@login_required
def job_applications(job_id):
    conn = get_db()
    job = conn.execute('SELECT * FROM job_openings WHERE id = ?', (job_id,)).fetchone()
    
    if not job:
        flash('Job not found', 'error')
        conn.close()
        return redirect(url_for('admin_jobs'))
    
    applications = conn.execute('''
        SELECT ja.*, w.name, w.mobile, w.skills, w.origin_state
        FROM job_applications ja
        JOIN workers w ON ja.worker_id = w.id
        WHERE ja.job_id = ?
        ORDER BY ja.application_date DESC
    ''', (job_id,)).fetchall()
    
    conn.close()
    return render_template('admin_job_applications.html', job=job, applications=applications)

@app.route('/admin/job/application/<int:app_id>/update', methods=['POST'])
@login_required
def update_application_status(app_id):
    status = request.form['status']
    admin_notes = request.form.get('admin_notes', '')
    
    conn = get_db()
    conn.execute('UPDATE job_applications SET status = ?, admin_notes = ? WHERE id = ?',
                (status, admin_notes, app_id))
    conn.commit()
    conn.close()
    
    flash('Application status updated!', 'success')
    return redirect(request.referrer or url_for('admin_jobs'))

@app.route('/admin/job/<int:job_id>/toggle_status', methods=['POST'])
@login_required
def toggle_job_status(job_id):
    conn = get_db()
    job = conn.execute('SELECT status FROM job_openings WHERE id = ?', (job_id,)).fetchone()
    
    if job:
        new_status = 'Closed' if job['status'] == 'Active' else 'Active'
        conn.execute('UPDATE job_openings SET status = ? WHERE id = ?', (new_status, job_id))
        conn.commit()
        flash(f'Job status changed to {new_status}', 'success')
    
    conn.close()
    return redirect(url_for('admin_jobs'))

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
