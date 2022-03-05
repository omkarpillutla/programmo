import csv
from write_contacts import main

with open('contacts.csv', 'r') as file:
    contacts_reader = csv.reader(file, delimiter="-")

    # Reading names
    search_name = input("Enter the name you want to find: ")
    
    for row in contacts_reader:
        if search_name.lower().strip() == row[0].lower().strip():
            while True:
                search_what = input("What do you want to search (Number or Address)? ")
                if search_what in ['number', 'Number', 'no', 'No']:
                    print("The phone number is: ", row[1])

                elif search_what in ['address', 'Address']:
                    print("The address is: ", row[2])
                exit()

print("The name entered does not exist.")
add_choice = input("Would you like to add it?")
if add_choice in ['yes', 'YES', 'Yes', 'y', 'Y']:
    main()

elif add_choice in ['no', 'NO', 'No', 'n', 'N']:
    exit()

