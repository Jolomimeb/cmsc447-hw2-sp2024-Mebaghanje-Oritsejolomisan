import sqlite3

conn = sqlite3.connect("database.db")

print("Successfully opened database")

conn.execute("CREATE TABLE students (name TEXT, Id TEXT, Points TEXT)")

print("Table created successfully")

conn.close()