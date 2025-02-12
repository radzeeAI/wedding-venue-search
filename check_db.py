import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('venues.db')
cursor = conn.cursor()

# Query all data from the venues table
cursor.execute("SELECT * FROM venues")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(row)
else:
    print("No data found in 'venues' table.")

# Close the connection
conn.close()
