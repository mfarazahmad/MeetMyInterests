CREATE_MEDIA_MOVIES_TABLE = """
    CREATE TABLE IF NOT EXISTS media_movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        genre VARCHAR(100),
        release_year INTEGER,
        director VARCHAR(255),
        rating DECIMAL(3,1),
        user_rating INTEGER,
        watch_date DATE,
        watch_duration_minutes INTEGER,
        platform VARCHAR(100),
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_MEDIA_GAMES_TABLE = """
    CREATE TABLE IF NOT EXISTS media_games (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        genre VARCHAR(100),
        platform VARCHAR(100),
        developer VARCHAR(255),
        publisher VARCHAR(255),
        release_date DATE,
        play_time_hours DECIMAL(6,2),
        user_rating INTEGER,
        completion_status VARCHAR(50),
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_MEDIA_CONSUMPTION_TABLE = """
    CREATE TABLE IF NOT EXISTS media_consumption (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        media_type VARCHAR(50) NOT NULL,
        media_id VARCHAR(255),
        consumption_date DATE NOT NULL,
        duration_minutes INTEGER,
        platform VARCHAR(100),
        rating INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_MEDIA_PLATFORMS_TABLE = """
    CREATE TABLE IF NOT EXISTS media_platforms (
        id SERIAL PRIMARY KEY,
        platform_name VARCHAR(100) NOT NULL,
        platform_type VARCHAR(50),
        subscription_cost DECIMAL(8,2),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_MEDIA_ANALYTICS_TABLE = """
    CREATE TABLE IF NOT EXISTS media_analytics (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        media_type VARCHAR(50) NOT NULL,
        total_consumption_hours DECIMAL(8,2),
        favorite_genre VARCHAR(100),
        average_rating DECIMAL(3,2),
        analytics_period VARCHAR(20),
        period_start_date DATE,
        period_end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
