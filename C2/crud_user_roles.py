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

# Insert user_roles
#
# PARAMETERS:
#   con         connection object
#   user_role    tuple with values to insert
# ----------------------------------
def insert_user_role(con,user_role):
    try:
        with con:
            con.execute("insert into user_roles values (?,?)", (user_role))
            return("OK")
    except sqlite3.IntegrityError:
        return("Role already exists for this username.")

# List role_users Function
#
# PARAMETERS:
#   con         connection object
#   user_role   string "ALL" or tuple with values to list
#
#   If role = ALL then Select all table
#   Tuple can have wildcards
#
#  RETURN:
#   List of tuples with users with a given role
# ----------------------------------
def list_role_users(con,role):
    if role=="ALL":
        return con.execute('SELECT u_username, u_name, ur_role, ur_resource, r_permissions FROM user_roles \
                            JOIN users on ur_username = u_username \
                            JOIN roles on ur_role = r_name \
                            ORDER BY ur_role').fetchall()
    else:
        return con.execute('SELECT u_username, u_name, ur_role, r_resource, r_permissions FROM user_roles \
                            JOIN users on ur_username = u_username \
                            JOIN roles on ur_role = r_name \
                            WHERE ur_role like (?) ORDER BY ur_role', (role)).fetchall()

# List user_roles Function
#
# PARAMETERS:
#   con         connection object
#   user_role   string "ALL" or tuple with values to list
#
#   If user_role = ALL then Select all table
#   Tuple can have wildcards
#
#  RETURN:
#   List of tuples with roles available to the given user
# ----------------------------------
def list_user_roles(con,user):
    if user=="ALL":
        return con.execute('SELECT ur_role, u_username, u_name, r_resource, r_permissions FROM user_roles \
                            JOIN users on ur_username = u_username \
                            JOIN roles on ur_role = r_name \
                            ORDER BY ur_username').fetchall()
    else:
        return con.execute('SELECT ur_role, u_username, u_name, r_resource, r_permissions FROM user_roles \
                            JOIN users on ur_username = u_username \
                            JOIN roles on ur_role = r_name \
                            WHERE ur_username like (?) ORDER BY ur_username', (user)).fetchall()

# Find user_roles Function
#
# PARAMETERS:
#   con         connection object
#   user_role   tuple with username and role to retrieve
#
#  RETURN:
#   tuple with all table columns
# ----------------------------------
def find_user_role(con,user_role):
    return con.execute('SELECT * FROM user_roles WHERE ur_username = (?) and ur_role = (?)', (user_role)).fetchone()
    
# Update user_roles Function
#
# PARAMETERS:
#   con             connection object
#   update_values   tuple with the new values, the first pair refers to the new values and the second pair identifies the user_role to be updated
#
# ----------------------------------
def update_user_role(con,update_values):
    try:
        with con:
            con.execute('UPDATE user_roles SET ur_username = (?), ur_role = (?)  WHERE ur_username = (?) and ur_role = (?)', (update_values))
            return("OK")
    except sqlite3.IntegrityError:
        return("Update failed. Role already exists for this username.")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])

# Delete user_roles Function
#
# PARAMETERS:
#   con         connection object
#   user_role    tuple with user and role to delete
# ----------------------------------
def delete_user_role(con,user_role):
    try:
        with con:
            con.execute('DELETE FROM user_roles WHERE ur_username = (?) and ur_role= (?) ', (user_role))
            return("OK")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])

# List resources accessed by a specific user Function
#
# PARAMETERS:
#   con         connection object
#   resource    tuple with resource to list users for
#
#
#  RETURN:
#   List of tuples with users with a given role
# ----------------------------------
def list_resources_accessed_by_user(con,resource):
    return con.execute('SELECT u_username, u_name, ur_role, r_resource, r_permissions FROM user_roles \
                            JOIN users on ur_username = u_username \
                            JOIN roles on ur_role = r_name \
                            WHERE r_resource like (?) ORDER BY r_resource', (resource)).fetchall()

# List resources accessed by a specific user Function
#
# PARAMETERS:
#   con         connection object
#   resource    tuple with resource to list users for
#
#
#  RETURN:
#   List of tuples with users with a given role
# ----------------------------------
def list_resources_accessed_by_username(con,username):
    return con.execute('SELECT u_username, u_name, ur_role, r_resource, r_permissions FROM user_roles \
                            JOIN users on ur_username = u_username \
                            JOIN roles on ur_role = r_name \
                            WHERE ur_username like (?) ORDER BY r_resource', (username)).fetchall()
