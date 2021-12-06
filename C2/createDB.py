#!/usr/bin/env python
# coding: utf-8
#
# 20211205 - PGSICP-PRCSE - Grupo2

# Create Database
#
# PARAMETERS:
#   con         connection object
# ----------------------------------
def createTables(con):
    con.execute("create table if not exists resources (rs_name varchar unique)")
    con.execute("create table if not exists roles (r_name varchar unique, r_resource varchar, r_permissions varchar)")
    con.execute("create table if not exists users (u_username varchar unique, u_name varchar, \
                u_bank_account_number varchar, u_password varchar, u_password_validity int, u_password_expire_date int)")
    con.execute("create table if not exists user_roles (ur_username varchar, ur_role varchar, \
                primary key (ur_username, ur_role))")