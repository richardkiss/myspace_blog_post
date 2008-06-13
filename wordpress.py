#!/usr/bin/env python

import MySQLdb

from myspace_blog import post_entry

def get_posts(host, user, passwd, db):
    c = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cu = c.cursor()
    r = cu.execute("select post_title, post_content, post_date from wp_posts order by post_date asc")
    return cu

def stitch_from_wordpress(mysql_host, mysql_user, mysql_passwd, mysql_db, myspace_login, myspace_passwd):
    posts = [t for t in get_posts(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db)]

    for i,p in enumerate(posts):
        print "%2d) %s" % (i+1, p[0])

    n = int(raw_input("choose post to copy to MySpace %s>" % myspace_login))

    subject, text_body, post_date = posts[n-1]

    print subject
    print text_body
    print post_date

    post_entry(myspace_login, myspace_passwd, post_date, subject, text_body)

