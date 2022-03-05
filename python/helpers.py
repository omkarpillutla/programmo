import csv
import sqlite3

def print_csv(file_name):
    with open(file_name, 'r') as file:
        file_reader = csv.DictReader(file, delimiter = ",")
        for row in file_reader:
            print(row)

file_name = input("Enter the file name: ")
print_csv(file_name)



entered_username = "Username"
entered_password = "Password"
list_database = db.execute(f"SELECT * FROM database WHERE Username = {entered_username} AND Password = {entered_password}")
if len(list_database) == 1:
    print("authenticated")
else:
    print("Wrong username")

print(list_database)


