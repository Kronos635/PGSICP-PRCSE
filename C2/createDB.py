#!/usr/bin/env python3
# coding: utf-8
#
# 20211205 - PGSICP-PRCSE - Grupo2

import logging 
import app_logging

# Create Database
#
# PARAMETERS:
#   con         connection object
# ----------------------------------
def createTables(con):
    # Create resources table
    #
    # FIELDS:
    #   rs_name - Nome of the resource (PRIMARY KEY)
    con.execute("create table if not exists resources (rs_name VARCHAR PRIMARY KEY)")
    logging.info(f'### INFO - Table "resources" created ###\n')

    # Create users table
    #
    # FIELDS:
    #   u_username - username in e-mail format (PRIMARY KEY)
    #   u_name - User name
    #   u_bank_account_number - User account number
    #   u_password - User account password
    #   u_password_validity - Password validity
    #   u_passsord_expire_date - Date in which the password should be changed.
    #                            It's a computed value between the date in which the user last changed his password and the 'u_password_validity'
    con.execute("create table if not exists users (u_username varchar PRIMARY KEY, u_name varchar NOT NULL, \
                u_bank_account_number varchar NOT NULL, u_password varchar NOT NULL, u_password_validity int DEFAULT 30, \
                u_password_expire_date int NOT NULL)")
    logging.info(f'### INFO - Table "users" created ###\n')

    # create roles table
    # The "roles" table has r_resource as a foreign key from "resources" table.
    # "cascades" exists to maintain relationships integrity in case of resources updates or deletion
    #
    # FIELDS:
    #   r_name - Role name (PRIMARY KEY)
    #   r_resource - Resource over which the role is to be applied
    #   r_permissions - Permissions to be granted by this role. It should be one of 2 values:
    #                   'r' - If user onlye has reading permission over the resource
    #                   'w' - If the user has read/write permissions over the resource
    con.execute("create table if not exists roles (r_name varchar UNIQUE NOT NULL, r_resource varchar, r_permissions varchar, \
                PRIMARY KEY (r_resource,r_permissions), \
                foreign key (r_resource) REFERENCES resources(rs_name) on update cascade on delete cascade)")
    logging.info(f'### INFO - Table "roles" created ###\n')

    # create user_roles table. This is the relational table.
    # The "user_roles" table has 2 foreign keys: ur_role as a foreign key from "roles" table and ur_username as a foreign key from "users"
    # "cascades" exists to maintain relationships integrity in case of updates or deletion on both "users" or "roles" tables
    #
    # FIELDS:
    #   ur_username - Username to which the role is to be applied (PRIMARY KEY)
    #   ur_role - role to be applied (PRIMARY KEY)
    con.execute("create table if not exists user_roles (ur_username varchar, ur_role varchar, \
                PRIMARY KEY (ur_username, ur_role), \
                foreign key (ur_username) REFERENCES users(u_username) on update cascade on delete cascade, \
                foreign key (ur_role) REFERENCES roles(r_name) on update cascade on delete cascade)")
    logging.info(f'### INFO - Table "user_roles" created ###\n')