import sqlite3


class DBContext(object):
    """
    Context manager for sqlite3. Commits everything on exit.
    """
    def __init__(self, path, connection=None, cursor=None):
        self.path = path
        self.conn = connection
        self.cursor = cursor

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()
