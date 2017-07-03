#!/usr/bin/env python3

# Prerequisites:
#
# pip3 install mysql-connector-python-rf

import config
import mysql.connector

cnx = mysql.connector.connect(
        user=config.dbuser,
        password=config.dbpassword,
        database=config.db)

print("I think we're connected?")

cnx.close()


