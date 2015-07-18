#!/usr/bin/python

import sqlite3


sqlite_file = 'blog_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute(
    "Create table blog(blog_id INTEGER PRIMARY KEY,blog_title TEXT,blog_content TEXT,category TEXT);")
c.execute("Create table category(cat_id INTEGER PRIMARY KEY,category TEXT);")
conn.commit()
conn.close()
