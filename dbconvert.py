#!/usr/bin/env python3

# Prerequisites:
#
# - A Drupal 6 MySQL database
# - pip3 install mysql-connector-python-rf

from datetime import datetime
from collections import defaultdict
import mysql.connector

# Database credentials are in dbconfig.py.
import dbconfig

# Mapping of nid to list of tags.
tags = defaultdict(list)

# Mapping of URL like "node/288" to URL like "2017/04/22/my-first-chess-program".
urls = {}

def convert_tags(cnx):
    """Get the tags associated with each post, storing them in the global tags variable."""

    query = """SELECT tn.nid, td.name
    FROM term_node tn
    JOIN term_data td ON tn.tid = td.tid
    """

    cursor = cnx.cursor()
    cursor.execute(query)

    for (nid, name) in cursor:
        tags[nid].append(name)

    cursor.close()

def convert_urls(cnx):
    """Get the URL associated with each post."""

    query = """SELECT src, dst
    FROM url_alias
    """

    cursor = cnx.cursor()
    cursor.execute(query)

    for (src, dst) in cursor:
        urls[src] = dst

    cursor.close()

def convert_posts(cnx):
    """Get all published posts."""

    query = """SELECT n.nid, nr.title, n.created, nr.timestamp, ff.name, nr.body
        FROM node n
        JOIN node_revisions nr ON n.nid = nr.nid
        JOIN filter_formats ff ON nr.format = ff.format
        WHERE n.status = 1
        AND n.type = 'story'
        """

    cursor = cnx.cursor()
    cursor.execute(query)

    for (nid, title, created, timestamp, filter, body) in cursor:
        print("----")
        print(f"nid: {nid}")
        print(f"title: {title}")
        print(f"created: {datetime.utcfromtimestamp(created)}")
        print(f"timestamp: {datetime.utcfromtimestamp(timestamp)}")
        print(f"filter: {filter}")
        print(f"body: {body[0:40]}...")

    cursor.close()

def convert():
    """Convert everything from Drupal 6 database to static site generator files."""
    cnx = mysql.connector.connect(
            user=dbconfig.dbuser,
            password=dbconfig.dbpassword,
            database=dbconfig.db)

    convert_posts(cnx)
    convert_tags(cnx)
    convert_urls(cnx)

    cnx.close()

convert()

