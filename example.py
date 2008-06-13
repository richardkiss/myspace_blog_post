#!/usr/bin/env python2.4

mysql_host = "MYSQL_DB_SERVER"
mysql_user = "USER_NAME"
mysql_passwd = "PASSWORD"
mysql_db = "DB_NAME"
myspace_login = "something@somewhere.com"
myspace_passwd = "A_SECRET_MYSPACE_PASSWORD0"

import wordpress

wordpress.stitch_from_wordpress(mysql_host, mysql_user, mysql_passwd, mysql_db, myspace_login, myspace_passwd)
