CHECK_TABLE_EXISTS = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.tables 
    WHERE table_name IN ({tablenames})
);
"""

TABLES_MANIFEST = {
    "analytics": [
        "users", 
        "user_sessions",
        "user_activity",
        "analytics_events"
    ],
    "blog": [
        "blog_posts",
        "blog_analytics", 
        "blog_engagement",
        "blog_categories"
    ],
    "fitness": [
        "fitness_programs",
        "fitness_exercises",
        "fitness_program_exercises", 
        "fitness_workouts",
        "fitness_exercise_logs",
        "fitness_measurements",
        "fitness_equipment",
        "fitness_bands",
        "fitness_goals",
        "fitness_nutrition"
    ],
    "media": [
        "media_movies",
        "media_games",
        "media_consumption",
        "media_platforms",
        "media_analytics"
    ],
}