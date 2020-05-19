#!/usr/bin/env python
import sys
import os
import urllib
import json
from PythonConfluenceAPI import ConfluenceAPI

user = sys.argv[1]
pswd = sys.argv[2]
source_path = sys.argv[3]
file_name = sys.argv[4]

#url = "http://confluence.test.com/rest/api/content/"
#api = ConfluenceAPI(user, pswd, 'http://confluence.test.com/')
url = "http://dev.confluence.test.com:8090/rest/api/content/"
api = ConfluenceAPI(user, pswd, 'http://dev.confluence.test.com:8090/')

def get_content_dict(url):
    open_url = urllib.urlopen(url)
    content = open_url.read()
    return json.loads(content)

list_id = []
for page_dict in get_content_dict(url)["results"]:
    list_id.append(page_dict["id"])

 
for content_id in list_id:
    file_object = open(os.path.join(source_path, file_name), 'r')
    attachment = {"file": file_object, "comment": ""}
    attachment_url = url + content_id + "/child/attachment?filename=" + file_name    
    attachment_content = get_content_dict(attachment_url)

    if attachment_content["results"]: 
        api.update_attachment(content_id, attachment_content["results"][0]["id"], attachment, callback=None)
    else:
        api.create_new_attachment_by_content_id(content_id, attachment, callback=None)
    file_object.close()
