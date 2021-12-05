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

import sqlite3

try:
    con = sqlite3.connect('example.db')
except:
        print("Not possible to connect to database")

def createTables():
    con.execute("create table if not exists resources (rs_name varchar unique)")
    con.execute("create table if not exists roles (r_name varchar unique, r_resource varchar, r_permissions varchar)")
    con.execute("create table if not exists users (u_username varchar unique, u_name varchar, \
                u_bank_account_number varchar, u_password varchar, u_password_validity int, u_password_expire_date int)")
    con.execute("create table if not exists user_roles (ur_username varchar, ur_role varchar, \
                primary key (ur_username, ur_role))")

def insert_resource(resource):
    try:
        with con:
            con.execute("insert into resources values (?)", (resource))
    except sqlite3.IntegrityError:
        print("Resource already exists")

def list_resource(resource):
    if resource=="ALL":
        for row in con.execute('SELECT * FROM resources ORDER BY rs_name'):
            print(row)
    else:
        for row in con.execute('SELECT * FROM resources WHERE rs_name like (?) ORDER BY rs_name', (resource)):
            print(row)


#createTables()
#resource=("resource1",)
#insert_resource(resource)
#resource=("resource2",)
#insert_resource(resource)
#resource=("resource3",)
#insert_resource(resource)

#list_resource(("ALL",))

#insert_resource(resource)

#con.close()
