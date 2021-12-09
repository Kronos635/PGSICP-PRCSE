#!/usr/bin/env python3
import os, logging, re, hashlib
from datetime import datetime, timezone, timedelta
import app_logging
from crud_resources import *
from createDB import *
from crud_users import *
from crud_roles import *
from crud_user_roles import *
from date_operations import *
from password_validation import *

# Main menu, the 1st menu the operator sees
def mainMenu():
    error=""
    while True:
        os.system("clear") # VM
        # Used to print messages to the user after executing an actions
        print(error)
        print("\nChoose an option: ")
        print("""
        1 : User accounts actions (leads to another menu with create/delete/modify/list)
        2 : Company resources actions (leads to another menu with create/delete/modify/list)
        3 : Roles actions (leads to another menu with create/delete/modify/list)
        4 : Assign roles to user
        0 : Exit"""
              )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            print(f'\nChoice: {choice}')
            userMenu()
        elif choice == '2' :
            print(f'\nChoice: {choice}')
            resourcesMenu()
        elif choice == '3' :
            print(f'\nChoice: {choice}')
            rolesMenu()
        elif choice == '4' :
            print(f'\nChoice: {choice}')
            # Ask resource to assign roles to.
            resource = input("\nName of the resource to assign roles: ")
            # check if resource exisos
            if find_resource(con, (resource,)) is not None:
                # lets loop until we received a existing username
                while True:
                    # List existing roles for given resource to help user to choose one
                    print(f"Roles for resource {resource}:")
                    for row in list_role_for_resource(con,(resource,)):
                        print(row[0] + ";" + row[1] + ";" + row[2])
                    # Ask for username
                    user = input("\nUsername of the resource to assign the role: ")
                    # If username exists
                    if find_user(con, (user,)) is not None:
                        # Ask for role to be assigned
                        role = input("\nInsert role to be assigned: ")
                        if find_role(con, (role,)) is not None:
                            # If role exists, lets assign it to the user
                            error = insert_user_role(con,(user,role))
                            if error == "OK":
                                # role assigned. Return Success afte mesage for user ans log.
                                error = "Role " + role + " assigned to user "+ user + " successfully"
                                logging.info(f'[INFO] - {error}.\n')
                                break
                            else:
                                # something went wrong
                                error = f'[ERROR] - User role {role} couldnt be  assigned to {user}.'
                                logging.error('{error}.\n')
                                break 
                        else:
                            # wrong role. Lets loop
                            error=f'\n[ERROR] - Role {role} does not exists!'
                            logging.error('{error}.\n')
                            continue
                    else:
                        # wrong username. Lets loop
                        error=f'\n[ERROR] - User {user} does not exists!'
                        logging.error('{error}.\n')
                        continue
            else:
                error=f'\n[ERROR] - Resource {resource} does not exists!'
        elif choice == '0':
            print(f'\nChoice: {choice}')
            con.close()
            exit()
        else:
            #os.system("clear")
            error=f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!' #VM
            #print(f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!')
            logging.error(f'ERROR - Choice: {choice} is NOT valid!')

# User menu, perform operations related to user accounts
def userMenu():
    error=""
    while True:
        os.system("clear")
        print(error)
        print("\nChoose an option: ")
        print("""
        1 : Create user account                   (DONE)
        2 : Update/Modify user account            (DONE)
        3 : Delete user account                   (DONE)
        4 : List information of a user account    (DONE)
        5 : List information of all user accounts (DONE)
        6 : Return to main menu
        0 : Exit"""
              )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            while True:
                username = input('\nType user account name (Email): ')
                # Convert username to lowercase
                username = username.lower()
                # Check if the username entered is a valid email
                # ^[a-z0-9-\._] -> check if the string start with [a-z] and/or [0-9] and/or [- . _] The slash \ serves as an escape character
                # Check the presence of @
                # Looks for char/word/number until the [.]
                # After the [.] looks for char/word/number, bigger than 2 chars
                # Example of valid email: nf_o.asd-asd@info1.info1
                if not re.search('^[a-z0-9-\._]+[a-z0-9]+[@]\w+[.]\w{2,}$', username):
                    print(f'\n[ERROR] - Not a valid email!')
                    continue
                else:
                    #print(f'\nValidity ok.')
                    break
            name = input('\nType user name: ')
            while True:
                bank_account_number = input('\nType bank account number: ')
                # Bank account number must have 21 numbers
                if not re.search('^[0-9]{21}$', bank_account_number):
                    print(f'\n[ERROR] - Bank account number must have 21 numbers!')
                    continue
                else:
                    #print(f'\nValidity ok.')
                    break
            while True:
                password_before_hash = input('\nType the password: ')
                validate_password_return = validarPassword(password_before_hash)
                if not validate_password_return == "OK":
                    print(f'\n{validate_password_return}')
                    continue
                else:
                    #print(f'\nValidity ok.')
                    password_before_hash = password_before_hash.encode('UTF-8')
                    break
            password_hash = hashlib.sha256(password_before_hash).hexdigest()
            # While the user doesn't input a valid number [1-30], the cycle continues
            while True:
                password_validity_days = input('\nType how many days should this password be valid for [1-30]: ')
                # Regex validates if the numbre of days is in the range [1-30]. 
                # ^([1-9] -> check if the beginning of the string is in the range [1-9]
                # | -> regex OR operator
                # |1[0-9] -> OR the string starts with 1 in combination with the range [0-9], checks for range [10-19]
                # |2[0-9] -> OR the string starts with 2 in combination with the range [0-9], checks for range [20-29]
                # |3[0] -> OR the string starts with 1 in combination with the range [0-9], checks for value [3]
                if not re.search("^([1-9]|1[0-9]|2[0-9]|3[0])$", password_validity_days):
                    print(f'\n[ERROR] - Password validity must be in the range [1-30]!')
                    continue
                else:
                    #print(f'\nValidity ok.')
                    break
            password_expire_date = converto_to_ms(password_validity_days)
            # Create user tuple to send to the DB
            user = (username,name,bank_account_number,password_hash,password_validity_days,password_expire_date)
            # Creating user in DB
            insert_user_return = insert_user(con, user)
            # If user creation went ok, return info to user
            if insert_user_return == "OK":
                error = f'\n[INFO] - User: {username} creation success!'
            # If user creation didn't go ok, return error to user
            else:
                error=f'\n[ERROR] - Couldnt create user: {username}\n{insert_user_return}'
        elif choice == '2' :
            while True:
                # Modify user, gets input from user
                username = input('\nType the username to modify: ')
                # Get current values from the role in the DB
                result = find_user(con,(username,))
                if result is not None:
                    break
                else:
                    print(f'\n[ERROR] - User "{username}" not found!')
                    continue
            name_current = result[1]
            bank_account_number_current = result[2]
            password_validity_current = result[3]
            # Get new name for the role, or keep the same by hitting enter
            # In case the user doesn't write anything, we save this variable to use later
            name = input(f'\nNew name (To keep the current value "{name_current}", just hit "Enter" button): ')
            if not name.isspace() and not name.strip():
                #print("Nothing written for userName")
                name = name_current
            # Get bank account number, or keep the same by hitting enter
            while True:
                bank_account_number = input(f'\nNew bank account number (To keep the current value "{bank_account_number_current}", just hit "Enter" button): ')
                # Exit while cycle, keeping the bank account number already in the DB
                if not bank_account_number.isspace() and not bank_account_number.strip():
                    bank_account_number = bank_account_number_current
                    break
                # Bank account number must have 21 numbers
                elif not re.search('^[0-9]{21}$', bank_account_number):
                    print(f'\n[ERROR] - Bank account number must have 21 numbers!')
                    continue
                else:
                    #print(f'\nValidity ok.')
                    break
            while True:
                # New password validity time, or keep the same by hitting enter
                password_validity = input(f'\nNew password validity time (To keep the current value "{password_validity_current}", just hit "Enter" button): ')
                # Regex validates if the numbre of days is in the range [1-30]. 
                # ^([1-9] -> check if the beginning of the string is in the range [1-9]
                # | -> regex OR operator
                # |1[0-9] -> OR the string starts with 1 in combination with the range [0-9], checks for range [10-19]
                # |2[0-9] -> OR the string starts with 2 in combination with the range [0-9], checks for range [20-29]
                # |3[0] -> OR the string starts with 1 in combination with the range [0-9], checks for value [3]
                if not re.search("^([1-9]|1[0-9]|2[0-9]|3[0])$", password_validity):
                    print(f'\n[ERROR] - Password validity must be in the range [1-30]!')
                    continue
                else:
                    #print(f'\nValidity ok.')
                    break
            if not password_validity.isspace() and not password_validity.strip():
                password_validity = password_validity_current
            # Create tuple to feed the update function
            update_values = (name,bank_account_number,password_validity,username)
            error = update_user(con,update_values)
            if error == "OK":
                error = f'[INFO] - User: "{username}" updated successfully.'
                logging.info(f'[INFO] - Role: {username}, updated successfully.\n')
            else:
                error = f'[ERROR] - User: "{username}" couldnt be updated.'
                logging.error(f'[ERROR] - User: {username} couldnt be updated.\n')
        elif choice == '3' :
            # Delete a role, gets input from user. Before deleting checks if it exists in DB
            username = input("\nUsername to delete: ")
            varQuestionDelete = input(f"\nAre you sure you want to delete role: {username}? (Y/N)")
            if varQuestionDelete in ('y', 'yes', 'Y', 'YES'):
                varFind_username = find_user(con,(username,))
                # If username exists, proceed to delete
                if varFind_username[0] == username:
                    delete_user_return = delete_user(con,(username,))
                    # Delete operation requires a commit, so that when the connection is closed to the DB, the user is actually deleted
                    con.commit()
                    # If user delete went ok, return info to user
                    if delete_user_return == "OK":
                        error = f'\n[INFO] - User: "{username}" deleted.'
                        logging.info(f'[INFO] INFO - role: "{username}"", deleted\n')
                    # If user creation didn't go ok, return error to user
                    else:
                        error = f'\n[ERROR] - Couldnt delete user: "{username}"\n"{insert_user_return}"'
                        logging.info(f'\n[ERROR] - Couldnt delete user: "{username}"\n"{insert_user_return}"\n')
                else:
                    print(f'{username}, is not a role!')
            else:
                print(f'Role: {username}, not deleted')
        elif choice == '4' :
            username = input('\nType user account name: ')
            # Get current values from the role in the DB
            results = find_user(con,(username,))
            print(f'\n[Username]: {results[0]}; [Name]: {results[1]}; [Bank Account Number]: {results[2]}; [Password valid for]: {results[3]} days; [Password expiration date]: {results[4]}')
            input("\nPress <enter> to continue")
            userMenu()
        elif choice == '5' :
            print(f'\nChoice: {choice}')
            # Print all roles
            print(f'\n### List of all user accounts ###')
            results = list_user(con,"ALL")
            # For each line in the returned results, show each value
            for row in results:
                print(f'\nUsername: {row[0]}; Name: {row[1]}; Bank Account Number: {row[2]}; Password valid for: {row[3]} days; Password expiration date: {row[4]}')
            input("\nPress <enter> to continue")
            userMenu()
        elif choice == '6' :
            mainMenu()
        elif choice == '0':
            print(f'\nChoice: {choice}')
            con.close()
            exit()
        else:
            error=f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!'
            logging.error(f'[ERROR] - Choice: {choice} is NOT valid!')

# Resources menu, perform operations related to resources
def resourcesMenu():
    error=""
    while True:
        os.system("clear")
        # Used to print messages to the user after executing an actions
        print(error)
        print("\nChoose an option: ")
        print("""
        1 : Create company resource                             (DONE)
        2 : Update/Modify company resource
        3 : Delete company resource                             (DONE)
        4 : List which users have access to a specific resource
        5 : List resources that contain "input" in the name     (DONE)
        6 : List all resources                                  (DONE)
        7 : Return to main menu
        0 : Exit"""
              )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            # Create new resource, gets input from user
            resource = input("\nName of the resource to create:")
            error = insert_resource(con,(resource,))
            if error == "OK":
                error = "Resource " + resource + " created successfully"
        elif choice == '2' :
            print(f'\nChoice: {choice}')
        elif choice == '3' :
            # Delete a resource, gets input from user. Before deleting checks if it exists in DB
            resource = input("\nName of the resource to delete: ")
            varQuestionDelete = input(f"\nAre you sure you want to delete resource: {resource}? (Y/N)")
            if varQuestionDelete in ('y', 'yes', 'Y', 'YES'):
                varFind_resource = find_resource(con,(resource,))
                if varFind_resource[0] == resource:
                    delete_resource(con,(resource,))
                    # Delete operation requires a commit, so that when the connection is closed to the DB the resource is actually deleted
                    con.commit()
                    print(f'Resource: {resource}, deleted')
                    logging.info(f'[INFO] - Resource: {resource}, deleted.\n')
                else:
                    print(f'{resource}, is not a resource!')
            else:
                print(f'Resource: {resource}, not deleted')
        elif choice == '4' :
            print(f'\nChoice: {choice}')
        elif choice == '5' :
            # Print resources that contain "{resource}"
            resource = input("\nList of resources that contain:")
            print(f'\n### List of resources that contain "{resource}" in the name###')
            resource = "%"+resource+"%"
            results = list_resource(con,(resource,))
            for row in results:
                print(row[0])
            input("Press <enter> to continue")
        elif choice == '6' :
            # Print all resources
            print(f'\n### List of all resources ###')
            results = list_resource(con,"ALL")
            for row in results:
                print(row[0])
            input("Press <enter> to continue")
        elif choice == '7' :
            # Return to main menu
            print(f'\nChoice: {choice}')
            mainMenu()
        elif choice == '0':
            # Exit the script
            print(f'\nChoice: {choice}')
            con.close()
            exit()
        else:
            error=f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!'
            #print(f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!')
            logging.error(f'ERROR - Choice: {choice} is NOT valid!')

# Roles menu, perform operations related to roles
def rolesMenu():
    error=""
    while True:
        os.system("clear")
        # Used to print messages to the user after executing an actions
        print(f"{error}")
        print("\nChoose an option: ")
        print("""
        1 : Create a role                           (DONE)
        2 : Update/Modify a role                    (DONE)
        3 : Delete role                             (DONE)
        4 : List which users have a specific role
        5 : List all roles                          (DONE)
        6 : Return to main menu
        0 : Exit"""
              )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            # Create new role, gets input from user
            role_name = input(f'\nName of the role to create (Ex.: roleName_resourceName_permission): ')
            role_resource = input(f'\nName of the resource this role, "{role_name}", will grant access: ')
            role_permission = input(f'\nPermissions of the role, "{role_name}"", on the resource, "{role_resource}" (Values:"R" or "RW"): ')
            # Check if the permission entered is valid
            if role_permission in ('r', 'R', 'rw', 'RW'):
                role = (role_name,role_resource,role_permission)
                error = insert_role(con,role)
            else:
                error = f'Role permission "{role_permission}" is not valid!'
            if error == "OK":
                error = f'Role "{role_name}" created successfully.'
                logging.info(f'[INFO] - Role: {role_name}, created successfully.\n')
        elif choice == '2' :
            # Change role, gets input from user
            role_name_current = input('\nName of the role to modify: ')
            # Get current values from the role in the DB
            result = find_role(con,(role_name_current,))
            role_resource_current = result[1]
            role_permission_current = result[2]
            # Get new name for the role, or keep the same by hitting enter
            # In case the user doesn't write anything, we save this variable to use later
            role_name = input(f'\nNew name of the role (To keep the current name "{role_name_current}", just hit "Enter" button): ')
            if not role_name.isspace() and not role_name.strip():
                #print("Nothing written for roleName")
                role_name = role_name_current
            # Get new resource for the role, or keep the same by hitting enter
            role_resource = input(f'\nName of the resource this role, will grant access (To keep the current resource "{role_resource_current}", just hit "Enter" button): ')
            if not role_resource.isspace() and not role_resource.strip():
                role_resource = role_resource_current
            # Get new permission for the role, or keep the same by hitting enter
            role_permission = input(f'\nPermissions of the role, "{role_name}", on the resource, "{role_resource_current}" (Values:"R", "W" or "RW"): ')
            if not role_permission.isspace() and not role_permission.strip():
                role_permission = role_permission_current
            # Check if the permission entered is valid
            if role_permission in ('r', 'R', 'w', 'W', 'rw', 'RW'):
                role = (role_name,role_resource,role_permission,role_name_current)
                error = update_role(con,role)
            else:
                error = f'Role permission "{role_permission}" is not valid!'
            if error == "OK":
                error = f'Role "{role_name}" updated successfully.'
                logging.info(f'[INFO]- Role: {role_name_current}, updated successfully. {role_name} {role_resource} {role_permission}\n')
        elif choice == '3' :
            # Delete a role, gets input from user. Before deleting checks if it exists in DB
            role = input("\nName of the role to delete: ")
            varQuestionDelete = input(f"\nAre you sure you want to delete role: {role}? (Y/N)")
            if varQuestionDelete in ('y', 'yes', 'Y', 'YES'):
                varFind_role = find_role(con,(role,))
                if varFind_role[0] == role:
                    delete_role(con,(role,))
                    # Delete operation requires a commit, so that when the connection is closed to the DB the role is actually deleted
                    con.commit()
                    error = f'Role: "{role}", deleted'
                    logging.info(f'[INFO] - role: {role}, deleted.\n')
                else:
                    print(f'{role}, is not a role!')
            else:
                print(f'Role: {role}, not deleted')
        elif choice == '4' :
            print(f'\nChoice: {choice}')
        elif choice == '5' :
            # Print all roles
            print(f'\n### List of all roles ###')
            results = list_role(con,"ALL")
            for row in results:
                print(row[0])
            input("\nPress <enter> to continue")
            rolesMenu()
        elif choice == '6' :
            mainMenu()
        elif choice == '0':
            print(f'\nChoice: {choice}')
            con.close()
            exit()
        else:
            error=f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!'
            #print(f'\n[ERROR] - Please insert a valid option. Choice: {choice} is NOT valid!')
            logging.error(f'ERROR - Choice: {choice} is NOT valid!')

### Script execution ###

# Connect to database
if not os.path.isfile("example.db"):
    try:
        con = sqlite3.connect('example.db')
    except:
        print("Not possible to connect to database")
        logging.error('[ERROR] - Not possible to connect to database\n')
    createTables(con)
else:
    try:
        con = sqlite3.connect('example.db')
    except:
        print("Not possible to connect to database")
        logging.error('[ERROR] - Not possible to connect to database\n')

# Calling main menu function
logging.info('[INFO] - Starting script\n')

mainMenu()

