CREATE_FITNESS_PROGRAMS_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_programs (
        id SERIAL PRIMARY KEY,
        program_name VARCHAR(255) NOT NULL,
        program_type VARCHAR(50) NOT NULL,
        frequency INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        status VARCHAR(20) DEFAULT 'active'
    );
"""

CREATE_FITNESS_EXERCISES_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_exercises (
        id SERIAL PRIMARY KEY,
        exercise_name VARCHAR(255) NOT NULL,
        exercise_type VARCHAR(50) NOT NULL,
        body_part VARCHAR(100),
        movement_type VARCHAR(50),
        equipment_needed TEXT[],
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_PROGRAM_EXERCISES_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_program_exercises (
        id SERIAL PRIMARY KEY,
        program_id INTEGER REFERENCES fitness_programs(id),
        exercise_id INTEGER REFERENCES fitness_exercises(id),
        workout_day VARCHAR(10),
        recommended_sets INTEGER,
        recommended_reps INTEGER,
        recommended_volume VARCHAR(100),
        band_weight_multiplier DECIMAL(5,2),
        alternative_exercise_id INTEGER REFERENCES fitness_exercises(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_WORKOUTS_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_workouts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        program_id INTEGER REFERENCES fitness_programs(id),
        workout_date DATE NOT NULL,
        workout_notes TEXT,
        total_duration_minutes INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_EXERCISE_LOGS_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_exercise_logs (
        id SERIAL PRIMARY KEY,
        workout_id INTEGER REFERENCES fitness_workouts(id),
        exercise_id INTEGER REFERENCES fitness_exercises(id),
        sets INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        weight DECIMAL(8,2),
        duration_seconds INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_MEASUREMENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_measurements (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        measurement_date DATE NOT NULL,
        height DECIMAL(5,2),
        chest DECIMAL(5,2),
        bicep DECIMAL(5,2),
        tricep DECIMAL(5,2),
        thighs DECIMAL(5,2),
        calves DECIMAL(5,2),
        waist DECIMAL(5,2),
        neck DECIMAL(5,2),
        weight DECIMAL(6,2),
        body_fat_percentage DECIMAL(4,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_EQUIPMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_equipment (
        id SERIAL PRIMARY KEY,
        equipment_name VARCHAR(255) NOT NULL,
        equipment_type VARCHAR(100),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_BANDS_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_bands (
        id SERIAL PRIMARY KEY,
        band_name VARCHAR(100) NOT NULL,
        band_type VARCHAR(50),
        low_weight INTEGER,
        single_weight INTEGER,
        color VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_GOALS_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_goals (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        goal_type VARCHAR(50) NOT NULL,
        goal_target JSONB,
        goal_deadline DATE,
        goal_status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_FITNESS_NUTRITION_TABLE = """
    CREATE TABLE IF NOT EXISTS fitness_nutrition (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        nutrition_date DATE NOT NULL,
        calories INTEGER,
        protein_grams DECIMAL(6,2),
        carbs_grams DECIMAL(6,2),
        fat_grams DECIMAL(6,2),
        water_ounces DECIMAL(6,2),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
