CREATE_BLOG_POSTS_TABLE = """
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        blog_id VARCHAR(255) UNIQUE NOT NULL,
        title VARCHAR(500) NOT NULL,
        sub_title VARCHAR(500),
        category VARCHAR(100),
        post_content TEXT,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        author_id INTEGER,
        status VARCHAR(20) DEFAULT 'published'
    );
"""

CREATE_BLOG_ANALYTICS_TABLE = """
    CREATE TABLE IF NOT EXISTS blog_analytics (
        id SERIAL PRIMARY KEY,
        blog_id VARCHAR(255) NOT NULL,
        user_id INTEGER,
        view_count INTEGER DEFAULT 0,
        read_time_seconds INTEGER,
        scroll_depth_percentage INTEGER,
        time_on_page_seconds INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(45),
        user_agent TEXT
    );
"""

CREATE_BLOG_ENGAGEMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS blog_engagement (
        id SERIAL PRIMARY KEY,
        blog_id VARCHAR(255) NOT NULL,
        user_id INTEGER,
        engagement_type VARCHAR(50) NOT NULL,
        engagement_data JSONB,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_BLOG_CATEGORIES_TABLE = """
    CREATE TABLE IF NOT EXISTS blog_categories (
        id SERIAL PRIMARY KEY,
        category_name VARCHAR(100) UNIQUE NOT NULL,
        category_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
