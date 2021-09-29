import sqlite3

conn = sqlite3.connect('data.db')
print( "Opened database successfully")

conn.execute("CREATE TABLE USERS (ID INT, NAME TEXT, AUTO TEXT);")
print( "Table USERS created successfully")
conn.execute("CREATE TABLE URL (HTTP TEXT);")
print("Table URL created successfully")

conn.close()
print( "Closed database successfully")
