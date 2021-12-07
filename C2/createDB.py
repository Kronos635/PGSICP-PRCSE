#!/usr/bin/env python3
# coding: utf-8
#
# 20211205 - PGSICP-PRCSE - Grupo2

# Create Database
#
# PARAMETERS:
#   con         connection object
# ----------------------------------
def createTables(con):
    con.execute("create table if not exists resources (rs_name VARCHAR PRIMARY KEY)")
    con.execute("create table if not exists users (u_username varchar PRIMARY KEY, u_name varchar, \
                u_bank_account_number varchar, u_password varchar, u_password_validity int, \
                u_password_expire_date int)")
    con.execute("create table if not exists roles (r_name varchar PRIMARY KEY, r_resource varchar, \
                r_permissions varchar, foreign key (r_resource) REFERENCES resources(rs_name) on update cascade on delete cascade)")
                #")
    con.execute("create table if not exists user_roles (ur_username varchar, ur_role varchar, \
                PRIMARY KEY (ur_username, ur_role), \
                foreign key (ur_username) REFERENCES users(u_username) on update cascade on delete cascade, \
                foreign key (ur_role) REFERENCES roles(r_name) on update cascade on delete cascade)")