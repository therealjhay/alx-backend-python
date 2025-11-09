import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open connection and execute query with parameters
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close connection
        if self.conn:
            self.conn.close()

# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)
with ExecuteQuery("example.db", query, params) as result:
    print(result)
