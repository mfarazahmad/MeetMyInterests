
BASE_READ = """ SELECT * FROM {table} WHERE {condition} {sort}; """
BASE_WRITE = """ INSERT INTO {table} ({columns}) VALUES ({values}); """
BASE_UPDATE = """ UPDATE {table} SET {data} WHERE {condition}; """
BASE_DELETE = """ DELETE FROM {table} WHERE {condition}; """
