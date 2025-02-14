import sqlite3
import csv

# Define the SQLite3 database file
db_file = 'ratings.db'

# Create a connection to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create a table for storing wine information
cursor.execute('''
CREATE TABLE IF NOT EXISTS wines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    variety TEXT NOT NULL,
    rating FLOAT NOT NULL,
    notes TEXT
)
''')

# Commit the table creation
conn.commit()

# Open the CSV file and insert data into the database
csv_file = 'ratings.csv'  # Path to your CSV file

for i in range(2):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Extract data from the row
                name = row['name']
                region = row['region']
                variety = row['variety']
                rating = float(row['rating'])  # Convert rating to float
                notes = row['notes']

                # Insert the row into the database
                cursor.execute('''
                INSERT INTO wines (name, region, variety, rating, notes)
                VALUES (?, ?, ?, ?, ?)
                ''', (name, region, variety, rating, notes))

            except Exception as e:
                # If there's an error (e.g., missing data or conversion issues), ignore the row
                print(f"Skipping row due to error: {e}")
                continue

# Commit the changes and close the connection
conn.commit()
conn.close()

print("CSV data has been inserted into the database successfully!")

