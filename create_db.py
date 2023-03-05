import sqlite3

conn = sqlite3.connect('identifier.sqlite [2]')
c = conn.cursor()

try:
    c.execute('''CREATE TABLE users2 (id INTEGER PRIMARY KEY, Name TEXT,
              Last_Name TEXT,
              Street TEXT,
              Building_Number TEXT,
              Area TEXT,
              Time DATETIME)''')
except sqlite3.OperationalError:
    pass
