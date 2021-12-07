#!/usr/bin/env python3
# coding: utf-8
#
# 20211205 - PGSICP-PRCSE - Grupo2
#
# pip install -r Requirements.txt
#
# About Python and SQLLite
# https://docs.python.org/3/library/sqlite3.html#
# https://www.sqlite.org/index.html

# SQL operations usually need to use values from Python variables. However, beware of using Python’s 
# string operations to assemble queries, as they are vulnerable to SQL injection attacks
# Never do this -- insecure!
#       symbol = 'RHAT'
#       cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
#  Instead, use the DB-API’s parameter substitution

import sqlite3


# Insert resources
#
# PARAMETERS:
#   con         connection object
#   resource    tuple with values to insert
# ----------------------------------
def insert_resource(con,resource):
    try:
        with con:
            con.execute("insert into resources values (?)", (resource))
    except sqlite3.IntegrityError:
        print("Resource already exists")

# List resources Function
#
# PARAMETERS:
#   con         connection object
#   resource    string "ALL" or tuple with values to list
#
#   If resource = ALL then Select all table
#   Tuple can have wildcards
#
#  RETURN:
#   List of tuples with all table columns
# ----------------------------------
def list_resource(con,resource):
    if resource=="ALL":
        #for row in con.execute('SELECT * FROM resources ORDER BY rs_name'):
        #    print(row)
        return con.execute('SELECT * FROM resources ORDER BY rs_name').fetchall()
    else:
        return con.execute('SELECT * FROM resources WHERE rs_name like (?) ORDER BY rs_name', (resource)).fetchall()

# Find resources Function
#
# PARAMETERS:
#   con         connection object
#   resource    tuple with resource to retrieve
#
#  RETURN:
#   tuple with all table columns
# ----------------------------------
def find_resource(con,resource):
    return con.execute('SELECT * FROM resources WHERE rs_name = (?)', (resource)).fetchone()
    
# Update resources Function
#
# PARAMETERS:
#   con             connection object
#   update_values   tuple which 1st element is the new value, the second element is the resource to update
#
# ----------------------------------
def update_resource(con,update_values):
    try:
        with con:
            con.execute('UPDATE resources SET rs_name = (?) WHERE rs_name = (?)', (update_values))
    except:
        print("Update failed. Resource name should be unique.")

# Delete resources Function
#
# PARAMETERS:
#   con         connection object
#   resource    tuple with resource to delete
# ----------------------------------
def delete_resource(con,resource):
    con.execute('DELETE FROM resources WHERE rs_name = (?)', (resource))
