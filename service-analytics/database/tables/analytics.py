CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        column1 VARCHAR(50),
        column2 INT
    );
"""