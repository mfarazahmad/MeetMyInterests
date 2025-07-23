# Service Analytics Database Schema

This document describes the database schema for the service-analytics project. The database uses PostgreSQL and is designed to track analytics data across multiple services including fitness tracking, blog analytics, media consumption, and general user analytics.

## Database Overview

The database is organized into four main categories:
- **Analytics**: User sessions, activity tracking, and general analytics events
- **Blog**: Blog posts, analytics, and engagement tracking
- **Fitness**: Comprehensive fitness tracking including programs, exercises, workouts, and measurements
- **Media**: Media consumption tracking for movies, games, and other media

## Table Structure

### Analytics Tables

#### users
Stores user information and demographics.
```sql
- id (SERIAL PRIMARY KEY)
- username (VARCHAR(100) UNIQUE NOT NULL)
- email (VARCHAR(255) UNIQUE NOT NULL)
- name (VARCHAR(100))
- tdee (INTEGER) -- Total Daily Energy Expenditure
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- updated_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### user_sessions
Tracks user login sessions and session metadata.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER REFERENCES users(id))
- session_id (VARCHAR(255) UNIQUE NOT NULL)
- login_time (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- logout_time (TIMESTAMP)
- ip_address (VARCHAR(45))
- user_agent (TEXT)
- is_active (BOOLEAN DEFAULT TRUE)
```

#### user_activity
Tracks user activity and interactions.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER REFERENCES users(id))
- activity_type (VARCHAR(50) NOT NULL)
- activity_data (JSONB)
- timestamp (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- page_url (VARCHAR(500))
- session_id (VARCHAR(255))
```

#### analytics_events
General analytics events for tracking user behavior.
```sql
- id (SERIAL PRIMARY KEY)
- event_name (VARCHAR(100) NOT NULL)
- event_category (VARCHAR(50))
- event_data (JSONB)
- user_id (INTEGER REFERENCES users(id))
- timestamp (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- session_id (VARCHAR(255))
```

### Blog Tables

#### blog_posts
Stores blog post information.
```sql
- id (SERIAL PRIMARY KEY)
- blog_id (VARCHAR(255) UNIQUE NOT NULL)
- title (VARCHAR(500) NOT NULL)
- sub_title (VARCHAR(500))
- category (VARCHAR(100))
- post_content (TEXT)
- date_created (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- date_updated (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- author_id (INTEGER)
- status (VARCHAR(20) DEFAULT 'published')
```

#### blog_analytics
Tracks blog post analytics and engagement metrics.
```sql
- id (SERIAL PRIMARY KEY)
- blog_id (VARCHAR(255) NOT NULL)
- user_id (INTEGER)
- view_count (INTEGER DEFAULT 0)
- read_time_seconds (INTEGER)
- scroll_depth_percentage (INTEGER)
- time_on_page_seconds (INTEGER)
- timestamp (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- ip_address (VARCHAR(45))
- user_agent (TEXT)
```

#### blog_engagement
Tracks user engagement with blog posts.
```sql
- id (SERIAL PRIMARY KEY)
- blog_id (VARCHAR(255) NOT NULL)
- user_id (INTEGER)
- engagement_type (VARCHAR(50) NOT NULL)
- engagement_data (JSONB)
- timestamp (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### blog_categories
Stores blog post categories.
```sql
- id (SERIAL PRIMARY KEY)
- category_name (VARCHAR(100) UNIQUE NOT NULL)
- category_description (TEXT)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

### Fitness Tables

#### fitness_programs
Stores workout programs and their configurations.
```sql
- id (SERIAL PRIMARY KEY)
- program_name (VARCHAR(255) NOT NULL)
- program_type (VARCHAR(50) NOT NULL)
- frequency (INTEGER NOT NULL)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- updated_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- user_id (INTEGER)
- status (VARCHAR(20) DEFAULT 'active')
```

#### fitness_exercises
Stores exercise definitions and metadata.
```sql
- id (SERIAL PRIMARY KEY)
- exercise_name (VARCHAR(255) NOT NULL)
- exercise_type (VARCHAR(50) NOT NULL)
- body_part (VARCHAR(100))
- movement_type (VARCHAR(50))
- equipment_needed (TEXT[])
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_program_exercises
Links exercises to programs with specific configurations.
```sql
- id (SERIAL PRIMARY KEY)
- program_id (INTEGER REFERENCES fitness_programs(id))
- exercise_id (INTEGER REFERENCES fitness_exercises(id))
- workout_day (VARCHAR(10))
- recommended_sets (INTEGER)
- recommended_reps (INTEGER)
- recommended_volume (VARCHAR(100))
- band_weight_multiplier (DECIMAL(5,2))
- alternative_exercise_id (INTEGER REFERENCES fitness_exercises(id))
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_workouts
Stores individual workout sessions.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER)
- program_id (INTEGER REFERENCES fitness_programs(id))
- workout_date (DATE NOT NULL)
- workout_notes (TEXT)
- total_duration_minutes (INTEGER)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_exercise_logs
Stores individual exercise sets and performance data.
```sql
- id (SERIAL PRIMARY KEY)
- workout_id (INTEGER REFERENCES fitness_workouts(id))
- exercise_id (INTEGER REFERENCES fitness_exercises(id))
- sets (INTEGER NOT NULL)
- reps (INTEGER NOT NULL)
- weight (DECIMAL(8,2))
- duration_seconds (INTEGER)
- notes (TEXT)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_measurements
Stores body measurements and tracking data.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER)
- measurement_date (DATE NOT NULL)
- height (DECIMAL(5,2))
- chest (DECIMAL(5,2))
- bicep (DECIMAL(5,2))
- tricep (DECIMAL(5,2))
- thighs (DECIMAL(5,2))
- calves (DECIMAL(5,2))
- waist (DECIMAL(5,2))
- neck (DECIMAL(5,2))
- weight (DECIMAL(6,2))
- body_fat_percentage (DECIMAL(4,2))
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_equipment
Stores fitness equipment definitions.
```sql
- id (SERIAL PRIMARY KEY)
- equipment_name (VARCHAR(255) NOT NULL)
- equipment_type (VARCHAR(100))
- description (TEXT)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_bands
Stores resistance band specifications.
```sql
- id (SERIAL PRIMARY KEY)
- band_name (VARCHAR(100) NOT NULL)
- band_type (VARCHAR(50))
- low_weight (INTEGER)
- single_weight (INTEGER)
- color (VARCHAR(50))
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_goals
Stores user fitness goals and targets.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER)
- goal_type (VARCHAR(50) NOT NULL)
- goal_target (JSONB)
- goal_deadline (DATE)
- goal_status (VARCHAR(20) DEFAULT 'active')
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- updated_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### fitness_nutrition
Stores nutrition tracking data.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER)
- nutrition_date (DATE NOT NULL)
- calories (INTEGER)
- protein_grams (DECIMAL(6,2))
- carbs_grams (DECIMAL(6,2))
- fat_grams (DECIMAL(6,2))
- water_ounces (DECIMAL(6,2))
- notes (TEXT)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

### Media Tables

#### media_movies
Stores movie consumption data.
```sql
- id (SERIAL PRIMARY KEY)
- title (VARCHAR(255) NOT NULL)
- genre (VARCHAR(100))
- release_year (INTEGER)
- director (VARCHAR(255))
- rating (DECIMAL(3,1))
- user_rating (INTEGER)
- watch_date (DATE)
- watch_duration_minutes (INTEGER)
- platform (VARCHAR(100))
- user_id (INTEGER)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### media_games
Stores gaming data and play statistics.
```sql
- id (SERIAL PRIMARY KEY)
- title (VARCHAR(255) NOT NULL)
- genre (VARCHAR(100))
- platform (VARCHAR(100))
- developer (VARCHAR(255))
- publisher (VARCHAR(255))
- release_date (DATE)
- play_time_hours (DECIMAL(6,2))
- user_rating (INTEGER)
- completion_status (VARCHAR(50))
- user_id (INTEGER)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### media_consumption
General media consumption tracking.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER)
- media_type (VARCHAR(50) NOT NULL)
- media_id (VARCHAR(255))
- consumption_date (DATE NOT NULL)
- duration_minutes (INTEGER)
- platform (VARCHAR(100))
- rating (INTEGER)
- notes (TEXT)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### media_platforms
Stores media platform information.
```sql
- id (SERIAL PRIMARY KEY)
- platform_name (VARCHAR(100) NOT NULL)
- platform_type (VARCHAR(50))
- subscription_cost (DECIMAL(8,2))
- description (TEXT)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

#### media_analytics
Aggregated media consumption analytics.
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER)
- media_type (VARCHAR(50) NOT NULL)
- total_consumption_hours (DECIMAL(8,2))
- favorite_genre (VARCHAR(100))
- average_rating (DECIMAL(3,2))
- analytics_period (VARCHAR(20))
- period_start_date (DATE)
- period_end_date (DATE)
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
```

## Usage Examples

### Creating Tables
The database automatically creates all tables when initialized. Tables are created in the following order:
1. Analytics tables
2. Blog tables  
3. Fitness tables
4. Media tables

### Sample Data Population
Use the sample data script to populate the database with test data:
```bash
python scripts/populate_sample_data.py
```

### Query Examples

#### Get user's fitness programs
```sql
SELECT * FROM fitness_programs WHERE user_id = 1;
```

#### Get workout history for a user
```sql
SELECT w.*, p.program_name 
FROM fitness_workouts w 
JOIN fitness_programs p ON w.program_id = p.id 
WHERE w.user_id = 1 
ORDER BY w.workout_date DESC;
```

#### Get blog analytics for a post
```sql
SELECT * FROM blog_analytics WHERE blog_id = 'your-blog-id';
```

#### Get user activity for a session
```sql
SELECT * FROM user_activity WHERE session_id = 'your-session-id';
```

## Data Relationships

### Fitness Data Flow
1. **fitness_programs** → **fitness_program_exercises** → **fitness_exercises**
2. **fitness_workouts** → **fitness_exercise_logs** → **fitness_exercises**
3. **users** → **fitness_measurements** (body tracking)
4. **users** → **fitness_nutrition** (nutrition tracking)

### Blog Data Flow
1. **blog_posts** → **blog_analytics** (view tracking)
2. **blog_posts** → **blog_engagement** (user interactions)
3. **blog_categories** → **blog_posts** (categorization)

### Analytics Data Flow
1. **users** → **user_sessions** (login tracking)
2. **user_sessions** → **user_activity** (activity tracking)
3. **analytics_events** (general event tracking)

## Indexes and Performance

The database includes the following key indexes for performance:
- Primary keys on all tables
- Foreign key indexes for referential integrity
- Timestamp indexes for time-based queries
- User ID indexes for user-specific queries

## Maintenance

### Regular Maintenance Tasks
1. **Data Archiving**: Old analytics data should be archived periodically
2. **Index Maintenance**: Rebuild indexes on large tables
3. **Statistics Updates**: Update table statistics for query optimization
4. **Backup**: Regular database backups

### Data Retention
- User sessions: 90 days
- Analytics events: 1 year
- Fitness data: Indefinite (user data)
- Blog analytics: 2 years
- Media consumption: 1 year

## Security Considerations

1. **Data Encryption**: Sensitive user data should be encrypted at rest
2. **Access Control**: Implement proper database user permissions
3. **Audit Logging**: Track database access and modifications
4. **Data Privacy**: Ensure compliance with privacy regulations (GDPR, etc.)

## Troubleshooting

### Common Issues

1. **Connection Pool Exhaustion**: Increase pool size or implement connection pooling
2. **Slow Queries**: Add appropriate indexes or optimize query patterns
3. **Data Consistency**: Use transactions for multi-table operations
4. **Memory Usage**: Monitor and optimize JSONB field usage

### Monitoring

Key metrics to monitor:
- Database connection count
- Query execution time
- Table sizes and growth
- Index usage statistics
- Lock contention 