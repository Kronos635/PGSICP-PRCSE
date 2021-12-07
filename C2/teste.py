#!/usr/bin/env python3
# coding: utf-8
#
import sqlite3
from crud_resources import *
from createDB import *
from crud_users import *

try:
    con = sqlite3.connect('example.db')
except:
    print("Not possible to connect to database")

createTables(con)

#---------------------------------- Resources
resource1=("resource1",)
insert_resource(con,resource1)
resource2=("resource2",)
insert_resource(con,resource2)
resource3=("resource3",)
insert_resource(con,resource3)

print(list_resource(con,"ALL"))

insert_resource(con,resource3)

update_state=("resource4","resource3")

update_resource(con,update_state)

delete_resource(con,resource1)

query = ("resource2",)
result=find_resource(con,query)
print(result)

print(list_resource(con,("resou%2",)))
# ---------------------------------

#---------------------------------- Users
user1=("user1@isep.ipp.pt","User1","435747437278474176347","password1",647646,646474)
insert_user(con, user1)

user2=("user2@isep.ipp.pt","User2","00747437278474176347","password1",647646,646474)
insert_user(con, user2)

user3=("user3@isep.ipp.pt","User3","35474857979808576456","password1",647646,646474)
insert_user(con, user3)

user4=("user4@isep.ipp.pt","User4","957347457576343456343","password1",647646,646474)
insert_user(con, user4)

update_state=("resource4","resource3")
update_resource(con,update_state)

print(list_user(con,"ALL"))

con.close()
