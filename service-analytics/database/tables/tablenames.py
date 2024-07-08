CHECK_TABLE_EXISTS = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.tables 
    WHERE table_name IN ({tablenames})
);
"""

TABLES_MANIFEST = {
    "analytics": [
        "users", 
    ],
    "blog": [
        "users", 
    ],
    "fitness": [
        "workouts", 
        "programs",
    ],
    "media": [
        "movies"
    ],
}