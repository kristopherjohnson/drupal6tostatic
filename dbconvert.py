#!/usr/bin/env python3

# Prerequisites:
#
# - A Drupal 6 MySQL database
# - Appropriate credentials in dbconfig.py in this directory
# - pip3 install mysql-connector-python-rf
# - pip3 install Jinja2

from datetime import datetime
from collections import defaultdict
import mysql.connector

from post import Post
from cactusgenerate import cactus_generate

# Database credentials are in dbconfig.py.
import dbconfig


def convert_tags(connection):
    """
    Get the tags associated with each post.

    Returns a dictionary where keys are node IDs and values are lists of strings.
    """

    tags = defaultdict(list)

    query = """
        SELECT tn.nid, td.name
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
    """
    Get the URL associated with each post.

    Returns a dictionary where keys are strings like "node/288" and
    values are strings like "2017/04/22/my-first-chess-program".
    """

    urls = {}

    query = """
        SELECT src, dst
        FROM url_alias
        """

    cursor = connection.cursor()
    cursor.execute(query)

    for (src, dst) in cursor:
        urls[src] = dst

    cursor.close()

    return urls


def convert_posts(connection, urls, tags):
    """
    Get all published posts.
    
    Returns a list of Posts.
    """

    query = """
        SELECT n.nid, nr.title, n.created, nr.timestamp, ff.name, nr.body
        FROM node n
        JOIN node_revisions nr ON n.nid = nr.nid
        JOIN filter_formats ff ON nr.format = ff.format
        WHERE n.status = 1
        AND n.type = 'story'
        """

    posts = []

    cursor = connection.cursor()
    cursor.execute(query)

    for (nid, title, created, timestamp, filter, body) in cursor:
        createdDatetime = datetime.utcfromtimestamp(created)
        timestampDatetime = datetime.utcfromtimestamp(timestamp)
        url = urls[f"node/{nid}"]

        if True:
            post = Post()
            post.nid = nid
            post.title = title
            post.created = createdDatetime
            post.timestamp = timestampDatetime
            post.url = url
            post.tags = tags
            post.filter = filter
            post.body = body
        else:
            post = {
                "nid": nid,
                "title": title,
                "created": createdDatetime,
                "timestamp": timestampDatetime,
                "url": url,
                "tags": tags,
                "filter": filter,
                "body": body
            }

        posts.append(post)

        if False:
            print("----")
            print(f"nid: {nid}")
            print(f"title: {title}")
            print(f"created: {createdDatetime}")
            print(f"timestamp: {timestampDatetime}")
            print(f"url: {url}")
            print(f"tags: {tags[nid]}")
            print(f"filter: {filter}")
            print(f"body: {body[0:40]}...")

    cursor.close()

    return posts


def convert():
    """Convert everything from Drupal 6 database to static site generator files."""
    connection = mysql.connector.connect(
            user=dbconfig.dbuser,
            password=dbconfig.dbpassword,
            database=dbconfig.db)

    urls = convert_urls(connection)
    tags = convert_tags(connection)
    posts = convert_posts(connection, urls, tags)

    connection.close()

    cactus_generate(posts)

if __name__ == '__main__':
    convert()

