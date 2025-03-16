import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Establish and return a database connection."""
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT
                )
            
            except psycopg2.Error as e:
                print(f"Database connection failed: {e}")
                self.conn = None
        return self.conn

    def close(self):
        """Closes the database connection."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None
