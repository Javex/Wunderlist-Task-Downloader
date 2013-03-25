#!/usr/bin/env python
# encoding: utf-8
import requests
import json
from collections import OrderedDict
from datetime import datetime
from pprint import pprint
from wunderlist_config import USER, PASSWORD

session = requests.Session()

login_data = json.dumps({'email': USER, 'password': PASSWORD})
r = session.post('https://api.wunderlist.com/login', login_data)
ret = r.json()
session.headers['Authorization'] = 'Bearer {0}'.format(ret['token'])

ops = json.dumps({'ops': [{"method": "get", "url": "/me/lists"}],
                   "sequential": True})


r = session.post('https://api.wunderlist.com/batch', ops)
data = r.json()
task_list_raw = data["results"][0]["body"]

task_list = [(d["position"], 
  d["id"],
  d["title"]) for d in task_list_raw]

task_list.append((1.0, 'inbox', 'Inbox'))
task_list = sorted(task_list, key=lambda t: t[0])
lists = OrderedDict((t[1], (t[2], [])) for t in task_list)
pprint(lists)


ops = json.dumps({'ops': [{"method": "get", "url": "/inbox/tasks"}], 
                  "sequential": True})
r = session.post('https://api.wunderlist.com/batch', ops)
data = r.json()


def from_iso8601(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

class Task(object):

    def __init__(self, api_data):

        date_list = ["completed_at", "created_at", "due_date"]
        for date_obj in date_list:
            try:
                setattr(self, date_obj, from_iso8601(api_data[date_obj]))
            except TypeError:
                setattr(self, date_obj, None)
        self.id = api_data["id"]
        self.list_id = api_data["list_id"]
        self.local_identifier = api_data["local_identifier"]
        self.note = api_data["note"]
        self.position = api_data["position"]
        self.starred = api_data["starred"]
        self.title = api_data["title"]
        self._all_data = api_data

    @property
    def completed(self):
        return bool(self.completed_at)

    def __str__(self):
        return "{0}: {1}".format(self.list_id, self.title)

    def __repr__(self):
        return str(self)


all_tasks = []
for task in data["results"][0]["body"]:
    all_tasks.append(Task(task))

ops = json.dumps({'ops': [{"method": "get", "url": "/me/tasks"}],
                  'sequential': True})
r = session.post('https://api.wunderlist.com/batch', ops)
data = r.json()

for task in data["results"][0]["body"]:
    all_tasks.append(Task(task))

for task in all_tasks:
    l = lists[task.list_id]
    l[1].append(task)

pprint(lists)
