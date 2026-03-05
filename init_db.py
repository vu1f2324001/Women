"""
Database Initialization Script for EmpowerHer
Creates all required tables and seeds sample data

Usage:
    python init_db.py

For Render deployment, run this script after deployment to create tables.
"""

import sqlite3
import os
import sys

# Get database path from environment variable or use default
DATABASE = os.getenv('DATABASE_NAME', 'database.db')

def get_db_connection():
    """Get database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create all required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Creating tables...")
    
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
    print("✓ women_achievers table created")
    
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
    print("✓ business_ideas table created")
    
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
    print("✓ job_listings table created")
    
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
    print("✓ contact_messages table created")
    
    # Newsletter subscriptions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ newsletter_subscribers table created")
    
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
    print("✓ admin_users table created")
    
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
    print("✓ scholarships table created")
    
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
    print("✓ online_courses table created")
    
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
    print("✓ health_tips table created")
    
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
    print("✓ health_articles table created")
    
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
    print("✓ health_videos table created")
    
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
    print("✓ health_resources table created")
    
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
    print("✓ safe_locations table created")
    
    conn.commit()
    conn.close()
    print("\n✅ All tables created successfully!")
    return True

def seed_sample_data():
    """Add sample data for demonstration purposes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM women_achievers')
    if cursor.fetchone()[0] == 0:
        print("\nSeeding sample data...")
        
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
        print("✓ Added 4 sample achievers")
        
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
        print("✓ Added 4 sample jobs")
        
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
        print("✓ Added 3 sample business ideas")
        
        conn.commit()
        print("\n✅ Sample data seeded successfully!")
    else:
        print("\n📋 Sample data already exists, skipping seed.")
    
    conn.close()

def main():
    """Main function to initialize database."""
    print(f"Initializing database: {DATABASE}")
    print("=" * 50)
    
    try:
        # Create tables
        create_tables()
        
        # Seed sample data
        seed_sample_data()
        
        print("\n" + "=" * 50)
        print("🎉 Database initialization complete!")
        print(f"Database file: {os.path.abspath(DATABASE)}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

