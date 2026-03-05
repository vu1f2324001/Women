"""
EmpowerHer - Women-Centric Website
Flask Backend Application

This application provides backend support for:
- Women Achievers showcase
- Business Ideas submission and display
- Job Listings management
- Contact form submissions

User Types:
1. Visitor/General User - Read content, browse, submit forms
2. Admin/Manager - Full CRUD operations on all tables
"""

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get secret key from environment variable or use a default for development
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')

# Database configuration
DATABASE = os.getenv('DATABASE_NAME', 'database.db')

# Admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# ==================== DATABASE FUNCTIONS ====================

def get_db_connection():
    """Get database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with all required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Women_Achievers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS women_achievers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            achievement TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            month TEXT,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Business_Ideas table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            contact_email TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Job_Listings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            requirements TEXT,
            category TEXT,
            job_type TEXT,
            posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Contact_Messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Newsletter subscriptions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Scholarships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            provider TEXT NOT NULL,
            amount TEXT NOT NULL,
            eligibility TEXT,
            deadline TEXT,
            link TEXT,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Online Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS online_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            provider TEXT NOT NULL,
            category TEXT,
            level TEXT,
            duration TEXT,
            link TEXT,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Health Tips table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            icon TEXT,
            content TEXT NOT NULL,
            display_order INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Health Articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            tag TEXT,
            description TEXT,
            image_emoji TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Health Videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Health Resources table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            icon TEXT,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Safe Locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS safe_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            latitude REAL,
            longitude REAL,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# ==================== HELPER FUNCTIONS ====================

def seed_sample_data():
    """Add sample data for demonstration purposes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM women_achievers')
    if cursor.fetchone()[0] == 0:
        # Sample Women Achievers
        achievers = [
            ('Dr. Maya Sharma', 'Innovative Healthcare Solution', 'Health', 
             'Developed an AI-powered diagnostic tool for early breast cancer detection', 
             'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400', 'January', 2024),
            ('Priya Patel', 'Tech Startup Founder', 'Entrepreneurship',
             'Founded a successful EdTech company serving 1M+ students',
             'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400', 'February', 2024),
            ('Dr. Amita Singh', 'Research Scientist', 'Education',
             'Published 50+ research papers in top journals',
             'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=400', 'March', 2024),
            ('Sunita Devi', 'Women Safety Advocate', 'Safety',
             'Created a safety app used by 500K+ women',
             'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400', 'April', 2024),
        ]
        cursor.executemany(
            'INSERT INTO women_achievers (name, achievement, category, description, image_url, month, year) VALUES (?, ?, ?, ?, ?, ?, ?)',
            achievers
        )
        
        # Sample Job Listings
        jobs = [
            ('Software Engineer', 'TechWomen Inc.', 'Remote', 
             'Build scalable web applications', '3+ years experience, Python, JavaScript',
             'Technology', 'Full-time'),
            ('Marketing Manager', 'GrowthHub', 'Mumbai',
             'Lead marketing campaigns', '5+ years experience in digital marketing',
             'Marketing', 'Full-time'),
            ('Data Analyst', 'DataViz Corp', 'Bangalore',
             'Analyze business data', 'Statistics, Python, SQL knowledge',
             'Technology', 'Full-time'),
            ('Content Writer', 'WriteSpace', 'Work from Home',
             'Create engaging content', 'Excellent English writing skills',
             'Content', 'Part-time'),
        ]
        cursor.executemany(
            'INSERT INTO job_listings (title, company, location, description, requirements, category, job_type) VALUES (?, ?, ?, ?, ?, ?, ?)',
            jobs
        )
        
        # Sample Business Ideas
        ideas = [
            ('Anita Joshi', 'Eco-Friendly Packaging', 
             'Biodegradable packaging solutions for small businesses', 'Sustainability', 'anita@email.com', 'approved'),
            ('Rashmi Verma', 'Women Health App',
             'Mobile app for women health tracking and consultation', 'Health Tech', 'rashmi@email.com', 'approved'),
            ('Kavya Nair', 'Skill Development Center',
             'Free skill training for underprivileged women', 'Education', 'kavya@email.com', 'pending'),
        ]
        cursor.executemany(
            'INSERT INTO business_ideas (name, title, description, category, contact_email, status) VALUES (?, ?, ?, ?, ?, ?)',
            ideas
        )
        
        conn.commit()
        print("Sample data seeded successfully!")
    
    conn.close()

# ==================== ADMIN DECORATOR ====================

def admin_required(f):
    """Decorator to require admin login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login as admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page with hero section and featured achievers."""
    conn = get_db_connection()
    achievers = conn.execute('SELECT * FROM women_achievers ORDER BY created_at DESC LIMIT 6').fetchall()
    conn.close()
    return render_template('index.html', achievers=achievers)

@app.route('/health')
def health():
    """Health section with tips, articles, and videos."""
    conn = get_db_connection()
    db_tips = conn.execute('SELECT * FROM health_tips WHERE is_active = 1 ORDER BY display_order, created_at DESC').fetchall()
    db_articles = conn.execute('SELECT * FROM health_articles WHERE is_active = 1 ORDER BY created_at DESC').fetchall()
    db_videos = conn.execute('SELECT * FROM health_videos WHERE is_active = 1 ORDER BY created_at DESC').fetchall()
    db_resources = conn.execute('SELECT * FROM health_resources WHERE is_active = 1 ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Use database tips if available, otherwise use default ones
    if db_tips:
        tips = db_tips
    else:
        tips = [
            {'title': 'Regular Health Check-ups', 'icon': '🩺',
             'content': 'Schedule annual health check-ups to detect potential issues early.'},
            {'title': 'Mental Wellness', 'icon': '🧘',
             'content': 'Practice meditation and mindfulness for mental peace.'},
            {'title': 'Nutrition & Diet', 'icon': '🥗',
             'content': 'Maintain a balanced diet rich in vitamins and minerals.'},
            {'title': 'Exercise Daily', 'icon': '🏃',
             'content': '30 minutes of exercise improves physical and mental health.'},
            {'title': 'Sleep Well', 'icon': '😴',
             'content': '7-8 hours of quality sleep is essential for overall wellness.'},
            {'title': 'Hydration', 'icon': '💧',
             'content': 'Drink at least 8 glasses of water daily.'},
        ]
    
    articles = db_articles if db_articles else []
    videos = db_videos if db_videos else []
    resources = db_resources if db_resources else []
    
    return render_template('health.html', tips=tips, articles=articles, videos=videos, resources=resources)

@app.route('/education')
def education():
    """Education section with courses, scholarships, and mentors."""
    conn = get_db_connection()
    achievers = conn.execute('SELECT * FROM women_achievers ORDER BY created_at DESC LIMIT 4').fetchall()
    scholarships = conn.execute('SELECT * FROM scholarships WHERE is_active = 1').fetchall()
    db_courses = conn.execute('SELECT * FROM online_courses WHERE is_active = 1').fetchall()
    conn.close()
    
    # Use database courses if available, otherwise use default ones
    if db_courses:
        courses = db_courses
    else:
        courses = [
            {'title': 'Digital Marketing Fundamentals', 'provider': 'Google Digital Garage', 
             'category': 'Marketing', 'level': 'Beginner', 'duration': '40 hours'},
            {'title': 'Python Programming', 'provider': 'Coursera',
             'category': 'Technology', 'level': 'Beginner', 'duration': '30 hours'},
            {'title': 'Financial Literacy', 'provider': 'NSE Academy',
             'category': 'Finance', 'level': 'Intermediate', 'duration': '20 hours'},
            {'title': 'Leadership Skills', 'provider': 'Harvard Online',
             'category': 'Leadership', 'level': 'Advanced', 'duration': '25 hours'},
        ]
    
    # If no scholarships in DB, show default ones
    if not scholarships:
        scholarships = [
            {'name': 'Pre-Matric Scholarship', 'provider': 'Government of India', 'amount': '₹50,000/year'},
            {'name': 'Women in Tech Scholarship', 'provider': 'Microsoft', 'amount': '₹1,00,000'},
            {'name': 'Merit cum Means Scholarship', 'provider': 'Various NGOs', 'amount': '₹75,000/year'},
        ]
    
    return render_template('education.html', courses=courses, scholarships=scholarships, mentors=achievers)

@app.route('/safety')
def safety():
    """Safety section with emergency contacts and resources."""
    conn = get_db_connection()
    db_locations = conn.execute('SELECT * FROM safe_locations WHERE is_active = 1 ORDER BY type, created_at DESC').fetchall()
    conn.close()
    
    emergency_contacts = [
        {'name': 'Women Helpline', 'number': '1091', 'description': '24/7 Emergency assistance'},
        {'name': 'Police Emergency', 'number': '100', 'description': 'Police emergency services'},
        {'name': 'Women Safety App', 'number': '112', 'description': 'National emergency response'},
        {'name': 'Domestic Violence Helpline', 'number': '181', 'description': 'Domestic violence support'},
        {'name': 'Mental Health Helpline', 'number': '1800-599-0019', 'description': 'Mental health support'},
    ]
    
    # Convert locations to list for template
    locations = [dict(row) for row in db_locations] if db_locations else []
    
    return render_template('safety.html', contacts=emergency_contacts, locations=locations)

@app.route('/entrepreneurship')
def entrepreneurship():
    """Entrepreneurship section with business ideas."""
    conn = get_db_connection()
    ideas = conn.execute("SELECT * FROM business_ideas WHERE status = 'approved' ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template('entrepreneurship.html', ideas=ideas)

@app.route('/career')
def career():
    """Career section with job listings."""
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM job_listings WHERE is_active = 1 ORDER BY posted_date DESC').fetchall()
    conn.close()
    return render_template('career.html', jobs=jobs)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if name and email and message:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                (name, email, subject, message)
            )
            conn.commit()
            conn.close()
            flash('Message sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('contact.html')

# ==================== FORM SUBMISSIONS ====================

@app.route('/submit_business_idea', methods=['POST'])
def submit_business_idea():
    """Submit a new business idea."""
    name = request.form.get('name')
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    email = request.form.get('email')
    
    if name and title and description and email:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO business_ideas (name, title, description, category, contact_email, status) VALUES (?, ?, ?, ?, ?, ?)',
            (name, title, description, category, email, 'pending')
        )
        conn.commit()
        conn.close()
        flash('Business idea submitted successfully! It will be reviewed shortly.', 'success')
    else:
        flash('Please fill in all required fields.', 'error')
    
    return redirect(url_for('entrepreneurship'))

@app.route('/subscribe_newsletter', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter."""
    email = request.form.get('email')
    
    if email:
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO newsletter_subscribers (email) VALUES (?)', (email,))
            conn.commit()
            conn.close()
            flash('Successfully subscribed to our newsletter!', 'success')
        except sqlite3.IntegrityError:
            flash('This email is already subscribed.', 'error')
    else:
        flash('Please enter a valid email address.', 'error')
    
    return redirect(url_for('index'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check against environment variables
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with overview."""
    conn = get_db_connection()
    
    stats = {
        'achievers': conn.execute('SELECT COUNT(*) FROM women_achievers').fetchone()[0],
        'ideas': conn.execute('SELECT COUNT(*) FROM business_ideas').fetchone()[0],
        'jobs': conn.execute('SELECT COUNT(*) FROM job_listings').fetchone()[0],
        'messages': conn.execute('SELECT COUNT(*) FROM contact_messages').fetchone()[0],
        'courses': conn.execute('SELECT COUNT(*) FROM online_courses').fetchone()[0],
        'scholarships': conn.execute('SELECT COUNT(*) FROM scholarships').fetchone()[0],
    }
    
    recent_messages = conn.execute('SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 5').fetchall()
    pending_ideas = conn.execute("SELECT * FROM business_ideas WHERE status = 'pending' ORDER BY created_at DESC").fetchall()
    rejected_ideas = conn.execute("SELECT * FROM business_ideas WHERE status = 'rejected' ORDER BY created_at DESC").fetchall()
    approved_ideas = conn.execute("SELECT * FROM business_ideas WHERE status = 'approved' ORDER BY created_at DESC").fetchall()
    
    conn.close()
    return render_template('admin/dashboard.html', stats=stats, messages=recent_messages, pending_ideas=pending_ideas, rejected_ideas=rejected_ideas, approved_ideas=approved_ideas)

@app.route('/admin/achievers')
@admin_required
def admin_achievers():
    """Manage women achievers."""
    conn = get_db_connection()
    achievers = conn.execute('SELECT * FROM women_achievers ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin/achievers.html', achievers=achievers)

@app.route('/admin/achievers/add', methods=['POST'])
@admin_required
def admin_add_achiever():
    """Add new achiever."""
    name = request.form.get('name')
    achievement = request.form.get('achievement')
    category = request.form.get('category')
    description = request.form.get('description')
    image_url = request.form.get('image_url')
    month = request.form.get('month')
    year = request.form.get('year')
    
    if name and achievement:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO women_achievers (name, achievement, category, description, image_url, month, year) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, achievement, category, description, image_url, month, year)
        )
        conn.commit()
        conn.close()
        flash('Achiever added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_achievers'))

@app.route('/admin/achievers/delete/<int:id>')
@admin_required
def admin_delete_achiever(id):
    """Delete achiever."""
    conn = get_db_connection()
    conn.execute('DELETE FROM women_achievers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Achiever deleted successfully!', 'success')
    return redirect(url_for('admin_achievers'))

@app.route('/admin/ideas')
@admin_required
def admin_ideas():
    """Manage business ideas."""
    conn = get_db_connection()
    ideas = conn.execute('SELECT * FROM business_ideas ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin/ideas.html', ideas=ideas)

@app.route('/admin/ideas/approve/<int:id>')
@admin_required
def admin_approve_idea(id):
    """Approve business idea."""
    conn = get_db_connection()
    conn.execute("UPDATE business_ideas SET status = 'approved' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Business idea approved!', 'success')
    return redirect(url_for('admin_ideas'))

@app.route('/admin/ideas/reject/<int:id>')
@admin_required
def admin_reject_idea(id):
    """Reject business idea."""
    conn = get_db_connection()
    conn.execute("UPDATE business_ideas SET status = 'rejected' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Business idea rejected.', 'success')
    return redirect(url_for('admin_ideas'))

@app.route('/admin/jobs')
@admin_required
def admin_jobs():
    """Manage job listings."""
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM job_listings ORDER BY posted_date DESC').fetchall()
    conn.close()
    return render_template('admin/jobs.html', jobs=jobs)

@app.route('/admin/jobs/add', methods=['POST'])
@admin_required
def admin_add_job():
    """Add new job listing."""
    title = request.form.get('title')
    company = request.form.get('company')
    location = request.form.get('location')
    description = request.form.get('description')
    requirements = request.form.get('requirements')
    category = request.form.get('category')
    job_type = request.form.get('job_type')
    
    if title and company:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO job_listings (title, company, location, description, requirements, category, job_type) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, company, location, description, requirements, category, job_type)
        )
        conn.commit()
        conn.close()
        flash('Job listing added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_jobs'))

@app.route('/admin/jobs/delete/<int:id>')
@admin_required
def admin_delete_job(id):
    """Delete job listing."""
    conn = get_db_connection()
    conn.execute('DELETE FROM job_listings WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Job listing deleted successfully!', 'success')
    return redirect(url_for('admin_jobs'))

@app.route('/admin/messages')
@admin_required
def admin_messages():
    """View contact messages."""
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/scholarships')
@admin_required
def admin_scholarships():
    """Manage scholarships."""
    conn = get_db_connection()
    scholarships = conn.execute('SELECT * FROM scholarships ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin/scholarships.html', scholarships=scholarships)

@app.route('/admin/scholarships/add', methods=['POST'])
@admin_required
def admin_add_scholarship():
    """Add new scholarship."""
    name = request.form.get('name')
    provider = request.form.get('provider')
    amount = request.form.get('amount')
    eligibility = request.form.get('eligibility')
    deadline = request.form.get('deadline')
    link = request.form.get('link')
    description = request.form.get('description')
    
    if name and provider and amount:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO scholarships (name, provider, amount, eligibility, deadline, link, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, provider, amount, eligibility, deadline, link, description)
        )
        conn.commit()
        conn.close()
        flash('Scholarship added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_scholarships'))

@app.route('/admin/scholarships/delete/<int:id>')
@admin_required
def admin_delete_scholarship(id):
    """Delete scholarship."""
    conn = get_db_connection()
    conn.execute('DELETE FROM scholarships WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Scholarship deleted successfully!', 'success')
    return redirect(url_for('admin_scholarships'))

@app.route('/admin/courses')
@admin_required
def admin_courses():
    """Manage online courses."""
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM online_courses ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['POST'])
@admin_required
def admin_add_course():
    """Add new online course."""
    title = request.form.get('title')
    provider = request.form.get('provider')
    category = request.form.get('category')
    level = request.form.get('level')
    duration = request.form.get('duration')
    link = request.form.get('link')
    description = request.form.get('description')
    
    if title and provider:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO online_courses (title, provider, category, level, duration, link, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, provider, category, level, duration, link, description)
        )
        conn.commit()
        conn.close()
        flash('Course added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/courses/delete/<int:id>')
@admin_required
def admin_delete_course(id):
    """Delete online course."""
    conn = get_db_connection()
    conn.execute('DELETE FROM online_courses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin_courses'))

# Health Content Admin Routes
@app.route('/admin/health')
@admin_required
def admin_health():
    """Manage health content."""
    conn = get_db_connection()
    tips = conn.execute('SELECT * FROM health_tips ORDER BY display_order, created_at DESC').fetchall()
    articles = conn.execute('SELECT * FROM health_articles ORDER BY created_at DESC').fetchall()
    videos = conn.execute('SELECT * FROM health_videos ORDER BY created_at DESC').fetchall()
    resources = conn.execute('SELECT * FROM health_resources ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin/health.html', tips=tips, articles=articles, videos=videos, resources=resources)

@app.route('/admin/health/tips/add', methods=['POST'])
@admin_required
def admin_add_health_tip():
    """Add new health tip."""
    title = request.form.get('title')
    icon = request.form.get('icon')
    content = request.form.get('content')
    display_order = request.form.get('display_order') or 0
    
    if title and content:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO health_tips (title, icon, content, display_order) VALUES (?, ?, ?, ?)',
            (title, icon, content, display_order)
        )
        conn.commit()
        conn.close()
        flash('Health tip added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_health'))

@app.route('/admin/health/tips/delete/<int:id>')
@admin_required
def admin_delete_health_tip(id):
    """Delete health tip."""
    conn = get_db_connection()
    conn.execute('DELETE FROM health_tips WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Health tip deleted successfully!', 'success')
    return redirect(url_for('admin_health'))

@app.route('/admin/health/articles/add', methods=['POST'])
@admin_required
def admin_add_health_article():
    """Add new health article."""
    title = request.form.get('title')
    tag = request.form.get('tag')
    description = request.form.get('description')
    image_emoji = request.form.get('image_emoji')
    
    if title and description:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO health_articles (title, tag, description, image_emoji) VALUES (?, ?, ?, ?)',
            (title, tag, description, image_emoji)
        )
        conn.commit()
        conn.close()
        flash('Health article added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_health'))

@app.route('/admin/health/articles/delete/<int:id>')
@admin_required
def admin_delete_health_article(id):
    """Delete health article."""
    conn = get_db_connection()
    conn.execute('DELETE FROM health_articles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Health article deleted successfully!', 'success')
    return redirect(url_for('admin_health'))

@app.route('/admin/health/videos/add', methods=['POST'])
@admin_required
def admin_add_health_video():
    """Add new health video."""
    title = request.form.get('title')
    description = request.form.get('description')
    
    if title:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO health_videos (title, description) VALUES (?, ?)',
            (title, description)
        )
        conn.commit()
        conn.close()
        flash('Health video added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_health'))

@app.route('/admin/health/videos/delete/<int:id>')
@admin_required
def admin_delete_health_video(id):
    """Delete health video."""
    conn = get_db_connection()
    conn.execute('DELETE FROM health_videos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Health video deleted successfully!', 'success')
    return redirect(url_for('admin_health'))

@app.route('/admin/health/resources/add', methods=['POST'])
@admin_required
def admin_add_health_resource():
    """Add new health resource."""
    title = request.form.get('title')
    icon = request.form.get('icon')
    description = request.form.get('description')
    
    if title:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO health_resources (title, icon, description) VALUES (?, ?, ?)',
            (title, icon, description)
        )
        conn.commit()
        conn.close()
        flash('Health resource added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_health'))

@app.route('/admin/health/resources/delete/<int:id>')
@admin_required
def admin_delete_health_resource(id):
    """Delete health resource."""
    conn = get_db_connection()
    conn.execute('DELETE FROM health_resources WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Health resource deleted successfully!', 'success')
    return redirect(url_for('admin_health'))

# Safe Locations Admin Routes
@app.route('/admin/safety')
@admin_required
def admin_safety():
    """Manage safe locations."""
    conn = get_db_connection()
    locations = conn.execute('SELECT * FROM safe_locations ORDER BY type, created_at DESC').fetchall()
    conn.close()
    return render_template('admin/safety.html', locations=locations)

@app.route('/admin/safety/locations/add', methods=['POST'])
@admin_required
def admin_add_safe_location():
    """Add new safe location."""
    name = request.form.get('name')
    loc_type = request.form.get('type')
    address = request.form.get('address')
    phone = request.form.get('phone')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    description = request.form.get('description')
    
    if name and loc_type:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO safe_locations (name, type, address, phone, latitude, longitude, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, loc_type, address, phone, latitude, longitude, description)
        )
        conn.commit()
        conn.close()
        flash('Safe location added successfully!', 'success')
    else:
        flash('Please fill in required fields.', 'error')
    
    return redirect(url_for('admin_safety'))

@app.route('/admin/safety/locations/delete/<int:id>')
@admin_required
def admin_delete_safe_location(id):
    """Delete safe location."""
    conn = get_db_connection()
    conn.execute('DELETE FROM safe_locations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Safe location deleted successfully!', 'success')
    return redirect(url_for('admin_safety'))

# ==================== ERROR HANDLERS ====================

@app.route('/.well-known/appspecific/<path:filename>')
def well_known_appspecific(filename):
    """Handle Chrome DevTools well-known requests to prevent 404 errors."""
    # Chrome makes internal requests to this path when DevTools is open
    # Return an empty JSON object to satisfy the request
    from flask import jsonify
    return jsonify({})

@app.errorhandler(404)
def not_found(e):
    """404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """500 error page."""
    return render_template('500.html'), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Initialize database
    if not os.path.exists(DATABASE):
        init_database()
        seed_sample_data()
    else:
        init_database()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5010)

