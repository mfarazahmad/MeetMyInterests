import psycopg2
from psycopg2 import pool, extras
from config.logger import log
from database.queries.base import *
from database.tables import *

class Database():

    def __init__(self,  host: str, user: str, password: str, name: str, port: int):
        log.info(f"Connecting To Database @ Host: {host}:{port}")
        self.pool  = pool.SimpleConnectionPool(
                            1, 10,
                            database = name, 
                            user = user, 
                            host= host,
                            password = password,
                            port = port
                        )
        self.instance = self.pool.getconn()
        
        schemaPresent = self.validateTables()
        if schemaPresent:
            log.info("Database connected and schemas validated")
        else: 
            log.error("Database connected and schemas do not exist. Creating now...")
            self.createTables()

    def tearDown(self):
        self.pool.putconn(self.instance)
        self.pool.closeall()
        log.info("Database connection closed")
    
    def createTables(self):
        """Create all tables defined in the table modules"""
        log.info("Creating database tables...")
        
        # Analytics tables
        self.executeQuery(CREATE_USER_TABLE, "create")
        self.executeQuery(CREATE_USER_SESSIONS_TABLE, "create")
        self.executeQuery(CREATE_USER_ACTIVITY_TABLE, "create")
        self.executeQuery(CREATE_ANALYTICS_EVENTS_TABLE, "create")
        
        # Blog tables
        self.executeQuery(CREATE_BLOG_POSTS_TABLE, "create")
        self.executeQuery(CREATE_BLOG_ANALYTICS_TABLE, "create")
        self.executeQuery(CREATE_BLOG_ENGAGEMENT_TABLE, "create")
        self.executeQuery(CREATE_BLOG_CATEGORIES_TABLE, "create")
        
        # Fitness tables
        self.executeQuery(CREATE_FITNESS_PROGRAMS_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_EXERCISES_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_PROGRAM_EXERCISES_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_WORKOUTS_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_EXERCISE_LOGS_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_MEASUREMENTS_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_EQUIPMENT_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_BANDS_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_GOALS_TABLE, "create")
        self.executeQuery(CREATE_FITNESS_NUTRITION_TABLE, "create")
        
        # Media tables
        self.executeQuery(CREATE_MEDIA_MOVIES_TABLE, "create")
        self.executeQuery(CREATE_MEDIA_GAMES_TABLE, "create")
        self.executeQuery(CREATE_MEDIA_CONSUMPTION_TABLE, "create")
        self.executeQuery(CREATE_MEDIA_PLATFORMS_TABLE, "create")
        self.executeQuery(CREATE_MEDIA_ANALYTICS_TABLE, "create")
        
        log.info("All tables created successfully")

    def validateTables(self):
        for _, tables in TABLES_MANIFEST.items():
            tablenames = ', '.join([f"'{table}'" for table in tables])
            
            query = CHECK_TABLE_EXISTS.format(tablenames=tablenames)
            results = self.executeQuery(query, "validate")
            if results["data"] and results["data"][0]["exists"]:
                continue
            else:
                return False
        return True
    
    def customQuery(self, query):
        self.executeQuery(query, "custom")

    def executeQuery(self, query, queryType):
        log.info(f'Triggering Query: {query}')
        cursor = self.instance.cursor(cursor_factory=extras.DictCursor)

        result = {"data": None}
        try:
            cursor.execute(query)
            if queryType == "select" or queryType == "validate":
                result["data"] = cursor.fetchall()
            else:
                self.instance.commit() 
                result["data"] = cursor.rowcount
        except Exception as e:
            log.debug(f"Database Error: {e}")

            if queryType != "select":
                self.instance.rollback()
                log.debug(f"Rolling Back Transaction...")

        finally:
            cursor.close()

        return result

    def read(self, columns: list, table: str, condition: str = "", sort: str = ""):
        columns_str = '*' if columns == ['*'] else ', '.join(columns)
        condition_str = f"WHERE {condition}" if condition else ""
        sort_str = f"ORDER BY {sort}" if sort else ""
        
        query = BASE_READ.format(columns=columns_str, table=table, condition=condition_str, sort=sort_str)
        return self.executeQuery(query, "select")

    def write(self, columnToValueMap: dict, table: str, condition:str =""):
        columns = ', '.join(columnToValueMap.keys())
        values = ', '.join([f"'{value}'" for value in columnToValueMap.values()])

        query = BASE_WRITE.format(table=table, columns=columns, values=values)
        return self.executeQuery(query, "insert")

    def update(self, columnToValueMap: dict, table: str, condition:str =""):
        data = ', '.join([f"{column} = '{value}'" if isinstance(value, str) else f"{column} = {value}" for column, value in columnToValueMap.items()])
        query = BASE_UPDATE.format(table=table, data=data, condition=condition)
        return self.executeQuery(query, "update")

    def delete(self, column: str, table: str, condition:str =""):
        query = BASE_DELETE.format(table=table, condition=condition)
        return self.executeQuery(query, "delete")