#!/usr/bin/env python3
# coding: utf-8
#
import sqlite3
import os
import hashlib
import logging
import app_logging
from createDB import *
from crud_resources import *
from crud_users import *
from crud_roles import *
from crud_user_roles import *

if not os.path.isfile("example.db"):
    try:
        con = sqlite3.connect('example.db')
    except:
        print("Not possible to connect to database")
    createTables(con)
else:
    try:
        con = sqlite3.connect('example.db')
    except:
        print("Not possible to connect to database")

#---------------------------------- Resources
print("\n\n---------------------------------- Resources Sanity Tests\n\n")
resource1=("resource1",)
print("Inserting new resource " + resource1[0] + ": [" + insert_resource(con,resource1) + "]")
resource2=("resource2",)
print("Inserting new resource " + resource2[0] + ": [" + insert_resource(con,resource2) + "]")
resource3=("resource3",)
print("Inserting new resource " + resource3[0] + ": [" + insert_resource(con,resource3) + "]")

print("\nList all resources:")
print(list_resource(con,"ALL"))

print("\nInserting duplicated resource " + resource1[0] + ": [" + insert_resource(con,resource1) + "]")

update_state=("resource4","resource3")
print("Updating " + update_state[1] + " to " + update_state[0] + ": [" + update_resource(con,update_state) + "]")
#print(update_resource(con,update_state))

print("\nList all resources:")
print(list_resource(con,("ALL")))

print("\nDeleting resource " + resource1[0] + ": [" + delete_resource(con,resource1) + "]")
#print(delete_resource(con,resource1))
print("\nList all resources:")
print(list_resource(con,("ALL")))

query = ("resource2",)
print("\nQuery for resource: " + query[0] + " explicitly")
result=find_resource(con,query)
print(result)

print("\nQuery for resource: resource2 using wildcard '%'")
print(list_resource(con,("resou%2",)))
# ---------------------------------

#---------------------------------- Users
# the password has to be encoded to a byte string before being hashed.
# a byte string is just a sequence of bytes. In this case we will use "UTF-8" for latin characters and special characters support
# ?|!"'*çÇàÀáÁãÃõÕéÉóÓõÕ<>€ºªêÊ^~£§,;.:-_#$%&/\()= is a valid password
print("\n\n---------------------------------- Users Sanity Tests\n\n")
user1_password=input("\nUser1 password:").encode('UTF-8')
user1=("user1@isep.ipp.pt","User1","435747437278474176347",hashlib.sha256(user1_password).hexdigest(),30,646474)

print("Inserting new user " + user1[0] + ": [" + insert_user(con, user1) + "]")

user2_password="password2".encode('UTF-8')
user2=("user2@isep.ipp.pt","User2","00747437278474176347",hashlib.sha256(user2_password).hexdigest(),30,646474)
print("Inserting new user " + user2[0] + ": [" + insert_user(con, user2) + "]")

user3_password="password3".encode('UTF-8')
user3=("user3@isep.ipp.pt","User3","35474857979808576456",hashlib.sha256(user3_password).hexdigest(),30,646474)
print("Inserting new user " + user3[0] + ": [" + insert_user(con, user3) + "]")

user4_password="password4".encode('UTF-8')
user4=("user4@isep.ipp.pt","User4","957347457576343456343",hashlib.sha256(user4_password).hexdigest(),30,646474)
print("Inserting new user " + user4[0] + ": [" + insert_user(con, user4) + "]")

print("\nList all users:")
list_all_users=list_user(con,"ALL")
print("list has " + str(len(list_all_users)) + " rows")
print(list_all_users)

update_data=("user5@isep.ipp.pt","Alterado","35474857979808576456",30,"user3@isep.ipp.pt")
print("\nUpdating " + update_data[4] + " to " + update_data[0] + ": [" + update_user(con, update_data) + "]")

query = ("%user3%",)
result=list_user(con,query)
print("\nQuery for user: user3 using wildcard '%'")
print(result)


# ---------------------------------

#---------------------------------- Roles
print("\n\n---------------------------------- Roles Sanity Tests\n\n")
role1=("role1","resource1","r")
print("Inserting new role " + role1[0] + ": [" + insert_role(con,role1) + "]")
role2=("role2","resource1","w")
print("Inserting new role " + role2[0] + ": [" + insert_role(con,role2) + "]")
role3=("role3","resource2","w")
print("Inserting new role " + role3[0] + ": [" + insert_role(con,role3) + "]")

print("\nList all roles:")
print(list_role(con,"ALL"))

print("\nInserting duplicated role " + role3[0] + ": [" + insert_role(con,role3) + "]")

update_state=("role4","resource2","w","role3")
print("\nUpdating role " + update_state[3] + " to " + update_state[0] + ": [" + update_role(con,update_state) + "]")

query = ("role4",)
print("\nQuery for role " + query[0] + " explicitly:")
print(find_role(con,query))

print("\nDeleting role2: [ " + delete_role(con,("role2",)) + "]")

print("\nList all roles:")
print(list_role(con,"ALL"))

print("\nQuery for role 'role1' using wildcard '%'")
print(list_role(con,("ro%1",)))

role5=("role5","resource2","r")
print("\nInserting new role " + role5[0] + ": [" + insert_role(con,role5) + "]")


# ---------------------------------

#---------------------------------- User Roles

print("\n\n---------------------------------- User Roles Sanity Tests\n\n")

user_role1=("user1@isep.ipp.pt","role1")
print("Assigning " + user_role1[1] + " to user " + user_role1[0] + ": [" + insert_user_role(con,user_role1) + "]")
user_role2=("user2@isep.ipp.pt","role4")
print("Assigning " + user_role2[1] + " to user " + user_role2[0] + ": [" + insert_user_role(con,user_role2) + "]")
user_role3=("user5@isep.ipp.pt","role1")
print("Assigning " + user_role3[1] + " to user " + user_role3[0] + ": [" + insert_user_role(con,user_role3) + "]")

print("\nList users by role:")
print(list_user_roles(con,"ALL"))


print("\nAssigning duplicated  " + user_role3[1] + " to " + user_role3[0] + ": [" + insert_user_role(con,user_role3) + "]")

user_role4=("user1@isep.ipp.pt","role5")
print("Assigning " + user_role4[1] + " to user " + user_role4[0] + ": [" + insert_user_role(con,user_role4) + "]")


update_state=("user1@isep.ipp.pt","role5","user1@isep.ipp.pt","role4")
print("Updating " + update_state[3] + " for user " + update_state[2] + " to " + update_state[1] + ": [" + update_user_role(con,update_state) + "]")

print("Revoking " + user_role2[1] + " for user: " + user_role2[0] + "[" + delete_user_role(con,user_role2) + "]")

print("\nList users by role:")
print(list_user_roles(con,"ALL"))

query = user_role1
result=find_user_role(con,query)
print("\nQuery if user  " + query[0] + " has " + query[1] + " role assigned")
print(result)

user_role5=("user1@isep.ipp.pt","role4")
print("\nAssigning " + user_role5[1] + " to user " + user_role5[0] + ": [" + insert_user_role(con,user_role5) + "]")

print("\nList users with role1 assigned:")
print(list_role_users(con,("role5",)))

print("\nList assigned roles for user 'user1@isep.ipp.pt':")
print(list_user_roles(con,("user1@isep.ipp.pt",)))

#print(list_user_roles(con,("%isep%",)))

con.close()
