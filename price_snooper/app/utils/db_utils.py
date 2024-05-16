import os
import sqlite3
import sys

app_name = 'price-snooper'
schema_file = 'sql/init_schema.sql'


class DatabaseUtil:
    def __init__(self, db_name):
        self.db_name = db_name
        self.schema_file = schema_file
        self.conn = self._get_database_conn()  # Call the method to get the database connection
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def get_data_directory(self):
        """Return the path to the Application Data Directory."""
        if sys.platform == 'darwin':
            # macOS
            return os.path.expanduser("~/Library/Application Support/" + app_name + "/")
        elif sys.platform.startswith('linux'):
            # Linux
            return os.path.expanduser("~/.local/share/" + app_name + '/')
        else:
            raise RuntimeError("Unsupported platform: " + sys.platform)

    def _get_database_conn(self):
        """Create an SQLite database file in the Application Data Directory."""
        data_directory = self.get_data_directory()
        # Create the directory if it doesn't exist
        os.makedirs(data_directory, exist_ok=True)

        # Connect to the SQLite database (or create it if it doesn't exist)
        db_file = os.path.join(data_directory, self.db_name)
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            raise RuntimeError(f"Error connecting to database: {e}")

    def _initialize_schema(self):
        """Initialize the database schema."""
        try:
            with open(self.schema_file, 'r') as f:
                schema_queries = f.read()
                self.cursor.executescript(schema_queries)
                self.conn.commit()
            print("Database schema initialized successfully!")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error initializing schema: {e}")

    def close(self):
        """Close the database connection."""
        try:
            if self.conn:
                self.cursor.close()
                self.conn.close()
                print("Database connection closed.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error closing database connection: {e}")

    def execute(self, query, params=None):
        """Execute a query that doesn't return data."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            raise RuntimeError(f"Error executing query: {e}")

    def fetch(self, query, params=None):
        """Fetch data from a query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise RuntimeError(f"Error fetching data: {e}")
