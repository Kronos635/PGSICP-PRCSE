#!/usr/bin/env python
# coding: utf-8
#

from crud_resources import *

try:
    con = sqlite3.connect('example.db')
except:
    print("Not possible to connect to database")

createTables(con)
resource1=("resource1",)
insert_resource(con,resource1)
resource2=("resource2",)
insert_resource(con,resource2)
resource3=("resource3",)
insert_resource(con,resource3)

list_resource(con,"ALL")

insert_resource(con,resource3)

update_state=("resource4","resource3")

update_resource(con,update_state)

delete_resource(con,resource1)

query = ("resource2",)
result=find_resource(con,query)
print(result)


#list_resource("ALL")

con.close()
