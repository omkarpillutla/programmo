import csv
import sqlite3
conect = sqlite3.connect("test.db")
cursor = conect.cursor()

file = open("movies.csv")
rows = csv.reader(file)
cursor.executemany("INSERT INTO test VALUES (?, ?)", rows)

cursor.execute("SELECT * FROM test")
print(cursor.fetchall())

conect.commit()
conect.close()