#!/usr/bin/env python3

"""
Converts Drupal 6 blog posts to static site generator input files.

Prerequisites:

- a Drupal 6 MySQL database
- appropriate credentials in dbconfig.py in this directory
- pip3 install mysql-connector-python-rf
- pip3 install Jinja2
"""

from datetime import datetime
from collections import defaultdict
from sys import argv

import mysql.connector

from post import Post
from cactusgenerate import cactus_generate
from hydegenerate import hyde_generate
from pelicangenerate import pelican_generate

# Database credentials are in dbconfig.py.
import dbconfig


def convert_tags(connection):
    """Get the tags associated with each post.

    Return a dictionary where keys are node IDs and values are lists of strings.
    """

    tags = defaultdict(list)

    query = """SELECT tn.nid, td.name
        FROM term_node tn
        JOIN term_data td ON tn.tid = td.tid
        """

    cursor = connection.cursor()
    cursor.execute(query)

    for (nid, name) in cursor:
        tags[nid].append(name)

    cursor.close()

    return tags


def convert_urls(connection):
    """Get the URL associated with each post.

    Return a dictionary where keys are strings like "node/288" and
    values are strings like "2017/04/22/my-first-chess-program".
    """

    urls = {}

    query = """SELECT src, dst
        FROM url_alias
        """

    cursor = connection.cursor()
    cursor.execute(query)

    for (src, dst) in cursor:
        urls[src] = dst

    cursor.close()

    return urls


def convert_posts(connection, urls, tags):
    """Get all published posts.
    
    Return a list of Posts.
    """

    query = """SELECT n.nid, nr.title, n.created, nr.timestamp, ff.name, nr.body
        FROM node n
        JOIN node_revisions nr ON n.nid = nr.nid
        JOIN filter_formats ff ON nr.format = ff.format
        WHERE n.status = 1
        AND n.type = 'story'
        """

    def make_post(nid, title, created, timestamp, filter, body):
        createdDatetime = datetime.utcfromtimestamp(created)
        timestampDatetime = datetime.utcfromtimestamp(timestamp)
        url = urls[f"node/{nid}"]

        post = Post()
        post.nid = nid
        post.title = title
        post.created = createdDatetime
        post.timestamp = timestampDatetime
        post.url = url
        post.tags = tags[nid]
        post.filter = filter
        post.body = body

        return post

    cursor = connection.cursor()
    cursor.execute(query)

    posts = [ make_post(nid, title, created, timestamp, filter, body)
              for (nid, title, created, timestamp, filter, body) in cursor
             ]

    cursor.close()

    return posts


def convert(*generators):
    """Convert blog posts from Drupal 6 database to static site generator files.
    
    Arguments are names of static site generator engines.
    Supported values are "pelican", "cactus" and "hyde".
    """
    connection = mysql.connector.connect(
            user=dbconfig.dbuser,
            password=dbconfig.dbpassword,
            database=dbconfig.db)

    urls = convert_urls(connection)
    tags = convert_tags(connection)
    posts = convert_posts(connection, urls, tags)

    connection.close()

    for generator in generators:
        if generator == 'cactus':
            cactus_generate(posts)
        elif generator == 'hyde':
            hyde_generate(posts)
        elif generator == 'pelican':
            pelican_generate(posts)
        else:
            raise ValueError(f'Unknown generator "{generator}"')


if __name__ == '__main__':
    if len(argv) > 1:
        convert(*argv[1:])
    else:
        convert("cactus", "hyde", "pelican")

