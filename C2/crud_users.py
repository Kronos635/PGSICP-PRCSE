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


# Insert users
#
# PARAMETERS:
#   con         connection object
#   user        tuple with values to insert
# ----------------------------------
def insert_user(con,user):
    try:
        with con:
            con.execute("insert into users values (?,?,?,?,?,?)", (user))
            return("OK")
    except sqlite3.IntegrityError:
        return("user already exists")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])

# List users Function
#
# PARAMETERS:
#   con         connection object
#   user    string "ALL" or tuple with values to list
#
#   If user = ALL then Select all table
#   Tuple can have wildcards
#
#  RETURN:
#   List of tuples with all table columns, except u_password
# ----------------------------------
def list_user(con,user):
    if user=="ALL":
        return con.execute('SELECT u_username,u_name,u_bank_account_number,u_password_validity,u_password_expire_date FROM users ORDER BY u_username').fetchall()
    else:
        return con.execute('SELECT u_username,u_name,u_bank_account_number,u_password_validity,u_password_expire_date FROM users \
                        WHERE u_username like (?) ORDER BY u_username', (user)).fetchall()

# Find users Function
#
# PARAMETERS:
#   con         connection object
#   user    tuple with user to retrieve
#
#  RETURN:
#   tuple with all table columns
# ----------------------------------
def find_user(con,user):
    return con.execute('SELECT u_username,u_name,u_bank_account_number,u_password_validity,u_password_expire_date FROM users WHERE u_username = (?)', (user)).fetchone()
    
# Update users Function
#
# PARAMETERS:
#   con             connection object
#   update_values   tuple with user information, except u_password and u_password_expire_date. The last element from tuple is the user to update
#
# ----------------------------------
def update_user(con,update_values):
    try:
        with con:
            con.execute('UPDATE users SET u_username = (?), u_name = (?),u_bank_account_number = (?),u_password_validity = (?) \
                        WHERE u_username = (?)', (update_values))
            return("Ok")
    except sqlite3.IntegrityError:
        return("Update failed. Resource name should be unique.")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])

# Update user passsword Function
#
# PARAMETERS:
#   con             connection object
#   update_values   tuple in which 1st element is the new password, the second element is the new computed password expiration date and the third element is the user to update
#
# ----------------------------------
def update_user_password(con,update_values):
    try:
        with con:
            con.execute('UPDATE users SET u_password = (?), \
                                u_password_expire_date = (?) \
                WHERE u_username = (?)', (update_values))
            return("OK")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])


# Delete users Function
#
# PARAMETERS:
#   con     connection object
#   user    tuple with user to delete
# ----------------------------------
def delete_user(con,user):
    try:
        with con:
            con.execute('DELETE FROM users WHERE u_username = (?)', (user))
            return("OK")
    except sqlite3.Error as e:
        return("An error occurred:", e.args[0])
