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
# https://www.sqlitetutorial.net/sqlite-python

# SQL operations usually need to use values from Python variables. However, beware of using Python’s 
# string operations to assemble queries, as they are vulnerable to SQL injection attacks
# Never do this -- insecure!
#       symbol = 'RHAT'
#       cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
#  Instead, use the DB-API’s parameter substitution

import sqlite3
import app_logging


# Insert roles
#
# PARAMETERS:
#   con         connection object
#   role    tuple with values to insert
# ----------------------------------
def insert_role(con,role):
    try:
        with con:
            con.execute("insert into roles values (?,?,?)", (role))
            return("OK")
    except sqlite3.IntegrityError:
        return("role already exists")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])

# List roles Function
#
# PARAMETERS:
#   con         connection object
#   role    string "ALL" or tuple with values to list
#
#   If role = ALL then Select all table
#   Tuple can have wildcards
#
#  RETURN:
#   List of tuples with all table columns
# ----------------------------------
def list_role(con,role):
    if role=="ALL":
        #for row in con.execute('SELECT * FROM roles ORDER BY rs_name'):
        #    print(row)
        return con.execute('SELECT * FROM roles ORDER BY r_name').fetchall()
    else:
        return con.execute('SELECT * FROM roles WHERE r_name like (?) ORDER BY r_name', (role)).fetchall()

# Find roles Function
#
# PARAMETERS:
#   con         connection object
#   role        tuple with role to retrieve
#
#  RETURN:
#   tuple with all table columns
# ----------------------------------
def find_role(con,role):
    return con.execute('SELECT * FROM roles WHERE r_name = (?)', (role)).fetchone()
    
# Update roles Function
#
# PARAMETERS:
#   con             connection object
#   update_values   tuple with the new values, the last element is the name of the role to be updated
#
# ----------------------------------
def update_role(con,update_values):
    try:
        with con:
            con.execute('UPDATE roles SET r_name = (?), r_resource = (?), r_permissions = (?)  WHERE r_name = (?)', (update_values))
            return("OK")
    except sqlite3.IntegrityError:
        return("Update failed. role name should be unique.")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])

# Delete roles Function
#
# PARAMETERS:
#   con         connection object
#   role    tuple with role to delete
# ----------------------------------
def delete_role(con,role):
    try:
        with con:
            con.execute('DELETE FROM roles WHERE r_name = (?)', (role))
            return("OK")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])
