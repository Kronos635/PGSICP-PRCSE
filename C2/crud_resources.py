#!/usr/bin/env python
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

def createTables(con):
    con.execute("create table if not exists resources (rs_name varchar unique)")
    con.execute("create table if not exists roles (r_name varchar unique, r_resource varchar, r_permissions varchar)")
    con.execute("create table if not exists users (u_username varchar unique, u_name varchar, \
                u_bank_account_number varchar, u_password varchar, u_password_validity int, u_password_expire_date int)")
    con.execute("create table if not exists user_roles (ur_username varchar, ur_role varchar, \
                primary key (ur_username, ur_role))")

# Insert resources
def insert_resource(con,resource):
    try:
        with con:
            con.execute("insert into resources values (?)", (resource))
    except sqlite3.IntegrityError:
        print("Resource already exists")

# List resources Function
#
# PARAMETERS:
#   tuple resource
#
#   If resource = ALL then Select all table
#   Tuple can have wildcards
def list_resource(con,resource):
    if resource=="ALL":
        for row in con.execute('SELECT * FROM resources ORDER BY rs_name'):
            print(row)
    else:
        for row in con.execute('SELECT * FROM resources WHERE rs_name like (?) ORDER BY rs_name', (resource)):
            print(row)

# Find resources Function
#
# PARAMETERS:
#   tuple resource
#
#  RETURN:
#   tuple with all table columns
def find_resource(con,resource):
    return con.execute('SELECT * FROM resources WHERE rs_name = (?)', (resource)).fetchone()
    
# Update resources Function
#
# PARAMETERS:
#   tuple update. 1st element is the new value, second element is the resource to update
#
def update_resource(con,update_state):
    con.execute('UPDATE resources SET rs_name = (?) WHERE rs_name = (?)', (update_state))

# Delete resources Function
#
# PARAMETERS:
#   tuple resource

def delete_resource(con,resource):
    con.execute('DELETE FROM resources WHERE rs_name = (?)', (resource))
