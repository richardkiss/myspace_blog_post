#!/usr/bin/env python

import re
import urllib
import urllib2

# CATEGORIES=(
#     1, "Art and Photography",
#     4, "Automotive",
#     2, "Blogging",
#     6, "Dreams and the Supernatural",
#     3, "Fashion, Style, Shopping",
#     7, "Food and Restaurants",
#     8, "Friends",
#     9, "Games",
#     10, "Goals, Plans, Hopes",
#     11, "Jobs, Work, Careers",
#     12, "Life",
#     14, "Movies, TV, Celebrities",
#     15, "Music",
#     16, "MySpace",
#     17, "News and Politics",
#     18, "Parties and Nightlife",
#     19, "Pets and Animals",
#     26, "Podcast",
#     20, "Quiz/Survey",
#     21, "Religion and Philosophy",
#     13, "Romance and Relationships",
#     22, "School, College, Greek",
#     23, "Sports",
#     24, "Travel and Places",
#     5, "Web, HTML, Tech",
#     25, "Writing and Poetry",
#     )

cp = urllib2.HTTPCookieProcessor()
urllib2.install_opener(urllib2.build_opener(cp))

def no_op(page):
    return 0

def myspace_login(email, password, log_response = no_op):
    # returns url opener
    data = urllib.urlencode({"email":email, "password":password, "Remember":0})
    req = urllib2.Request('http://login.myspace.com/index.cfm?fuseaction=login.process',
                          data)
    f = urllib2.urlopen(req)
    d = f.read()
    f.close()
    log_response(d)

def post_entry(login, password, post_date, subject, text_body, category_id = 0, log_response = no_op):
    """
    This function automatically posts a blog entry to a MySpace blog by scraping through the login, then
    the blog posting screen.
    
    post_date is a datetime object
    login, password, subject are all strings.
    text_body is a string with HTML
    log_response is an optional callback for debugging; it gets called back with the contents of
    the HTML at each step.
    """
    myspace_login(login, password)
    f = urllib2.urlopen("http://blog.myspace.com/index.cfm?fuseaction=blog.create&editor=false")
    log_response(f.read())
    f.close()
    year, month, day = post_date.year, post_date.month, post_date.day
    hour, minute, second = (post_date.hour-1)%12+1, post_date.minute, post_date.second
    ampm = "PM"
    if post_date.hour < 13: ampm = "AM"
    dictionary = {"blogID" : -1, "postMonth": month, "postDay": day, "postYear": year,
                  "postHour": hour, "postMinute": minute, "postTimeMarker": ampm,
                  "subject": subject, "BlogCategoryID": category_id, "editor": "false",
                  "body": text_body, "CurrentlyASIN": '', 
                  "CurrentlyProductName": "",
                  "CurrentlyProductBy": "",
                  "CurrentlyImageURL": "",
                  "CurrentlyProductURL": "",
                  "CurrentlyProductReleaseDate": "",
                  "CurrentlyProductType": "",
                  "Mode":"music",
                  "MoodSetID":7,
                  "MoodID":0,
                  "MoodOther":"",
                  "BlogViewingPrivacyID":0,
                  "Enclosure":''
                  }
    data = urllib.urlencode(dictionary)
    url = "http://blog.myspace.com/index.cfm?fuseaction=blog.previewBlog"
    req = urllib2.Request(url, data)
    f = urllib2.urlopen(req)
    t1 = f.read()
    f.close()
    log_response(t1)
    m = re.search(r'\<form method="post" name="theForm" id="theForm"\>(.+)\</form\>', t1, re.DOTALL)
    assert m
    t1 = m.group(1)
    data = urllib.urlencode(dict(re.findall(r'\<input type="hidden"\s+name="(.+)?"\s+value="(.+)"\>', t1)))
    url = "http://blog.myspace.com/index.cfm?fuseaction=blog.processCreate"
    req = urllib2.Request(url, data)
    f = urllib2.urlopen(req)
    t1 = f.read()
    f.close()
    log_response(t1)
