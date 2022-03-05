# Phone Book

"""
    Take name and phone number from user ad store it in a phone book
"""
import csv
from os import linesep

def main():
    # Declare data structure
    contacts = []

    # Initialize infinite loop
    while True:
        # Create contact?
        while True:
            create = input("Create contact? ")
            stop = True

            # Validate create contact input
            if create not in ['yes', 'YES', 'Yes', 'y', 'Y', 'no', 'NO', 'No', 'n', 'N']:
                stop = False

            if stop:
                break

        if create in ['yes', 'YES', 'Yes', 'y', 'Y']:
        
            # Get fullname from user
            while True:
                # Declare name dictionary
                name_dict = {}
                full_name = input("Enter full name: ")
                # Declare stop variable
                stop = True
                # Split fullname into separate names
                names = full_name.split(' ')

                # Validate name
                for name in names:
                    if not name.isalpha() or len(name) < 1:
                        stop = False
                        break
        
                if stop:
                    break

            # Add name to dictionary
            name_dict ["Name"] = full_name


            # Get contact number from user
            while True:
                num = input("Enter contact number: ")
                stop = True

                # Validate contact number
                if not num.isnumeric() or len(num) != 10:
                    stop = False

                if stop:
                    break

            # Add number to dictionary and list
            name_dict ["Phone Number"] = num


            while True:
                # Add address
                add_address = input("Add address?: ")
                if add_address in ['yes', 'YES', 'Yes', 'y', 'Y']:
                    address = input("Enter the address of the contact: ")
                    break

                elif add_address in ['no', 'NO', 'No', 'n', 'N']:
                    address = ""
                    break

            # Add address to dictionary
            name_dict ["Address"] = address

            # Add name_dict to contacts list
            contacts.append(name_dict)
        

        elif create in ['no', 'NO', 'No', 'n', 'N']:
            break

    # Sort contacts
    sorted_contacts = sorted(contacts, key=lambda k: k["Name"]) 
    print(sorted_contacts)


    # Opening contacts.csv file
    with open('contacts.csv', 'a') as file:
        contacts_writer = csv.DictWriter(file, lineterminator = '\n', fieldnames=['Name', 'Phone Number', 'Address'], delimiter = '-')
        contacts_writer.writerows(contacts)

# Calling main function
if __name__ == "__main__":
    main()
